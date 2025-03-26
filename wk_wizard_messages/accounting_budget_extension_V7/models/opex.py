# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Opex(models.Model):
    _name = 'budget.opex'
    _inherit = ['mail.thread']
    _description = _('Opex Report')

    name = fields.Char(string="Name", store=True)
    sequence = fields.Integer(string="Sequence", store=True)
    opex_type_id = fields.Many2one(
        'budget.opex.type', string="Type", ondelete="cascade")
    budget_total = fields.Float(
        string="Budget", compute='_compute_budget', store=True, track_visibility="onchange")
    actual_total = fields.Float(
        string="Actual", compute='_compute_total', store=True, track_visibility="onchange")
    percentage = fields.Float(
        string="%", compute='_compute_total', track_visibility="onchange")
    jul_line_ids = fields.One2many('opex.july.line', 'opex_id', string="July")
    aug_line_ids = fields.One2many(
        'opex.august.line', 'opex_id', string="August")
    sep_line_ids = fields.One2many(
        'opex.september.line', 'opex_id', string="September")
    oct_line_ids = fields.One2many(
        'opex.october.line', 'opex_id', string="October")
    nov_line_ids = fields.One2many(
        'opex.november.line', 'opex_id', string="November")
    dec_line_ids = fields.One2many(
        'opex.december.line', 'opex_id', string="December")
    jan_line_ids = fields.One2many(
        'opex.january.line', 'opex_id', string="January")
    feb_line_ids = fields.One2many(
        'opex.february.line', 'opex_id', string="February")
    mar_line_ids = fields.One2many(
        'opex.march.line', 'opex_id', string="March")
    apr_line_ids = fields.One2many(
        'opex.april.line', 'opex_id', string="April")
    may_line_ids = fields.One2many(
        'opex.may.line', 'opex_id', string="May")
    jun_line_ids = fields.One2many(
        'opex.june.line', 'opex_id', string="June")
    jul_total = fields.Float(
        string="JUL", compute='_compute_actual', store=True, track_visibility="onchange")
    aug_total = fields.Float(
        string="AUG", compute='_compute_actual', store=True, track_visibility="onchange")
    sep_total = fields.Float(
        string="SEP", compute='_compute_actual', store=True, track_visibility="onchange")
    oct_total = fields.Float(
        string="OCT", compute='_compute_actual', store=True, track_visibility="onchange")
    nov_total = fields.Float(
        string="NOV", compute='_compute_actual', store=True, track_visibility="onchange")
    dec_total = fields.Float(
        string="DEC", compute='_compute_actual', store=True, track_visibility="onchange")
    jan_total = fields.Float(
        string="JAN", compute='_compute_actual', store=True, track_visibility="onchange")
    feb_total = fields.Float(
        string="FEB", compute='_compute_actual', store=True, track_visibility="onchange")
    mar_total = fields.Float(
        string="MAR", compute='_compute_actual', store=True, track_visibility="onchange")
    apr_total = fields.Float(
        string="APR", compute='_compute_actual', store=True, track_visibility="onchange")
    may_total = fields.Float(
        string="MAY", compute='_compute_actual', store=True, track_visibility="onchange")
    jun_total = fields.Float(
        string="JUN", compute='_compute_actual', store=True, track_visibility="onchange")
    from_date = fields.Date(
        string="From", store=True, copy=False, required=True
    )
    to_date = fields.Date(
        string="To", store=True, copy=False, required=True
    )

    @api.depends('jul_line_ids.budget_amount')
    def _compute_budget(self):
        for rec in self:
            budget = 0
            for line in rec.jul_line_ids:
                budget = budget + line.budget_amount
                if rec.opex_type_id.name == "Expenses":
                    calc = -(budget / 1000)
                else:
                    calc = budget / 1000
                rec.budget_total = calc

    @api.depends('jul_line_ids.actual_amount', 'aug_line_ids.actual_amount', 'sep_line_ids.actual_amount', 'oct_line_ids.actual_amount', 'nov_line_ids.actual_amount', 'dec_line_ids.actual_amount', 'jan_line_ids.actual_amount', 'feb_line_ids.actual_amount', 'mar_line_ids.actual_amount', 'apr_line_ids.actual_amount', 'may_line_ids.actual_amount', 'jun_line_ids.actual_amount')
    def _compute_actual(self):
        for rec in self:
            jul = 0
            for line in rec.jul_line_ids:
                jul = jul + line.actual_amount
                calc = jul / 1000
                rec.jul_total = round(calc)
            aug = 0
            for line in rec.aug_line_ids:
                aug = aug + line.actual_amount
                calc = aug / 1000
                rec.aug_total = round(calc)
            sep = 0
            for line in rec.sep_line_ids:
                sep = sep + line.actual_amount
                calc = sep / 1000
                rec.sep_total = round(calc)
            oct = 0
            for line in rec.oct_line_ids:
                oct = oct + line.actual_amount
                calc = oct / 1000
                rec.oct_total = round(calc)
            nov = 0
            for line in rec.nov_line_ids:
                nov = nov + line.actual_amount
                calc = nov / 1000
                rec.nov_total = round(calc)
            dec = 0
            for line in rec.dec_line_ids:
                dec = dec + line.actual_amount
                calc = dec / 1000
                rec.dec_total = round(calc)
            jan = 0
            for line in rec.jan_line_ids:
                jan = jan + line.actual_amount
                calc = jan / 1000
                rec.jan_total = round(calc)
            feb = 0
            for line in rec.feb_line_ids:
                feb = feb + line.actual_amount
                calc = feb / 1000
                rec.feb_total = round(calc)
            mar = 0
            for line in rec.mar_line_ids:
                mar = mar + line.actual_amount
                calc = mar / 1000
                rec.mar_total = round(calc)
            apr = 0
            for line in rec.apr_line_ids:
                apr = apr + line.actual_amount
                calc = apr / 1000
                rec.apr_total = round(calc)
            may = 0
            for line in rec.may_line_ids:
                may = may + line.actual_amount
                calc = may / 1000
                rec.may_total = round(calc)
            jun = 0
            for line in rec.jun_line_ids:
                jun = jun + line.actual_amount
                calc = jun / 1000
                rec.jun_total = round(calc)

    @api.depends('jul_total', 'aug_total', 'sep_total', 'oct_total', 'nov_total', 'dec_total', 'jan_total', 'feb_total', 'mar_total', 'apr_total', 'may_total', 'jun_total')
    def _compute_total(self):
        total = 0
        for rec in self:
            total = rec.jul_total + rec.aug_total + rec.sep_total + rec.oct_total + \
                rec.nov_total + rec.dec_total + rec.jan_total + rec.feb_total + \
                rec.mar_total + rec.apr_total + rec.may_total + rec.jun_total
            rec.actual_total = total
        percentage = 0
        if rec.budget_total > 0:
            percentage = rec.actual_total / rec.budget_total * 100
            rec.percentage = percentage
        elif rec.budget_total < 0:
            percentage = (-rec.actual_total) / (-rec.budget_total) * 100
            rec.percentage = percentage


class OpexType(models.Model):
    _name = 'budget.opex.type'
    _description = _('Opex Type')
    _default = 'sequence asc'

    name = fields.Char(string='Name', store=True)
    sequence = fields.Integer(string="Sequence")


class OpexJulyLine(models.Model):
    _name = 'opex.july.line'
    _inherit = ['mail.thread']
    _description = _('Opex July')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    budget_id = fields.Many2one('budgetextension.budget', string="Budget")
    opex_id = fields.Many2one('budget.opex', string="Opex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")
    budget_amount = fields.Float(
        string="Budget", related="budget_id.planned_amount", track_visibility="onchange")

    @api.depends('from_date', 'to_date', 'account_id')
    def _compute_actual(self):
        actual = 0
        for rec in self:
            line_obj = self.env['account.move.line']
            domain = [('account_id', '=', rec.account_id.id), ('date',
                                                               '>=', rec.from_date), ('date', '<=', rec.to_date)]
            where_query = line_obj._where_calc(domain)
            line_obj._apply_ir_rules(where_query, 'read')
            from_clause,  where_clause, where_clause_params = where_query.get_sql()
            select = "SELECT sum(credit)-sum(debit) from " + \
                from_clause + " where " + where_clause
            self.env.cr.execute(select, where_clause_params)
            actual = self.env.cr.fetchone()[0] or 0.0
            rec.actual_amount = actual


class OpexAugustLine(models.Model):
    _name = 'opex.august.line'
    _inherit = ['mail.thread']
    _description = _('Opex August')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    budget_id = fields.Many2one('budgetextension.budget', string="Budget")
    opex_id = fields.Many2one('budget.opex', string="Opex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")
    budget_amount = fields.Float(
        string="Budget", related="budget_id.planned_amount", track_visibility="onchange")

    @api.depends('from_date', 'to_date', 'account_id')
    def _compute_actual(self):
        actual = 0
        for rec in self:
            line_obj = self.env['account.move.line']
            domain = [('account_id', '=', rec.account_id.id), ('date',
                                                               '>=', rec.from_date), ('date', '<=', rec.to_date)]
            where_query = line_obj._where_calc(domain)
            line_obj._apply_ir_rules(where_query, 'read')
            from_clause,  where_clause, where_clause_params = where_query.get_sql()
            select = "SELECT sum(credit)-sum(debit) from " + \
                from_clause + " where " + where_clause
            self.env.cr.execute(select, where_clause_params)
            actual = self.env.cr.fetchone()[0] or 0.0
            rec.actual_amount = actual


class OpexSeptemberLine(models.Model):
    _name = 'opex.september.line'
    _inherit = ['mail.thread']
    _description = _('Opex September')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    budget_id = fields.Many2one('budgetextension.budget', string="Budget")
    opex_id = fields.Many2one('budget.opex', string="Opex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")
    budget_amount = fields.Float(
        string="Budget", related="budget_id.planned_amount", track_visibility="onchange")

    @api.depends('from_date', 'to_date', 'account_id')
    def _compute_actual(self):
        actual = 0
        for rec in self:
            line_obj = self.env['account.move.line']
            domain = [('account_id', '=', rec.account_id.id), ('date',
                                                               '>=', rec.from_date), ('date', '<=', rec.to_date)]
            where_query = line_obj._where_calc(domain)
            line_obj._apply_ir_rules(where_query, 'read')
            from_clause,  where_clause, where_clause_params = where_query.get_sql()
            select = "SELECT sum(credit)-sum(debit) from " + \
                from_clause + " where " + where_clause
            self.env.cr.execute(select, where_clause_params)
            actual = self.env.cr.fetchone()[0] or 0.0
            rec.actual_amount = actual


class OpexOctoberLine(models.Model):
    _name = 'opex.october.line'
    _inherit = ['mail.thread']
    _description = _('Opex October')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    budget_id = fields.Many2one('budgetextension.budget', string="Budget")
    opex_id = fields.Many2one('budget.opex', string="Opex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")
    budget_amount = fields.Float(
        string="Budget", related="budget_id.planned_amount", track_visibility="onchange")

    @api.depends('from_date', 'to_date', 'account_id')
    def _compute_actual(self):
        actual = 0
        for rec in self:
            line_obj = self.env['account.move.line']
            domain = [('account_id', '=', rec.account_id.id), ('date',
                                                               '>=', rec.from_date), ('date', '<=', rec.to_date)]
            where_query = line_obj._where_calc(domain)
            line_obj._apply_ir_rules(where_query, 'read')
            from_clause,  where_clause, where_clause_params = where_query.get_sql()
            select = "SELECT sum(credit)-sum(debit) from " + \
                from_clause + " where " + where_clause
            self.env.cr.execute(select, where_clause_params)
            actual = self.env.cr.fetchone()[0] or 0.0
            rec.actual_amount = actual


class OpexNovemberLine(models.Model):
    _name = 'opex.november.line'
    _inherit = ['mail.thread']
    _description = _('Opex November')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    budget_id = fields.Many2one('budgetextension.budget', string="Budget")
    opex_id = fields.Many2one('budget.opex', string="Opex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")
    budget_amount = fields.Float(
        string="Budget", related="budget_id.planned_amount", track_visibility="onchange")

    @api.depends('from_date', 'to_date', 'account_id')
    def _compute_actual(self):
        actual = 0
        for rec in self:
            line_obj = self.env['account.move.line']
            domain = [('account_id', '=', rec.account_id.id), ('date',
                                                               '>=', rec.from_date), ('date', '<=', rec.to_date)]
            where_query = line_obj._where_calc(domain)
            line_obj._apply_ir_rules(where_query, 'read')
            from_clause,  where_clause, where_clause_params = where_query.get_sql()
            select = "SELECT sum(credit)-sum(debit) from " + \
                from_clause + " where " + where_clause
            self.env.cr.execute(select, where_clause_params)
            actual = self.env.cr.fetchone()[0] or 0.0
            rec.actual_amount = actual


class OpexDecemberLine(models.Model):
    _name = 'opex.december.line'
    _inherit = ['mail.thread']
    _description = _('Opex December')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    budget_id = fields.Many2one('budgetextension.budget', string="Budget")
    opex_id = fields.Many2one('budget.opex', string="Opex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")
    budget_amount = fields.Float(
        string="Budget", related="budget_id.planned_amount", track_visibility="onchange")

    @api.depends('from_date', 'to_date', 'account_id')
    def _compute_actual(self):
        actual = 0
        for rec in self:
            line_obj = self.env['account.move.line']
            domain = [('account_id', '=', rec.account_id.id), ('date',
                                                               '>=', rec.from_date), ('date', '<=', rec.to_date)]
            where_query = line_obj._where_calc(domain)
            line_obj._apply_ir_rules(where_query, 'read')
            from_clause,  where_clause, where_clause_params = where_query.get_sql()
            select = "SELECT sum(credit)-sum(debit) from " + \
                from_clause + " where " + where_clause
            self.env.cr.execute(select, where_clause_params)
            actual = self.env.cr.fetchone()[0] or 0.0
            rec.actual_amount = actual


class OpexJanuaryLine(models.Model):
    _name = 'opex.january.line'
    _inherit = ['mail.thread']
    _description = _('Opex January')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    budget_id = fields.Many2one('budgetextension.budget', string="Budget")
    opex_id = fields.Many2one('budget.opex', string="Opex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")
    budget_amount = fields.Float(
        string="Budget", related="budget_id.planned_amount", track_visibility="onchange")

    @api.depends('from_date', 'to_date', 'account_id')
    def _compute_actual(self):
        actual = 0
        for rec in self:
            line_obj = self.env['account.move.line']
            domain = [('account_id', '=', rec.account_id.id), ('date',
                                                               '>=', rec.from_date), ('date', '<=', rec.to_date)]
            where_query = line_obj._where_calc(domain)
            line_obj._apply_ir_rules(where_query, 'read')
            from_clause,  where_clause, where_clause_params = where_query.get_sql()
            select = "SELECT sum(credit)-sum(debit) from " + \
                from_clause + " where " + where_clause
            self.env.cr.execute(select, where_clause_params)
            actual = self.env.cr.fetchone()[0] or 0.0
            rec.actual_amount = actual


class OpexFebruaryLine(models.Model):
    _name = 'opex.february.line'
    _inherit = ['mail.thread']
    _description = _('Opex February')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    budget_id = fields.Many2one('budgetextension.budget', string="Budget")
    opex_id = fields.Many2one('budget.opex', string="Opex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")
    budget_amount = fields.Float(
        string="Budget", related="budget_id.planned_amount", track_visibility="onchange")

    @api.depends('from_date', 'to_date', 'account_id')
    def _compute_actual(self):
        actual = 0
        for rec in self:
            line_obj = self.env['account.move.line']
            domain = [('account_id', '=', rec.account_id.id), ('date',
                                                               '>=', rec.from_date), ('date', '<=', rec.to_date)]
            where_query = line_obj._where_calc(domain)
            line_obj._apply_ir_rules(where_query, 'read')
            from_clause,  where_clause, where_clause_params = where_query.get_sql()
            select = "SELECT sum(credit)-sum(debit) from " + \
                from_clause + " where " + where_clause
            self.env.cr.execute(select, where_clause_params)
            actual = self.env.cr.fetchone()[0] or 0.0
            rec.actual_amount = actual


class OpexMarchLine(models.Model):
    _name = 'opex.march.line'
    _inherit = ['mail.thread']
    _description = _('Opex March')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    budget_id = fields.Many2one('budgetextension.budget', string="Budget")
    opex_id = fields.Many2one('budget.opex', string="Opex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")
    budget_amount = fields.Float(
        string="Budget", related="budget_id.planned_amount", track_visibility="onchange")

    @api.depends('from_date', 'to_date', 'account_id')
    def _compute_actual(self):
        actual = 0
        for rec in self:
            line_obj = self.env['account.move.line']
            domain = [('account_id', '=', rec.account_id.id), ('date',
                                                               '>=', rec.from_date), ('date', '<=', rec.to_date)]
            where_query = line_obj._where_calc(domain)
            line_obj._apply_ir_rules(where_query, 'read')
            from_clause,  where_clause, where_clause_params = where_query.get_sql()
            select = "SELECT sum(credit)-sum(debit) from " + \
                from_clause + " where " + where_clause
            self.env.cr.execute(select, where_clause_params)
            actual = self.env.cr.fetchone()[0] or 0.0
            rec.actual_amount = actual


class OpexAprilLine(models.Model):
    _name = 'opex.april.line'
    _inherit = ['mail.thread']
    _description = _('Opex April')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    budget_id = fields.Many2one('budgetextension.budget', string="Budget")
    opex_id = fields.Many2one('budget.opex', string="Opex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")
    budget_amount = fields.Float(
        string="Budget", related="budget_id.planned_amount", track_visibility="onchange")

    @api.depends('from_date', 'to_date', 'account_id')
    def _compute_actual(self):
        actual = 0
        for rec in self:
            line_obj = self.env['account.move.line']
            domain = [('account_id', '=', rec.account_id.id), ('date',
                                                               '>=', rec.from_date), ('date', '<=', rec.to_date)]
            where_query = line_obj._where_calc(domain)
            line_obj._apply_ir_rules(where_query, 'read')
            from_clause,  where_clause, where_clause_params = where_query.get_sql()
            select = "SELECT sum(credit)-sum(debit) from " + \
                from_clause + " where " + where_clause
            self.env.cr.execute(select, where_clause_params)
            actual = self.env.cr.fetchone()[0] or 0.0
            rec.actual_amount = actual


class OpexMayLine(models.Model):
    _name = 'opex.may.line'
    _inherit = ['mail.thread']
    _description = _('Opex May')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    budget_id = fields.Many2one('budgetextension.budget', string="Budget")
    opex_id = fields.Many2one('budget.opex', string="Opex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")
    budget_amount = fields.Float(
        string="Budget", related="budget_id.planned_amount", track_visibility="onchange")

    @api.depends('from_date', 'to_date', 'account_id')
    def _compute_actual(self):
        actual = 0
        for rec in self:
            line_obj = self.env['account.move.line']
            domain = [('account_id', '=', rec.account_id.id), ('date',
                                                               '>=', rec.from_date), ('date', '<=', rec.to_date)]
            where_query = line_obj._where_calc(domain)
            line_obj._apply_ir_rules(where_query, 'read')
            from_clause,  where_clause, where_clause_params = where_query.get_sql()
            select = "SELECT sum(credit)-sum(debit) from " + \
                from_clause + " where " + where_clause
            self.env.cr.execute(select, where_clause_params)
            actual = self.env.cr.fetchone()[0] or 0.0
            rec.actual_amount = actual


class OpexJuneLine(models.Model):
    _name = 'opex.june.line'
    _inherit = ['mail.thread']
    _description = _('Opex June')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    budget_id = fields.Many2one('budgetextension.budget', string="Budget")
    opex_id = fields.Many2one('budget.opex', string="Opex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")
    budget_amount = fields.Float(
        string="Budget", related="budget_id.planned_amount", track_visibility="onchange")

    @api.depends('from_date', 'to_date', 'account_id')
    def _compute_actual(self):
        actual = 0
        for rec in self:
            line_obj = self.env['account.move.line']
            domain = [('account_id', '=', rec.account_id.id), ('date',
                                                               '>=', rec.from_date), ('date', '<=', rec.to_date)]
            where_query = line_obj._where_calc(domain)
            line_obj._apply_ir_rules(where_query, 'read')
            from_clause,  where_clause, where_clause_params = where_query.get_sql()
            select = "SELECT sum(credit)-sum(debit) from " + \
                from_clause + " where " + where_clause
            self.env.cr.execute(select, where_clause_params)
            actual = self.env.cr.fetchone()[0] or 0.0
            rec.actual_amount = actual
