# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ApprovalProductLine(models.Model):
    _inherit = "approval.product.line"

    pr_uom_qty = fields.Float(
        "PR UoM Quantity",
        compute="_compute_pr_uom_qty",
        help="The quantity converted into the UoM used by the product in PR.",
    )
    purchase_request_line_id = fields.Many2one("purchase.request.line")

    @api.depends("approval_request_id.approval_type", "product_uom_id", "quantity")
    def _compute_pr_uom_qty(self):
        for line in self:
            approval_type = line.approval_request_id.approval_type
            if (
                approval_type == "purchase_request"
                and line.product_id
                and line.quantity
            ):
                uom = line.product_uom_id or line.product_id.uom_id
                line.pr_uom_qty = uom._compute_quantity(
                    line.quantity, line.product_id.uom_po_id
                )
            else:
                line.pr_uom_qty = 0.0
