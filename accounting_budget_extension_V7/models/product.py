
# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta
from odoo import api, exceptions, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

class Product(models.Model):
    _inherit = 'product.template'

    @api.model
    def _default_start_date(self):
        fiscal_day = self.env.user.company_id.fiscalyear_last_day
        fiscal_month = self.env.user.company_id.fiscalyear_last_month
        now = datetime.now()
        if now < datetime.strptime(
                "%s-%s-%s" % (now.year, fiscal_month, fiscal_day),
                DEFAULT_SERVER_DATE_FORMAT
        ):
            temp = datetime.strptime(
                "%s-%s-%s" % (now.year - 1, fiscal_month, fiscal_day),
                DEFAULT_SERVER_DATE_FORMAT
            )
        else:
            temp = datetime.strptime(
                "%s-%s-%s" % (now.year, fiscal_month, fiscal_day),
                DEFAULT_SERVER_DATE_FORMAT
            )
        return str(temp + timedelta(days=1))

    @api.model
    def _default_end_date(self):
        fiscal_day = self.env.user.company_id.fiscalyear_last_day
        fiscal_month = self.env.user.company_id.fiscalyear_last_month
        now = datetime.now()
        if now < datetime.strptime(
                "%s-%s-%s" % (now.year, fiscal_month, fiscal_day),
                DEFAULT_SERVER_DATE_FORMAT
        ):
            temp = datetime.strptime(
                "%s-%s-%s" % (now.year, fiscal_month, fiscal_day),
                DEFAULT_SERVER_DATE_FORMAT
            )
        else:
            temp = datetime.strptime(
                "%s-%s-%s" % (now.year + 1, fiscal_month, fiscal_day),
                DEFAULT_SERVER_DATE_FORMAT
            )
        return str(temp)

    practical_amount = fields.Float(compute='_compute_practical_amount', string='Practical Amount', digits=0)
    different_amount = fields.Float(compute='_compute_different_amount', string='Different Amount', digits=0)

    def _compute_different_amount(self):
        for line in self:
            line.different_amount = line.x_studio_field_Gs0md - line.practical_amount

    def _compute_practical_amount(self):
        for line in self:
            aml_obj = self.env['account.move.line']
            domain = [('account_id', '=',
                line.account_id.id),
                ('date', '>=', line.start_date),
                ('date', '<=', line.end_date)
                ]
            where_query = aml_obj._where_calc(domain)
            aml_obj._apply_ir_rules(where_query, 'read')
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            select = "SELECT sum(debit)-sum(credit) from " + from_clause + " where " + where_clause
            self.env.cr.execute(select, where_clause_params)
            line.practical_amount = self.env.cr.fetchone()[0] or 0.0
