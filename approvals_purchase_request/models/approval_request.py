# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ApprovalRequest(models.Model):
    _inherit = "approval.request"

    purchase_request_count = fields.Integer(compute="_compute_purchase_request_count")

    @api.depends("product_line_ids.purchase_request_line_id")
    def _compute_purchase_request_count(self):
        for request in self:
            purchase_requests = (
                request.product_line_ids.purchase_request_line_id.request_id
            )
            request.purchase_request_count = len(purchase_requests)

    def action_cancel(self):
        """Override to notify Purchase Requests when the
        Approval Request is cancelled."""
        res = super().action_cancel()
        purchase_requests = self.product_line_ids.purchase_request_line_id.request_id
        for request in purchase_requests:
            product_lines = self.product_line_ids.filtered(
                lambda line: line.purchase_request_line_id.request_id.id == request.id
            )
            request._activity_schedule_with_view(
                "mail.mail_activity_data_warning",
                views_or_xmlid=(
                    "approvals_purchase_request.exception_approval_request_canceled"
                ),
                user_id=self.env.user.id,
                render_context={
                    "approval_requests": self,
                    "product_lines": product_lines,
                },
            )
        return res

    def action_confirm(self):
        for request in self:
            if (
                request.approval_type == "purchase_request"
                and not request.product_line_ids
            ):
                raise UserError(_("You cannot create an empty purchase request."))
        return super().action_confirm()

    def _prepare_purchase_request(self):
        self.ensure_one()
        vals = {
            "origin": self.name,
            "company_id": self.company_id.id,
            "requested_by": self.request_owner_id.id,
            "description": "XXXXXXXXXXXXXXXxx",
        }
        return vals

    def _prepare_purchase_request_line(self, line, request):
        line_val = {
            "request_id": request.id,
            "product_id": line.product_id.id,
            "name": "PRODUCT XXX",
            "product_qty": line.quantity,
            "product_uom_id": line.product_uom_id.id,
            "estimated_cost": 111,
            "specifications": "SPEC XXX",
        }
        return line_val

    def action_create_purchase_request(self):
        """ Create and/or modifier Purchase Reuqest. """
        self.ensure_one()
        pr_vals = self._prepare_purchase_request()
        new_request = self.env["purchase.request"].create(pr_vals)
        for line in self.product_line_ids:
            pr_line_vals = self._prepare_purchase_request_line(line, new_request)
            new_pr_line = self.env["purchase.request.line"].create(pr_line_vals)
            line.purchase_request_line_id = new_pr_line.id

    def action_open_purchase_requests(self):
        """Return the list of purchase requests the approval request created or
        affected in quantity."""
        self.ensure_one()
        request_ids = self.product_line_ids.purchase_request_line_id.request_id.ids
        domain = [("id", "in", request_ids)]
        action = {
            "name": _("Purchase Request"),
            "view_type": "tree",
            "view_mode": "list,form",
            "res_model": "purchase.request",
            "type": "ir.actions.act_window",
            "context": self.env.context,
            "domain": domain,
        }
        return action
