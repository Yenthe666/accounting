# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    followup_disabled = fields.Boolean(
        string='Followup disabled'
    )

    @api.onchange('followup_disabled')
    def _onchange_followup_disabled(self):
        self._compute_for_followup()

    def _compute_for_followup(self):
        """
        Set the followup status to no_action_needed when followup_disabled is set on the partner
        """
        super(ResPartner, self)._compute_for_followup()
        for record in self:
            if record.followup_disabled:
                record.followup_status = 'no_action_needed'
