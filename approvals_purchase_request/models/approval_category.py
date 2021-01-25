# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ApprovalCategory(models.Model):
    _inherit = "approval.category"

    approval_type = fields.Selection(
        selection_add=[("purchase_request", "Create PR's")]
    )

    @api.onchange("approval_type")
    def _onchange_approval_type(self):
        if self.approval_type == "purchase_request":
            self.has_product = "required"
            self.has_quantity = "required"
