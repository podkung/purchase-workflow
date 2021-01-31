# Copyright 2021 ProThai Technology Co.,Ltd. (http://prothaitechnology.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

import base64

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    rfq_number = fields.Char(
        "RFQ Reference",
        index=True,
        copy=False,
        default="New",
    )

    @api.model
    def create(self, vals):
        company = False
        if "company_id" in vals:
            company = self.env["res.company"].browse(vals.get("company_id"))
        else:
            company = self.env.company
        if not company.keep_name_po and vals.get("name", "New") == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("purchase.rfq") or "New"
            vals["rfq_number"] = vals["name"]
        return super().create(vals)

    def button_confirm(self):
        for order in self:
            if (
                order.state not in ["draft", "sent"]
                and not order.company_id.keep_name_po
            ):
                continue
            else:
                order.write(
                    {
                        "name": self.env["ir.sequence"].next_by_code("purchase.order"),
                    }
                )

            # save rfq pdf as attachment
            order.action_get_rfq_attachment()

        return super().button_confirm()

    def action_get_rfq_attachment(self):
        rfq_pdf = self.env.ref("purchase.report_purchase_quotation")._render_qweb_pdf(
            self.id
        )[0]
        return self.env["ir.attachment"].create(
            {
                "name": "%s.pdf" % (self.rfq_number),
                "type": "binary",
                "datas": base64.encodebytes(rfq_pdf),
                "res_model": self._name,
                "res_id": self.id,
            }
        )
