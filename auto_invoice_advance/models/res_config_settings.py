# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deposit_default_percentage = fields.Float(
        'Default deposit percentage',
        config_parameter='sale.deposit_default_percentage',
        help='Default percentage for automatic deposits'
    )

    auto_confirm_down_payment = fields.Boolean(
        string='Automatically confirm down payments',
        help='If set to true, the action will confirm the auto generated down payments.',
        config_parameter='sale.auto_confirm_down_payment'
    )

    auto_email_down_payment = fields.Boolean(
        string='Automatically send down payment email to customer',
        help='If set to true, the action will send out the down payment invoice to the customer when available',
        config_parameter='sale.auto_email_down_payment'
    )

    auto_email_template_id = fields.Many2one(
        'mail.template',
        string='Down payment email',
        help='Email template used to send out down payment invoices to customers',
        config_parameter='sale.auto_email_template_id',
        domain=[('model_id', '=', 'account.move')]
    )

    @api.constrains('deposit_default_percentage')
    def _check_constraint_deposit_default_percentage(self):
        if not (0 < self.deposit_default_percentage <= 100):
            raise ValidationError(_('The deposit amount must be between 0 and 100.'))
