# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    followup_enabled = fields.Boolean(
        string='Send follow-up reminders',
        default=True
    )

    @api.onchange('followup_enabled')
    def _onchange_followup_enabled(self):
        self.sudo()._compute_for_followup()

    def _compute_for_followup(self):
        """
        Set the followup status to no_action_needed when followup_enabled is set on the partner
        """
        super(ResPartner, self)._compute_for_followup()
        for record in self:
            if not record.followup_enabled:
                record.followup_status = 'no_action_needed'
