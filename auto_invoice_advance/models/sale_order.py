# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    down_payment_id = fields.Many2one(
        'account.move',
        string="Down payment invoice",
        readonly=True,
        help="Auto generated down payment invoice",
        copy=False
        )

    def _cron_create_advance_invoices(self):
        """
            Creates invoices in draft and depending on the configuration confirms them and emails them
        """
        orders = self.search(self._prepare_order_deposit_domain())
        if len(orders) == 0:
            return  # Nothing to be processed
        _logger.info(f"Creating {len(orders)} advance invoices for sale.orders: {orders.ids}")

        # Get the configurations
        percentage_amount = self.env['ir.config_parameter'].sudo().get_param('sale.deposit_default_percentage')
        confirm_down_payment = self.env['ir.config_parameter'].sudo().get_param('sale.auto_confirm_down_payment')
        do_send_email = self.env['ir.config_parameter'].sudo().get_param('sale.auto_email_down_payment')

        down_payments_to_create = []
        for order in orders:
            down_payments_to_create.append(self._prepare_down_payment_values(order, percentage_amount))

        # Creates the down payments (account.move records)
        self._create_advance_invoices(
            down_payments_to_create,
            confirm_down_payment,
            do_send_email
        )

    def _create_advance_invoices(self, down_payments_to_create, confirm_down_payment, do_send_email):
        """
            Creates invoices for all matching sale orders
            Args:
                down_payments_to_create (list): list with a set of values within to create invoices in bulk
                confirm_down_payment (string): parameter based on the configuration of the user to know if the
                    invoice(s) should be automatically confirmed or not
                do_send_email (string): parameter based on the configuration of the user to know if the invoice(s)
                    should be automatically e-mailed to the customer or not
        """
        payment_invoices = self.env['sale.advance.payment.inv'].create(down_payments_to_create)
        invoice_confirmable_ids = self.env['account.move']
        # Loop over the sale.advance.payment.inv wizard(s) to generate one invoice at a time through the default
        # Odoo code flows (we reuse their code)
        for payment_invoice in payment_invoices:
            response = payment_invoice.create_down_payment_invoices()
            invoice_id = response.get('invoice_id')

            if response.get('can_be_confirmed'):
                invoice_confirmable_ids += invoice_id

            # Link the created down payment invoice to the sale order(s)
            # Note that there can be multiple sale orders on a single invoice, link all of them to the invoice
            for sale_order_id in payment_invoice.sale_order_ids:
                sale_order_id.down_payment_id = invoice_id

        # The setting in the database is configured that the customer wants the invoice(s) to be automatically booked
        if confirm_down_payment:
            invoice_confirmable_ids.action_post()
            # The setting in the database is configured that the customer wants the invoice(s) to be automatically
            # emailed too - let's do so.
            if do_send_email:
                invoice_confirmable_ids.print_and_send_automatic_emails()

        _logger.info(f'Created {len(payment_invoices)} advance invoices')

    def _prepare_order_deposit_domain(self):
        """
            Returns the domain used to find all sale orders that match to generate a first down payment invoice for
        """
        return [
            ('state', '=', 'sale'),         # For all the confirmed sales
            ('invoice_ids', '=', None)      # Without any invoices
        ]

    def _prepare_down_payment_values(self, order_id, percentage_amount):
        """
            Returns the values needed to create a down payment wizard (as if you'd click through the UI on the
            'Create Invoice' button on a sale order) based on the configuration values in the database.
            Args:
                order_id (record): current sale.order record
                percentage_amount (float): percentage of the total value we should create a down payment (invoice) for
        """
        # We will only allow the automatic confirming of invoices with one tax
        deposit_taxes_id = self._try_get_tax_id(order_id)

        return {
            'sale_order_ids': order_id,
            'advance_payment_method': 'percentage',
            'amount': percentage_amount,
            'deposit_taxes_id': deposit_taxes_id,
        }

    def _try_get_tax_id(self, order_id):
        """
            Checks if a sale order has multiple taxes or not.
            If we only find one tax we simply use that tax to put it on our invoice line.
            If we find multiple taxes (e.g 6% & 21% VAT) we return nothing, do not auto-confirm the invoice and later
            on add an activity on the invoice.
            Args:
                order_id (record): current sale.order record
        """
        tax_ids = []
        for order_line in order_id.order_line:
            if order_line.tax_id not in tax_ids:
                tax_ids.append(order_line.tax_id)
        return tax_ids[0] if len(tax_ids) == 1 else None
