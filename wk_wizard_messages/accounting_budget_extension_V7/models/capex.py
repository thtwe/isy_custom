# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Capex(models.Model):
    _name = 'budget.capex'
    _inherit = ['mail.thread']
    _description = _('Capex Report')

    name = fields.Char(string="Name", store=True)
    sequence = fields.Integer(string="Sequence", store=True)
    capex_type_id = fields.Many2one(
        'budget.capex.type', string="Type", ondelete="cascade")
    budget_total = fields.Float(
        string="Budget", store=True, track_visibility="onchange")
    actual_total = fields.Float(
        string="Actual", compute='_compute_total', store=True, track_visibility="onchange")
    percentage = fields.Float(
        string="%", compute='_compute_total', track_visibility="onchange")
    jul_line_ids = fields.One2many(
        'capex.july.line', 'capex_id', string="July")
    aug_line_ids = fields.One2many(
        'capex.august.line', 'capex_id', string="August")
    sep_line_ids = fields.One2many(
        'capex.september.line', 'capex_id', string="September")
    oct_line_ids = fields.One2many(
        'capex.october.line', 'capex_id', string="October")
    nov_line_ids = fields.One2many(
        'capex.november.line', 'capex_id', string="November")
    dec_line_ids = fields.One2many(
        'capex.december.line', 'capex_id', string="December")
    jan_line_ids = fields.One2many(
        'capex.january.line', 'capex_id', string="January")
    feb_line_ids = fields.One2many(
        'capex.february.line', 'capex_id', string="February")
    mar_line_ids = fields.One2many(
        'capex.march.line', 'capex_id', string="March")
    apr_line_ids = fields.One2many(
        'capex.april.line', 'capex_id', string="April")
    may_line_ids = fields.One2many(
        'capex.may.line', 'capex_id', string="May")
    jun_line_ids = fields.One2many(
        'capex.june.line', 'capex_id', string="June")
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


class CapexType(models.Model):
    _name = 'budget.capex.type'
    _description = _('Capex Type')
    _default = 'sequence asc'

    name = fields.Char(string='Name', store=True)
    sequence = fields.Integer(string="Sequence")


class CapexJulyLine(models.Model):
    _name = 'capex.july.line'
    _inherit = ['mail.thread']
    _description = _('Capex July')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    capex_id = fields.Many2one('budget.capex', string="Capex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")

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


class CapexAugustLine(models.Model):
    _name = 'capex.august.line'
    _inherit = ['mail.thread']
    _description = _('Capex August')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    capex_id = fields.Many2one('budget.capex', string="Capex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")

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


class CapexSeptemberLine(models.Model):
    _name = 'capex.september.line'
    _inherit = ['mail.thread']
    _description = _('Capex September')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    capex_id = fields.Many2one('budget.capex', string="Capex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")

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


class CapexOctoberLine(models.Model):
    _name = 'capex.october.line'
    _inherit = ['mail.thread']
    _description = _('Capex October')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    capex_id = fields.Many2one('budget.capex', string="Capex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")

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


class CapexNovemberLine(models.Model):
    _name = 'capex.november.line'
    _inherit = ['mail.thread']
    _description = _('Capex November')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    capex_id = fields.Many2one('budget.capex', string="Capex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")

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


class CapexDecemberLine(models.Model):
    _name = 'capex.december.line'
    _inherit = ['mail.thread']
    _description = _('Capex December')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    capex_id = fields.Many2one('budget.capex', string="Capex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")

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


class CapexJanuaryLine(models.Model):
    _name = 'capex.january.line'
    _inherit = ['mail.thread']
    _description = _('Capex January')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    capex_id = fields.Many2one('budget.capex', string="Capex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")

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


class CapexFebruaryLine(models.Model):
    _name = 'capex.february.line'
    _inherit = ['mail.thread']
    _description = _('Capex February')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    capex_id = fields.Many2one('budget.capex', string="Capex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")

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


class CapexMarchLine(models.Model):
    _name = 'capex.march.line'
    _inherit = ['mail.thread']
    _description = _('Capex March')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    capex_id = fields.Many2one('budget.capex', string="Capex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")

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


class CapexAprilLine(models.Model):
    _name = 'capex.april.line'
    _inherit = ['mail.thread']
    _description = _('Capex April')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    capex_id = fields.Many2one('budget.capex', string="Capex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")

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


class CapexMayLine(models.Model):
    _name = 'capex.may.line'
    _inherit = ['mail.thread']
    _description = _('Capex May')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    capex_id = fields.Many2one('budget.capex', string="Capex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")

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


class CapexJuneLine(models.Model):
    _name = 'capex.june.line'
    _inherit = ['mail.thread']
    _description = _('Capex June')

    account_id = fields.Many2one(
        'account.account', string="Account", ondelete="cascade")
    capex_id = fields.Many2one('budget.capex', string="Capex")
    from_date = fields.Date(string="From Date", track_visibility="onchange")
    to_date = fields.Date(string="To Date", track_visibility="onchange")
    type_id = fields.Selection(string="Type", related="account_id.account_type")
    actual_amount = fields.Float(
        string="Actual", compute="_compute_actual", track_visibility="onchange")

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
