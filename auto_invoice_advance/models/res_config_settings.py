# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deposit_default_percentage = fields.Float(
        'Default deposit percentage',
        config_parameter='sale.deposit_default_percentage',
        help='Default percentage for automatic deposits')

    @api.constrains('deposit_default_percentage')
    def _check_constraint_deposit_default_percentage(self):
        if not (0 < self.deposit_default_percentage <= 100):
            raise ValidationError(_('The deposit amount must be between 0 and 100.'))
