# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.fields import Command


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def create_down_payment_invoices(self):
        self._prepare_tax_id()
        invoice_id = self._create_invoices(self.sale_order_ids)
        can_be_confirmed = True

        if not self.deposit_taxes_id:
            can_be_confirmed = False
            self.env['mail.message'].create(self._prepare_mail_message_values(invoice_id))

        return {
            'invoice_id': invoice_id,
            'can_be_confirmed': can_be_confirmed
        }

    def _prepare_tax_id(self):
        # When there is a product_id set, update its taxes_id to the one we want to use.
        if self.product_id:
            # Remove the taxes in case we could not figure it out
            self.product_id.taxes_id = None

            # Set the tax id according to the sale if present
            if self.deposit_taxes_id:
                self.product_id.taxes_id = [Command.set(self.deposit_taxes_id.ids)]

    def _prepare_mail_message_values(self, invoice_id):
        """
            Prepares all values needed to create a new mail.message record with info about why we did not confirm/email
            the invoice. (multiple taxes)
        """
        return{
            'model': 'account.move',
            'res_id': invoice_id.id,
            'subject': 'Could not set taxes on invoice',
            'message_type': 'notification',
            'subtype_id': self.env.ref('mail.mt_note').id,
            'author_id': self.env.user.id,
            'body': _('We could not automatically set the taxes on the down payment lines as '
                      'there are multiple taxes (or no taxes) set on the related order.')
        }
