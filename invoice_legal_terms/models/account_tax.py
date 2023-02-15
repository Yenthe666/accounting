# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class AccountTax(models.Model):
    _inherit = 'account.tax'

    invoice_terms = fields.Html(
        string='Invoice terms',
        translate=True
    )
