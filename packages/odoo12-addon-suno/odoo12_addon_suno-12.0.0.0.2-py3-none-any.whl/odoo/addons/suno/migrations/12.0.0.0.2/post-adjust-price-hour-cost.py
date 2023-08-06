from odoo import SUPERUSER_ID, api

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    account_analytic_lines = env["account.analytic.line"].search([
        ["amount", "=", 0.00],
        ["unit_amount", "!=", 0.00],
        ["employee_id", "!=", None]
    ])
    for line in account_analytic_lines:
        line.amount = -line.unit_amount * line.employee_id.timesheet_cost
