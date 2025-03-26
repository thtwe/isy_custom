# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.api import Environment as env
from odoo.addons import decimal_precision as dp

# Capital Budget


class CapitalBudgetTemplate (models.Model):
    _name = "capital.budget.template"
    _description = "Capital Budget Template"

    name = fields.Char(string="Name", store=True, track_visibility="onchange")
    sequence = fields.Integer(string="Sequence", store=True)
    type_id = fields.Many2one('capital.budget.type',
                              string="Type", ondelete="cascade")
    capital_line_ids = fields.One2many(
        'capital.budget.line', 'capital_budget_id', string="Budget Lines")
    line_total = fields.Float(
        string="Line Total", compute='_compute_line_total', track_visibility="onchange")
    is_application = fields.Boolean(string="Application")
    application_fee = fields.Float(
        string="Application Fee", track_visibility="onchange")
    contingency_percentage = fields.Float(
        string="Contingency (%)", store=True, track_visibility="onchange")
    contingency_amount = fields.Float(
        string="Contingency Amount", compute='_compute_total', track_visibility="onchange")
    current_income = fields.Float(
        string="Current Income", compute='_compute_current_reserve', track_visibility="onchange")
    previous_income = fields.Float(
        string="Previous Income", store=True, track_visibility="onchange")
    from_date = fields.Date(string="From Date", store=True)
    to_date = fields.Date(string="To Date", store=True)
    is_reserve = fields.Boolean(string="Expense Reserve")
    current_year_reserve = fields.Float(
        string="Current Year Reserve", compute='_compute_current_reserve', track_visibility="onchange")
    is_enrollment = fields.Boolean(string="Enrollment")
    enrollment_fee = fields.Float(
        string="Enrollment Fee", store=True, track_visibility="onchange")
    last_year_planned_amount = fields.Float(
        string="Last Year Planned Amount", store=True, track_visibility="onchange")
    last_2_year_planned_amount = fields.Float(
        string="Last 2 Year Planned Amount", store=True, track_visibility="onchange")
    variance = fields.Float(
        string="Variance", compute='_compute_variance', track_visibility="onchange")
    variance_percentage = fields.Float(
        string="Variance (%)", compute='_compute_variance')
    planned_amount = fields.Float(
        string="Planned Amount", compute='_compute_total', track_visibility="onchange")

    # KMS Update
    planned_amount_neg = fields.Float(
        string="Planned Amount [Negative]", compute='compute_negative', track_visibility="onchange")
    last_year_planned_amount_neg = fields.Float(
        string="Last Year Planned Amount [Negative]", compute='compute_negative', store=True, track_visibility="onchange")
    last_2_year_planned_amount_neg = fields.Float(
        string="Last 2 Year Planned Amount [Negative]", compute='compute_negative', store=True, track_visibility="onchange")

    @api.depends('planned_amount', 'last_year_planned_amount', 'last_2_year_planned_amount')
    def compute_negative(self):
        for rec in self:
            if rec.type_id.is_expense:
                rec.planned_amount_neg = -(rec.planned_amount)
                rec.last_year_planned_amount_neg = -(rec.last_year_planned_amount)
                rec.last_2_year_planned_amount_neg = -(rec.last_2_year_planned_amount)
            else:
                rec.planned_amount_neg = rec.planned_amount
                rec.last_year_planned_amount_neg = rec.last_year_planned_amount
                rec.last_2_year_planned_amount_neg = rec.last_2_year_planned_amount

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        res = super(CapitalBudgetTemplate, self).read_group(domain, fields, groupby,
                                                            offset=offset, limit=limit, orderby=orderby, lazy=lazy)
        for line in res:
            if '__domain' in line:
                lines = self.search(line['__domain'])
                total_planned_amount = 0.0
                total_planned_amount_neg = 0.0
                total_last_year_planned_amount_neg = 0.0
                total_last_2_year_planned_amount_neg = 0.0
                total_variance = 0.0
                for record in lines:
                    total_planned_amount += record.planned_amount
                    total_planned_amount_neg += record.planned_amount_neg
                    total_last_year_planned_amount_neg += record.last_year_planned_amount_neg
                    total_last_2_year_planned_amount_neg += record.last_2_year_planned_amount_neg
                    total_variance += record.variance
                line['planned_amount'] = total_planned_amount
                line['planned_amount_neg'] = total_planned_amount_neg
                line['last_year_planned_amount_neg'] = total_last_year_planned_amount_neg
                line['last_year_2_planned_amount_neg'] = total_last_2_year_planned_amount_neg
                line['variance'] = total_variance
        return res
    #END

    @api.model
    def _default_tax_group(self):
        return self.env['ir.model.field'].search(['name', '=', 'application_fee'], limit=1)

    @api.depends('capital_line_ids.total')
    def _compute_line_total(self):
        for rec in self:
            calc = 0
            for line in rec.capital_line_ids:
                calc = calc + line.total
            rec.line_total = calc

    @api.depends('from_date', 'to_date', 'previous_income')
    def _compute_current_reserve(self):
        income = 0
        reserve = 0
        for rec in self:
            domain = [('start_date', '=', rec.from_date), ('end_date', '=', rec.to_date),
                      ('planned_amount_100', '!=', 0), ('account_type', '=', 'Income')]
            budget_id = self.env['budgetextension.budget'].search(domain)
            if budget_id:
                for budget in budget_id:
                    income = income + budget.planned_amount
                    rec.current_income = income
            reserve = (rec.current_income - rec.previous_income) * 0.2
            rec.current_year_reserve = reserve

    @api.depends('line_total', 'enrollment_fee', 'contingency_percentage', 'contingency_amount', 'current_year_reserve', 'application_fee')
    def _compute_total(self):
        calc = 0
        total = 0
        for rec in self:
            if rec.is_enrollment:
                calc = (rec.line_total * rec.enrollment_fee) * \
                    rec.contingency_percentage / 100
                rec.contingency_amount = calc
                total = (rec.line_total * rec.enrollment_fee) + \
                    rec.contingency_amount
                rec.planned_amount = total
            elif rec.is_reserve:
                calc = rec.current_year_reserve * rec.contingency_percentage / 100
                rec.contingency_amount = calc
                total = rec.current_year_reserve + rec.contingency_amount
                rec.planned_amount = total
            else:
                if rec.is_application:
                    calc = (rec.line_total * rec.application_fee) * \
                        rec.contingency_percentage / 100
                    rec.contingency_amount = calc
                    total = (rec.line_total * rec.application_fee) + \
                        rec.contingency_amount
                    rec.planned_amount = total
                else:
                    calc = (rec.line_total) * \
                        rec.contingency_percentage / 100
                    rec.contingency_amount = calc
                    total = rec.line_total + rec.contingency_amount
                    rec.planned_amount = total

    @api.depends('planned_amount', 'last_year_planned_amount')
    def _compute_variance(self):
        for rec in self:
            total = 0
            percent = 0
            total = rec.planned_amount - rec.last_year_planned_amount
            rec.variance = total
            if rec.last_year_planned_amount > 0:
                percent = (rec.planned_amount - rec.last_year_planned_amount) / \
                    rec.last_year_planned_amount * 100
            rec.variance_percentage = percent

# Capital Budget Line


class CapitalBudgetLine(models.Model):
    _name = "capital.budget.line"
    _description = _("Capital Budget Line")

    name = fields.Char(string="Name", store=True)
    total = fields.Float(string="Total", store=True,
                         track_visibility="onchange")
    capital_budget_id = fields.Many2one(
        'capital.budget.template', string="Capital Budget", ondelete="cascade")

# Capital Budget Type


class CapitalBudgetType(models.Model):
    _name = "capital.budget.type"
    _description = _("Capital Budget Type")

    name = fields.Char(string="name", store=True)

    # KMS Update
    is_expense = fields.Boolean(string="Expense", store=True, default=False)
    # END

# Revenue Budget (YGN)


class RevenueBudgetYgn(models.Model):
    _name = "revenue.budget.ygn"
    _inherit = ['mail.thread']
    _description = _("Revenue Budget (YGN)")

    budget_id = fields.Many2one(
        'budgetextension.budget', string="Budget Grade", ondelete="cascade")
    current_year_student = fields.Float(string="Current Year Student", digits=(
        12, 0), store=True, track_visibility="onchange")
    current_year_fee = fields.Float(
        string="Current Year Fee", store=True, track_visibility="onchange")
    current_year_total = fields.Float(
        string="Current Year Total", track_visibility="onchange", compute='_compute_current_total')
    percentage = fields.Float(string="Percentage (%)",
                              store=True, track_visibility="onchange")
    next_year_student = fields.Float(string="Next Year Student", digits=(
        12, 0), store=True, track_visibility="onchange")
    next_year_fee = fields.Float(
        string="Next Year Fee", compute='_compute_next_fee', track_visibility="onchange")
    next_year_total = fields.Float(
        string="Next Year Total", compute='_compute_next_total', track_visibility="onchange")

    @api.depends('current_year_student', 'current_year_fee')
    def _compute_current_total(self):
        calc = 0
        for rec in self:
            calc = rec.current_year_fee * rec.current_year_student
            rec.current_year_total = calc

    @api.depends('current_year_fee', 'percentage')
    def _compute_next_fee(self):
        calc = 0
        for rec in self:
            calc = rec.current_year_fee * rec.percentage / 100
            rec.next_year_fee = calc

    @api.depends('next_year_student', 'next_year_fee')
    def _compute_next_total(self):
        total = 0
        for rec in self:
            total = rec.next_year_fee * rec.next_year_student
            rec.next_year_total = total
            record = rec.env['budgetextension.budget'].search(
                [('id', '=', rec.budget_id.id),('no_overwrite','=',False)])
            if record:
                planned_amount = rec.next_year_total * record.ccm_budget_percent / 100
                record.write({
                    'planned_amount_100': rec.next_year_total,
                    'planned_amount': planned_amount})
                # record.write({'planned_amount_100': rec.next_year_total})

# Revenue Budget (NPT)


class RevenueBudgetNpt(models.Model):
    _name = "revenue.budget.npt"
    _inherit = ['mail.thread']
    _description = _("Revenue Budget (NPT)")

    name = fields.Char(string="Name", store=True)
    budget_id = fields.Many2one(
        'budgetextension.budget', string="Budget", ondelete="cascade")
    budget_amount = fields.Float(
        string="Budget Amount", related="budget_id.planned_amount_100", track_visibility="onchange")
    revenue_npt_line_ids = fields.One2many(
        'revenue.budget.npt.line', 'revenue_budget_npt_id', string="Revenue Lines")
    line_total = fields.Float(
        string="Line Total", compute='_compute_line_total', track_visibility="onchange")
    from_date = fields.Date(string="From Date", store=True)
    to_date = fields.Date(string="To Date", store=True)
    contingency_percentage = fields.Float(
        string="Contingency (%)", store=True, track_visibility="onchange")
    contingency_amount = fields.Float(
        string="Contingency Amount", compute="_compute_total", track_visibility="onchange")
    budget_total = fields.Float(
        string="Total", compute='_compute_total', track_visibility="onchange")

    @api.depends('revenue_npt_line_ids.total')
    def _compute_line_total(self):
        for rec in self:
            calc = 0
            for line in rec.revenue_npt_line_ids:
                calc = calc + line.total
            rec.line_total = calc

    @api.depends('line_total', 'contingency_percentage')
    def _compute_total(self):
        calc = 0
        total = 0
        for rec in self:
            calc = rec.line_total * rec.contingency_percentage / 100
            rec.contingency_amount = calc
            total = rec.line_total + rec.contingency_amount
            rec.budget_total = total
            record = rec.env['budgetextension.budget'].search(
                [('id', '=', rec.budget_id.id)])
            if record:
                record.write({'planned_amount_100': rec.budget_total})

# Revenue Budget (NPT) Line


class RevenueBudgetNptLine(models.Model):
    _name = "revenue.budget.npt.line"
    _inherit = ['mail.thread']
    _description = _("Revenue Budget (NPT) Line")

    name = fields.Char(string="Name", store=True)
    revenue_budget_npt_id = fields.Many2one(
        'revenue.budget.npt', string="Revenue Budget (NPT)", ondelete="cascade")
    student = fields.Float(string="Student", digits=(
        12, 0), store=True, track_visibility="onchange")
    fee = fields.Float(string="Fee", store=True, track_visibility="onchange")
    total = fields.Float(
        string="Total", compute='_compute_total', track_visibility="onchange")

    @api.depends('student', 'fee')
    def _compute_total(self):
        total = 0
        for rec in self:
            total = rec.student * rec.fee
            rec.total = total

# Payroll Budget


class PayrollBudget(models.Model):
    _name = "payroll.budget"
    _inherit = ['mail.thread']
    _description = _("Payroll Budget")

    name = fields.Char(string="Name", store=True)
    budget_id = fields.Many2one(
        'budgetextension.budget', string="Budget", ondelete="cascade")
    base_budget_amount = fields.Float(
        string="Base Budget Amount", compute='_compute_base_total', track_visibility="onchange")
    retirement_budget_id = fields.Many2one(
        'budgetextension.budget', string="Retirement Budget", ondelete="cascade")
    retirement_budget_amount = fields.Float(
        string="Retirement Amount", compute='_compute_retirement_total', track_visibility="onchange")
    gratuity_budget_id = fields.Many2one(
        'budgetextension.budget', string="Gratuity Budget", ondelete="cascade")
    gratuity_budget_amount = fields.Float(
        string="Gratuity Amount", compute='_compute_gratuity_total', track_visibility="onchange")
    provident_fund_budget_id = fields.Many2one(
        'budgetextension.budget', string="Provident Fund Budget", ondelete="cascade")
    provident_fund_budget_amount = fields.Float(
        string="Provident Fund Amount", compute='_compute_provident_fund_total', track_visibility="onchange")
    payroll_line_m_ids = fields.One2many(
        'payroll.budget.line.m', 'budget_id', string="Payroll Lines for Manipulation")
    contingency_percentage = fields.Float(
        string="Contingency (%)", store=True, track_visibility="onchange")
    contingency_amount = fields.Float(
        string="Contingency Amount", compute='_compute_base_total')
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")

    # MT Start
    gratuity_budget_percent = fields.Float(string="Gratuity Budget Percent (%)", digits=dp.get_precision(
        'budget_percent'), default=8.333, track_visibility="onchange")

    # MT End

    @api.depends('payroll_line_m_ids.next_year_base_additional', 'contingency_percentage')
    def _compute_base_total(self):
        for rec in self:
            base_total = 0
            contingency_amount = 0
            planned_amount_100 = 0
            planned_amount = 0
            for line in rec.payroll_line_m_ids:
                base_total = base_total + line.next_year_base_additional
            contingency_amount = base_total * rec.contingency_percentage / 100
            rec.contingency_amount = contingency_amount
            record = rec.env['budgetextension.budget'].search(
                [('id', '=', rec.budget_id.id),('no_overwrite','=',False)])
            planned_amount_100 = base_total + rec.contingency_amount
            if record:
                planned_amount = planned_amount_100 * record.ccm_budget_percent / 100
                record.write({
                    'planned_amount_100': planned_amount_100,
                    'planned_amount': planned_amount})
            rec.base_budget_amount = planned_amount_100

    @api.depends('payroll_line_m_ids.next_year_provident_fund')
    def _compute_provident_fund_total(self):
        for rec in self:
            planned_amount_100 = 0
            planned_amount = 0
            for line in rec.payroll_line_m_ids:
                planned_amount_100 = planned_amount_100 + line.next_year_provident_fund
            record = rec.env['budgetextension.budget'].search(
                    [('id', '=', rec.provident_fund_budget_id.id),('no_overwrite','=',False)])
            if record:
                planned_amount = planned_amount_100 * record.ccm_budget_percent / 100
                record.write({
                    'planned_amount_100': planned_amount_100,
                    'planned_amount': planned_amount})
            rec.provident_fund_budget_amount = planned_amount_100

    @api.depends('payroll_line_m_ids.next_year_retirement')
    def _compute_retirement_total(self):
        for rec in self:
            planned_amount_100 = 0
            planned_amount = 0
            record = rec.env['budgetextension.budget'].search(
                    [('id', '=', rec.retirement_budget_id.id),('no_overwrite','=',False)])
            for line in rec.payroll_line_m_ids:
                planned_amount_100 = planned_amount_100 + line.next_year_retirement
                
            if record and not rec.mt_new_feature:
                planned_amount = planned_amount_100 * record.ccm_budget_percent / 100
                record.write({
                    'planned_amount_100': planned_amount_100,
                    'planned_amount': planned_amount})
            rec.retirement_budget_amount = planned_amount_100

    @api.depends('payroll_line_m_ids.next_year_base_additional', 'payroll_line_m_ids.next_year_allowance')
    def _compute_gratuity_total(self):
        for rec in self:
            base_total = 0
            allowance_total = 0
            planned_amount_100 = 0
            planned_amount = 0
            for line in rec.payroll_line_m_ids:
                if line.employee_type == 'local' and line.employee_id:
                    base_total = base_total + line.next_year_base_additional
                    allowance_total = allowance_total + line.next_year_allowance
            record = rec.env['budgetextension.budget'].search(
                [('id', '=', rec.gratuity_budget_id.id),('no_overwrite','=',False)])
            if record:
                planned_amount_100 = (
                    base_total + allowance_total) * 8.333 / 100
                planned_amount = planned_amount_100 * record.ccm_budget_percent / 100
                record.write({
                    'planned_amount_100': planned_amount_100,
                    'planned_amount': planned_amount})
            rec.gratuity_budget_amount = planned_amount_100

# Payroll Budget Line for Manipulation


class PayrollBudgetLineForManipulation(models.Model):
    _name = "payroll.budget.line.m"
    _description = _("Payroll Budget Line for Manipulation")

    employee = fields.Char(string="Employee", store=True)
    position = fields.Char(string="Position", store=True)
    employee_type = fields.Selection(
        [('local', 'Local'), ('expatriate', 'Expatriate')], string="Type")
    budget_id = fields.Many2one(
        'payroll.budget', string="Budget", ondelete="cascade")
    current_year_base = fields.Float(
        string="Current Year Base", store=True, track_visibility="onchange")
    retirement_percentage = fields.Float(
        string="Retirement %", store=True,  track_visibility="onchange")
    provident_fund_percentage = fields.Float(
        string="Provident Fund %", store=True,  track_visibility="onchange")
    current_year_retirement = fields.Float(
        string="Current Year Retirement", compute='_compute_current_year_retirement',  track_visibility="onchange")
    current_year_provident_fund = fields.Float(
        string="Current Year Provident Fund", compute='_compute_current_year_provident_fund',  track_visibility="onchange")
    current_year_budget = fields.Float(
        string="Current Year Budget", compute='_compute_current_year_budget',  track_visibility="onchange")
    inflation = fields.Float(
        string="Inflation", store=True,  track_visibility="onchange")
    next_year_origin = fields.Float(
        string="Next Year Origin",  track_visibility="onchange")
    next_year_base = fields.Float(
        string="Next Year Retirement", compute='_compute_next_year_base', track_visibility="onchange")
    additional_stipend = fields.Float(
        string="Additional Stipend", store=True,  track_visibility="onchange")
    next_year_base_additional = fields.Float(
        string="Next Year Base Additional", compute='_compute_next_year_base_additional',  track_visibility="onchange")
    next_year_retirement = fields.Float(
        string="Next Year Retirement", compute='_compute_next_year_retirement',  track_visibility="onchange")
    next_year_provident_fund = fields.Float(
        string="Next Year Provident Fund", compute='_compute_next_year_provident_fund',  track_visibility="onchange")
    next_year_budget = fields.Float(
        string="Next Year Budget", compute='_compute_next_year_budget',  track_visibility="onchange")
    variance = fields.Float(
        string="Variance", compute='_compute_variance',  track_visibility="onchange")

    # KMS Update
    current_year_tax_amount = fields.Float(
        string='Current Year Tax Amount', store=True)
    current_year_allowance = fields.Float(
        string='Current Year Allowance', store=True)
    current_year_net_budget = fields.Float(
        string='Current Year Net Budget', compute='_compute_current_year_net_budget', track_visibility="onchange")
    # END

    # mt
    employee_id = fields.Many2one('hr.employee', string="Employee(Tax)")
    next_year_allowance = fields.Float(
        string="Next Year Allowance", compute='_compute_next_year_allowance', track_visibility="onchange")
    next_year_gratuity_m = fields.Float(
        string="Next Year Gratuity", compute='_compute_next_year_gratuity_m', track_visibility="onchange")
    next_year_tax_amount = fields.Float(
        string="Next Year Tax Amount", compute='_compute_next_year_tax_amount', track_visibility="onchange")
    next_year_net_income = fields.Float(
        string="Next Year Net Income", compute='_compute_next_year_net_income', track_visibility="onchange")
    next_year_net_income_provident_fund = fields.Float(
        string="Next Year Net Income (Provident Fund)", compute='_compute_next_year_net_income_provident_fund', track_visibility="onchange")
    gratuity_budget_line_percent = fields.Float(string="Gratuity Budget Percent (%)", digits=dp.get_precision(
        'budget_percent'), default=8.333, track_visibility="onchange")

    #############################################################
    # MT Develop

    @api.onchange('employee_id')
    def onchange_employee(self):
        if self.employee_id:
            self.employee = self.employee_id.name
        else:
            self.employee = ''

    @api.depends('next_year_allowance', 'next_year_gratuity_m', 'next_year_base')
    def _compute_next_year_net_income(self):
        for rec in self:
            if rec.budget_id.state == '2' and rec.employee_id and rec.employee_type == 'local':
                rec.next_year_net_income = (
                    rec.next_year_base + rec.next_year_allowance + rec.next_year_gratuity_m) - rec.next_year_tax_amount
            else:
                rec.next_year_net_income = 0

    @api.depends('next_year_net_income', 'next_year_provident_fund')
    def _compute_next_year_net_income_provident_fund(self):
        for rec in self:
            if rec.employee_id and rec.employee_type == 'local':
                rec.next_year_net_income_provident_fund = rec.next_year_net_income + \
                    rec.next_year_provident_fund
            else:
                rec.next_year_net_income_provident_fund =0

    # tax calculation -> total sum of ( next_year_base + next_year_allowance + next_year_gratuity_m)
    @api.depends('next_year_base', 'employee_id', 'next_year_allowance', 'next_year_gratuity_m')
    def _compute_next_year_tax_amount(self):
        for rec in self:
            if rec.budget_id.state == '2' and rec.employee_id and rec.employee_type == 'local':
                to_calc_tax_amount_usd = rec.next_year_base + \
                    rec.next_year_allowance + rec.next_year_gratuity_m
                to_calc_tax_amount_mmk = to_calc_tax_amount_usd * \
                    rec.budget_id.budget_id.tax_currency_rate

                personal_relief_mmk = to_calc_tax_amount_mmk * 0.20
                print(rec.employee)
                print("Personal Relief")
                print(personal_relief_mmk)
                if rec.employee_id.marital == 'married':
                    spouse_relief_mmk = 1000000.00
                else:
                    spouse_relief_mmk = 0.00
                print("Spouse Relief")
                print(spouse_relief_mmk)

                if rec.employee_id.x_studio_registered_parent:
                    parent_relief_mmk = 1000000.00 * \
                        int(rec.employee_id.x_studio_registered_parent)
                else:
                    parent_relief_mmk = 0.00

                print("Parent Relief")
                print(parent_relief_mmk)

                if rec.employee_id.children:
                    child_reflief_mmk = 500000.00 * \
                        int(rec.employee_id.children)
                else:
                    child_reflief_mmk = 0.00

                print("Children Relief")
                print(child_reflief_mmk)

                total_allowance_deduction = personal_relief_mmk + \
                    spouse_relief_mmk + parent_relief_mmk + child_reflief_mmk

                taxable_amount = to_calc_tax_amount_mmk - \
                    total_allowance_deduction  # 58500000.00
                # taxable_amount=12,105,908.24

                accumulative_tax = 0
                taxable_income = 0
                Flag = False
                if taxable_amount >= 2000000:
                    taxable_income += 2000000
                    accumulative_tax += 0
                else:
                    Flag = True
                    rec.next_year_tax_amount = 0
                # correct
                print("< 2000000")
                print(accumulative_tax)
                if Flag == False:
                    if (taxable_amount - taxable_income) >= 3000000:
                        taxable_income += 3000000
                        accumulative_tax += 3000000 * 0.05

                        print("< 5000000")
                        print(3000000 * 0.05)
                    else:
                        taxable_income = taxable_amount - taxable_income
                        accumulative_tax += taxable_income * 0.05
                        Flag = True
                        print("< 5000000")
                        print(taxable_income * 0.05)
                    if Flag == False:
                        if (taxable_amount - taxable_income) >= 5000000:
                            taxable_income += 5000000
                            accumulative_tax += 5000000 * 0.1
                            print("< 10000000")
                            print(5000000 * 0.1)
                        else:
                            taxable_income = taxable_amount - taxable_income
                            accumulative_tax += taxable_income * 0.1
                            Flag = True
                            print("< 10000000")
                            print(taxable_income * 0.1)

                        if Flag == False:
                            if (taxable_amount - taxable_income) >= 10000000:
                                taxable_income += 10000000
                                accumulative_tax += 10000000 * 0.15
                                print("< 20000000")
                                print(10000000 * 0.15)
                            else:
                                taxable_income = taxable_amount - taxable_income
                                accumulative_tax += taxable_income * 0.15
                                Flag = True
                                print("< 20000000")
                                print(taxable_income * 0.15)
                            if Flag == False:
                                if (taxable_amount - taxable_income) >= 10000000:
                                    taxable_income += 10000000
                                    accumulative_tax += 10000000 * 0.20
                                    print("< 30000000")
                                    print(10000000 * 0.20)
                                    Flag = True
                                else:
                                    taxable_income = taxable_amount - taxable_income
                                    accumulative_tax += taxable_income * 0.20
                                    print("< 30000000")
                                    print(taxable_income * 0.20)
                                if Flag == True:
                                    taxable_income = taxable_amount - taxable_income
                                    accumulative_tax += taxable_income * 0.25

                                    print("> 30000000")
                                    print(taxable_income * 0.25)
                    rec.next_year_tax_amount = accumulative_tax / \
                        rec.budget_id.budget_id.tax_currency_rate
            else:
                rec.next_year_tax_amount = 0

    @api.depends('next_year_base_additional', 'next_year_allowance', 'budget_id', 'gratuity_budget_line_percent')
    def _compute_next_year_gratuity_m(self):
        for rec in self:
            if rec.budget_id.mt_new_feature == True:
                rec.next_year_gratuity_m = rec.next_year_base * (
                    rec.gratuity_budget_line_percent / 100)
            else:
                if rec.employee_type == 'local' and rec.employee_id:
                    rec.next_year_gratuity_m = (rec.next_year_allowance + rec.next_year_base_additional) * (
                        rec.budget_id.gratuity_budget_percent / 100)
                else:
                    rec.next_year_gratuity_m = 0

    @api.depends('employee_id')
    def _compute_next_year_allowance(self):
        # import pdb
        # pdb.set_trace()
        for rec in self:
            next_year_allowance = 0
            if rec.budget_id.budget_id and rec.budget_id.state == '2' and rec.employee_type == 'local' and rec.employee_id:
                obj_allowance_budget = self.env['allowance.budget'].search(
                    [('parent_budget_id', '=', rec.budget_id.budget_id.id)])
                for obj in obj_allowance_budget:
                    next_year_allowance += obj.allowance
            rec.next_year_allowance = next_year_allowance
    # MT Develop End
    #############################################################

    # KMS Update
    @api.onchange('current_year_budget', 'current_year_allowance')
    def _compute_current_year_net_budget(self):
        calc = 0
        for rec in self:
            if rec.employee_type == 'local':
                calc = rec.current_year_budget + \
                    (rec.current_year_budget * 8.333 / 100) + \
                    rec.current_year_allowance
                rec.current_year_net_budget = calc
            else:
                rec.current_year_net_budget = 0

    @api.onchange('employee_type')
    def reset_to_zero(self):
        for rec in self:
            if rec.employee_type == 'local':
                rec.write({'retirement_percentage': 0.0})
            else:
                rec.write({
                      'provident_fund_percentage': 0.0,
                      'current_year_tax_amount': 0.0,
                      'current_year_allowance': 0.0})
    # END

    @api.depends('current_year_base', 'retirement_percentage')
    def _compute_current_year_retirement(self):
        calc = 0
        for rec in self:
            calc = rec.current_year_base * rec.retirement_percentage / 100
            rec.current_year_retirement = calc

    @api.depends('current_year_base', 'provident_fund_percentage')
    def _compute_current_year_provident_fund(self):
        calc = 0
        for rec in self:
            calc = rec.current_year_base * rec.provident_fund_percentage / 100
            rec.current_year_provident_fund = calc

    @api.depends('current_year_base', 'current_year_retirement', 'current_year_provident_fund')
    def _compute_current_year_budget(self):
        calc = 0
        for rec in self:
            if rec.employee_type == 'local':
                calc = rec.current_year_base + rec.current_year_provident_fund
                rec.current_year_budget = calc
            else:
                calc = rec.current_year_base + rec.current_year_retirement
                rec.current_year_budget = calc
                
    # KMS Update (29/9/2020)
    #'next_year_origin',
    @api.depends('inflation')
    def _compute_next_year_base(self):
        calc = 0
        for rec in self:
            if rec.budget_id.mt_new_feature == True:
                calc = rec.current_year_base + \
                    (rec.current_year_base * rec.inflation / 100)
                rec.next_year_base = calc
            else:
                calc = rec.next_year_origin + \
                        (rec.next_year_origin * rec.inflation / 100)
                rec.next_year_base = calc
    # END

    @api.depends('next_year_base', 'additional_stipend')
    def _compute_next_year_base_additional(self):
        calc = 0        
        for rec in self:
            if rec.budget_id.mt_new_feature == True:
                rec.next_year_base_additional = rec.next_year_base
            else:
                calc = rec.next_year_base + \
                    (rec.next_year_base * rec.additional_stipend / 100)
                rec.next_year_base_additional = calc

    @api.depends('next_year_base', 'retirement_percentage')
    def _compute_next_year_retirement(self):
        calc = 0
        for rec in self:
            calc = rec.next_year_base * rec.retirement_percentage / 100
            rec.next_year_retirement = calc

    @api.depends('next_year_base', 'next_year_allowance', 'provident_fund_percentage')
    def _compute_next_year_provident_fund(self):
        calc = 0
        for rec in self:
            if rec.budget_id.mt_new_feature == True:
                if rec.employee_id and rec.employee_type == 'local':
                    calc = (rec.next_year_base) * \
                        rec.provident_fund_percentage / 100
                    rec.next_year_provident_fund = calc
                else:
                    rec.next_year_provident_fund = 0
            else:

                if rec.employee_id and rec.employee_type == 'local':
                    calc = (rec.next_year_base + rec.next_year_allowance) * \
                        rec.provident_fund_percentage / 100
                    rec.next_year_provident_fund = calc
                else:
                    rec.next_year_provident_fund = 0

    @api.depends('next_year_base_additional', 'next_year_provident_fund', 'next_year_retirement')
    def _compute_next_year_budget(self):
        calc = 0
        for rec in self:
            if rec.budget_id.mt_new_feature == True:
                if rec.employee_type == 'local':
                    calc = rec.next_year_base + rec.next_year_gratuity_m + rec.next_year_provident_fund + (rec.next_year_base * (rec.additional_stipend/100))
                    rec.next_year_budget = calc
                else:
                    calc = rec.next_year_base + rec.next_year_gratuity_m + \
                        (rec.next_year_base * (rec.additional_stipend/100))
                    rec.next_year_budget = calc
            else:
                if rec.employee_type == 'local':
                    calc = rec.next_year_base_additional + rec.next_year_provident_fund + \
                        rec.next_year_allowance + rec.next_year_gratuity_m
                    rec.next_year_budget = calc
                else:
                    calc = rec.next_year_base_additional + rec.next_year_retirement
                    rec.next_year_budget = calc
        
    # KMS Update
    @api.depends('next_year_budget', 'next_year_tax_amount', 'current_year_net_budget', 'current_year_tax_amount')
    def _compute_variance(self):
        calc = 0
        for rec in self:
            if rec.budget_id.mt_new_feature == True:
                calc = rec.next_year_base - rec.current_year_base
                rec.variance = calc
            else:
                if rec.employee_type == 'local':
                    calc = ((rec.next_year_budget - rec.next_year_tax_amount) -
                            (rec.current_year_net_budget - rec.current_year_tax_amount))
                    rec.variance = calc
                else:
                    rec.variance = 0
    # END

# Allowance Budget Template


class AllowanceBudget(models.Model):
    _name = "allowance.budget"
    _inherit = ['mail.thread']
    _description = _("Allowace Budget")

    budget_id = fields.Many2one('budgetextension.budget',
                                string="Budget", ondelete="cascade")
    parent_budget_id = fields.Many2one('budgetextension.budget',
                                       string="Parent Budget", ondelete="cascade")

    employee_count = fields.Integer(
        string="Employee Count", store=True,  track_visibility="onchange")
    allowance = fields.Float(
        string="Allowance", store=True,  track_visibility="onchange")
    total = fields.Float(
        string="Total", compute='_calc_allowance',  track_visibility="onchange")

    @api.depends('employee_count', 'allowance')
    def _calc_allowance(self):
        calc = 0
        for rec in self:
            calc = rec.employee_count * rec.allowance
            rec.total = calc
            record = rec.env['budgetextension.budget'].search(
                [('id', '=', rec.budget_id.id),('no_overwrite','=',False)])
            if record:
                record.write({'planned_amount_100': rec.total})

# Payroll Budget Line (Master)


class PayrollBudgetLineMaster(models.Model):
    _name = "payroll.budget.line.master"
    _inherit = ['mail.thread']
    _description = _("Payroll Budget Line (Master)")

    employee_id = fields.Many2one(
        'hr.employee', string="Employee", ondelete="cascade")
    position = fields.Char(string="Position")  # related="employee_id.x_job"
    employee_type = fields.Selection(
        [('local', 'Local'), ('expatriate', 'Expatriate')], string="Type")
    budget_id = fields.Many2one(
        'payroll.budget', string="Budget", ondelete="cascade")
    current_year_base = fields.Float(
        string="Current Year Base", compute="_get_base",  track_visibility="onchange")
    gratuity_percentage = fields.Float(
        string="Gratuity Percentage", store=True,  track_visibility="onchange")
    current_year_gratuity = fields.Float(
        string="Current Year Grauity", compute='_compute_current_year_gratuity', track_visibility="onchange")
    current_year_budget = fields.Float(
        string="Current Year Budget", compute='_compute_current_year_budget', track_visibility="onchange")
    inflation = fields.Float(
        string="Inflation", store=True, track_visibility="onchange")
    next_year_base = fields.Float(
        string="Next Year Base", compute='_compute_next_year_base', track_visibility="onchange")
    additional_stipend = fields.Float(
        string="Additional Stipend", store=True, track_visibility="onchange")
    next_year_base_additional = fields.Float(
        string="Next Year Base Additional", compute='_compute_next_year_base_additional', track_visibility="onchange")
    next_year_gratuity = fields.Float(
        string="Next Year Gratuity", compute='_compute_next_year_gratuity', track_visibility="onchange")
    next_year_budget = fields.Float(
        string="Next Year Budget", compute='_compute_next_year_budget', track_visibility="onchange")
    variance = fields.Float(
        string="Variance", compute='_compute_variance', track_visibility="onchange")

    @api.depends('employee_id')
    def _get_base(self):
        for rec in self:
            if rec.employee_id:
                contract = self.env['hr.contract'].search(
                    ['&', ('employee_id.id', '=', rec.employee_id.id), ('state', '=', 'open')])
                if contract:
                    rec.current_year_base = contract.wage

    @api.depends('current_year_base', 'gratuity_percentage')
    def _compute_current_year_gratuity(self):
        calc = 0
        for rec in self:
            calc = rec.current_year_base * rec.gratuity_percentage / 100
            rec.current_year_gratuity = calc

    @api.depends('current_year_base', 'current_year_gratuity')
    def _compute_current_year_budget(self):
        calc = 0
        for rec in self:
            calc = rec.current_year_base + rec.current_year_gratuity
            rec.current_year_budget = calc

    @api.depends('current_year_base', 'inflation')
    def _compute_next_year_base(self):
        calc = 0
        for rec in self:
            calc = rec.current_year_base + \
                (rec.current_year_base * rec.inflation / 100)
            rec.next_year_base = calc

    @api.depends('next_year_base', 'additional_stipend')
    def _compute_next_year_base_additional(self):
        calc = 0
        for rec in self:
            calc = rec.next_year_base + \
                (rec.next_year_base * rec.additional_stipend / 100)
            rec.next_year_base_additional = calc

    @api.depends('next_year_base', 'gratuity_percentage')
    def _compute_next_year_gratuity(self):
        calc = 0
        for rec in self:
            calc = rec.next_year_base * rec.gratuity_percentage / 100
            rec.next_year_gratuity = calc

    @api.depends('next_year_base_additional', 'next_year_gratuity')
    def _compute_next_year_budget(self):
        calc = 0
        for rec in self:
            calc = rec.next_year_base_additional + rec.next_year_gratuity
            rec.next_year_budget = calc

    @api.depends('current_year_budget', 'next_year_budget')
    def _compute_variance(self):
        calc = 0
        for rec in self:
            calc = rec.next_year_budget - rec.current_year_budget
            rec.variance = calc

# Rental Budget


class RentalBudget(models.Model):
    _name = 'rental.budget'
    _inherit = ['mail.thread']
    _description = _('Rental Budget')

    name = fields.Char(string="Name", store=True)
    budget_id = fields.Many2one('budgetextension.budget', string="Budget")
    budget_amount = fields.Float(
        string="Budget Amount", related="budget_id.planned_amount_100", track_visibility="onchange")
    rental_line_ids = fields.One2many(
        'rental.budget.line', 'rental_budget_id', string="Rental Lines")
    from_date = fields.Date(string="From Date", store=True)
    to_date = fields.Date(string="To Date", store=True)
    line_annual_total = fields.Float(
        string="Line Annual Total", compute='_compute_annual_total', track_visibility="onchange")
    contingency_percentage = fields.Float(
        string="Contingency (%)", store=True, track_visibility="onchange")
    contingency_amount = fields.Float(
        string="Contingeny Amount", compute='_compute_total', track_visibility="onchange")
    budget_total = fields.Float(
        string="Total", compute='_compute_total', track_visibility="onchange")
    acutal_rent_total = fields.Float(
        string="Actual Rent Total", compute='_compute_actual_rent', track_visibility="onchange")

    @api.depends('rental_line_ids.annual_allowance')
    def _compute_annual_total(self):
        for rec in self:
            total = 0
            for line in rec.rental_line_ids:
                total = total + line.annual_allowance
            rec.line_annual_total = total

    @api.depends('rental_line_ids.actual_monthly_rent')
    def _compute_actual_rent(self):
        for rec in self:
            total = 0
            for line in rec.rental_line_ids:
                total = total + line.actual_monthly_rent
            rec.acutal_rent_total = total

    @api.depends('line_annual_total', 'contingency_percentage')
    def _compute_total(self):
        calc = 0
        total = 0
        for rec in self:
            calc = rec.line_annual_total * rec.contingency_percentage / 100
            rec.contingency_amount = calc
            total = rec.line_annual_total + rec.contingency_amount
            rec.budget_total = total
            record = rec.env['budgetextension.budget'].search(
                [('id', '=', rec.budget_id.id),('no_overwrite','=',False)])
            if record:
                planned_amount = rec.budget_total * record.ccm_budget_percent / 100
                record.write({
                    'planned_amount_100': rec.budget_total,
                    'planned_amount': planned_amount})

                # record.write({'planned_amount_100': rec.budget_total})


# Rental Budget Line
class RentalBudgetLine(models.Model):
    _name = 'rental.budget.line'
    _description = _('Rental Budget Line')

    employee_id = fields.Many2one(
        'hr.employee', string="Employee", ondelete="cascade")
    categ_id = fields.Many2one(
        'rental.budget.category', string="Rental Category", ondelete="cascade")
    monthly_allowance = fields.Float(
        string="Monthly Allowance", related="categ_id.monthly_allowance", track_visibility="onchange")
    annual_allowance = fields.Float(
        string="Annual Allowance", compute='_compute_annual', track_visibility="onchange")
    actual_monthly_rent = fields.Float(
        string="Actual Monthly Rent", store=True, track_visibility="onchange")
    rental_budget_id = fields.Many2one(
        'rental.budget', string="Rental Budget", ondelete="cascade")

    @api.depends('monthly_allowance')
    def _compute_annual(self):
        calc = 0
        for rec in self:
            calc = rec.monthly_allowance * 12
            rec.annual_allowance = calc

# Rental Budget Category


class RentalCategory(models.Model):
    _name = 'rental.budget.category'
    _description = _('Rental Budget Category')

    name = fields.Char(string="Name", store=True)
    monthly_allowance = fields.Float(
        string="Monthly Allowance", store=True, track_visibility="onchange")
