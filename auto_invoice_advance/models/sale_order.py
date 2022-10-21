# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _cron_create_advance_invoices(self):
        order_ids = self.search(self._prepare_order_deposit_domain())
        if len(order_ids) == 0:
            return  # Nothing to be processed
        _logger.info(f"Creating {len(order_ids)} advance invoices for sale.orders: {order_ids.ids}")

        percentage_amount = self.env['ir.config_parameter'].sudo().get_param('sale.deposit_default_percentage')
        down_payments_to_create = []
        for order_id in order_ids:
            down_payments_to_create.append(self._prepare_down_payment_values(order_id, percentage_amount))
        self._create_advance_invoices(down_payments_to_create)

    def _create_advance_invoices(self, down_payments_to_create):
        payment_inv_ids = self.env['sale.advance.payment.inv'].create(down_payments_to_create)
        for payment_inv_id in payment_inv_ids:
            payment_inv_id.create_invoices()  # singleton check in code, so unable to bulk process
            self.env.cr.commit()
        _logger.info(f'Created {len(payment_inv_ids)} advance invoices')

    def _prepare_order_deposit_domain(self):
        return [('state', '=', 'sale'),         # For all the confirmed sales
                ('invoice_ids', '=', None)]     # Without any invoices

    def _prepare_down_payment_values(self, order_id, percentage_amount):
        return {
            'sale_order_ids': order_id,
            'advance_payment_method': 'percentage',
            'amount': percentage_amount
        }
