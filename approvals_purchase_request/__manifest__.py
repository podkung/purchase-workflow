# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Approvals - Purchase Request",
    "version": "14.0.1.0.0",
    "category": "Human Resources/Approvals",
    "website": "https://github.com/OCA/purchase-workflow",
    "summary": """
        This module adds to the approvals workflow the possibility to generate
        Purchase Request from an Approvals of Purchase Request.
    """,
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["approvals", "purchase_request"],
    "data": [
        "data/approval_category_data.xml",
        "data/mail_data.xml",
        "views/approval_category_views.xml",
        "views/approval_product_line_views.xml",
        "views/approval_request_views.xml",
    ],
    "demo": [
        "data/approval_demo.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": True,
}
