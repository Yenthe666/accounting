# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, Command


class AccountMove(models.Model):
    _inherit = "account.move"

    def print_and_send_automatic_emails(self):
        """
            Loops over a recordset of invoices (account.move) to trigger the send & print wizard and to automatically
            send the invoice(s) out to the customer(s)
        """
        email_template = self.env['ir.config_parameter'].sudo().get_param('sale.auto_email_template_id')
        template = self.env['mail.template'].search([('id', '=', email_template)], limit=1)

        for item in self:
            # Emails need to be sent out one-by-one to be, for them to appear in the invoice chatter
            item._print_and_send_down_payment(template)

            # The invoice could be confirmed/emailed but is not yet commited in the database.
            # Let's make sure to have everything stored to never do operations twice.
            self.env.cr.commit()

    def _print_and_send_down_payment(self, template):
        """
            Sends and prints out the PDF for one single invoice
            Args:
                template (record): mail template to be used for sending out the email
        """
        self.ensure_one()

        ctx = self._prepare_automatic_downpayment_email_ctx()
        values = self._prepare_automatic_downpayment_email_values(template)

        # Generate an e-mail wizard & prepare it
        invoice_to_send = self.env['account.invoice.send'].with_context(ctx).create(values)
        invoice_to_send._compute_composition_mode()
        invoice_to_send.onchange_template_id()
        invoice_to_send.onchange_is_email()

        # Send out the mail
        invoice_to_send.send_and_print_action()

    def _prepare_automatic_downpayment_email_ctx(self):
        """
            Prepares a dictionary with all values needed to build up an e-mail wizard (account.invoice.send)
        """
        return dict(
            mark_invoice_as_sent=True,
            active_ids=self.ids,
            force_email=True,
            default_res_model='account.move',
            default_use_template=False,
        )

    def _prepare_automatic_downpayment_email_values(self, template):
        """
            Prepares all values (dictionary) needed to set on an e-mail wizard (account.invoice.send)
        """
        return {
            'model': 'account.move',
            'res_id': self.id,
            'template_id': template.id,
            'composition_mode': 'comment',
            'is_email': True
        }
