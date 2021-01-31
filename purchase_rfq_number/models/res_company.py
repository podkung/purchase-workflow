# Copyright 2021 ProThai Technology Co.,Ltd. (http://prothaitechnology.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    keep_name_po = fields.Boolean(
        string="Use Same Enumeration",
        help="If this is unchecked, purchase rfq use a different sequence from "
        "Purchase orders",
        default=True,
    )


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    keep_name_po = fields.Boolean(related="company_id.keep_name_po", readonly=False)
