# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2018 brain-tec AG (http://www.braintec-group.com)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, exceptions, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import logging
_logger = logging.getLogger(__name__)

class Budget(models.Model):

    _name = "budgetextension.budget"
    _description = _("Account Budget for a fiscal year")
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = "end_date desc"

    @api.model
    def _default_start_date(self):
        fiscal_day = self.env.user.company_id.fiscalyear_last_day
        fiscal_month = self.env.user.company_id.fiscalyear_last_month
        now = datetime.now()
        if self._context.get('params',{}).get('action')==1397: #Future
            year = now.year +1
        else:
            year = now.year
        if now < datetime.strptime(
                "%s-%s-%s" % (now.year, fiscal_month, fiscal_day),
                DEFAULT_SERVER_DATE_FORMAT
        ):
            temp = datetime.strptime(
                "%s-%s-%s" % (year - 1, fiscal_month, fiscal_day),
                DEFAULT_SERVER_DATE_FORMAT
            )
        else:
            temp = datetime.strptime(
                "%s-%s-%s" % (year, fiscal_month, fiscal_day),
                DEFAULT_SERVER_DATE_FORMAT
            )
        return str(temp + timedelta(days=1))

    @api.model
    def _default_end_date(self):
        fiscal_day = self.env.user.company_id.fiscalyear_last_day
        fiscal_month = self.env.user.company_id.fiscalyear_last_month
        now = datetime.now()
        if self._context.get('params',{}).get('action')==1397: #Future
            year = now.year +1
        else:
            year = now.year
        if now < datetime.strptime(
                "%s-%s-%s" % (now.year, fiscal_month, fiscal_day),
                DEFAULT_SERVER_DATE_FORMAT
        ):
            temp = datetime.strptime(
                "%s-%s-%s" % (year, fiscal_month, fiscal_day),
                DEFAULT_SERVER_DATE_FORMAT
            )
        else:
            temp = datetime.strptime(
                "%s-%s-%s" % (year + 1, fiscal_month, fiscal_day),
                DEFAULT_SERVER_DATE_FORMAT
            )
        return str(temp)

    name = fields.Char(string="Budget Name", required=True,
                       help="Required to distinguish the budgets")
    active = fields.Boolean(default=True, index=True)
    account_id = fields.Many2one(comodel_name='account.account', string="Account",
                                 index=True, required=True)
    start_date = fields.Date(string="Start Date",
                             default=_default_start_date, required=True,
                             help="Start date of period")
    end_date = fields.Date(string="End Date",
                           default=_default_end_date, required=True,
                           help="End date of period")
    planned_amount = fields.Float(
        string="Planned Amount", digits=0, required=True, track_visibility="onchange")

    planned_amount_100 = fields.Float(
        string="Planned Amount (100)", digits=0, required=True, track_visibility="onchange")
    ccm_budget_percent = fields.Integer(
        string="CCM Budget Percent", default='85', track_visibility="onchange")
    proposed_amount = fields.Float(compute='_compute_proposed_amount', string="Proposed Amount", digits=0,
                                   required=True, track_visibility="onchange")
    percentage = fields.Float(string="Percentage", digits=0,
                              required=True, track_visibility="onchange")
    duration_days = fields.Integer(readonly=True,
                                   compute='_compute_duration_days')
    practical_amount = fields.Float(compute='_compute_planned_amount',
                                    string='Practical Amount',  digits=0, track_visibility="onchange")

    different_amount = fields.Float(compute='_compute_planned_amount',
                                    string='Remaining Balance', digits=0, track_visibility="onchange")

    state = fields.Selection(selection=[('1', _("past")),
                                        ('2', _("present")),
                                        ('3', _("future"))],
                             compute='_compute_state',
                             store=True,
                             default='2')

    account_type = fields.Selection(
        string="Type", related="account_id.account_type")
    x_studio_type = fields.Selection(
        string="Type", related="account_id.account_type")
    group_id = fields.Many2one('budgetextension.grouping', string="Grouping",
                               store=True)

    last_2_year_variance_amount = fields.Float(
        compute="_compute_last2year_planned_amount", string="Last 2 Year Variance", digits=0, track_visibility="onchange")
    last_2_year_planned_amount = fields.Float(
        compute="_compute_last2year_planned_amount", string="Last 2 Year Planned Amount", digits=0, track_visibility="onchange")
    last_2_year_practical_amount = fields.Float(
        compute="_compute_last2year_planned_amount", string="Last 2 Year Practical Amount", digits=0, track_visibility="onchange")
    last_year_planned_amount = fields.Float(
        compute="_compute_lastyear_planned_amount", string="Last Year Planned Amount", digits=0, track_visibility="onchange")
    last_year_variance_amount = fields.Float(
        compute="_compute_lastyear_planned_amount", string="Variance", digits=0, track_visibility="onchange")
    last_year_planned_amount_100 = fields.Float(
        compute="_compute_lastyear_planned_amount", string="Variance", digits=0, track_visibility="onchange")

    planned_amount_100_neg = fields.Float(
        string="Planned Amount [Negative]", compute="_compute_negative")

    # ADDED BY KMS
    planned_amount_revised = fields.Float(
        string="Planned Amount (Revised)", digits=0, track_visibility="onchange")
    planned_amount_revised_neg = fields.Float(
        string="Planned Amount (Revised) [Negative]", compute="_compute_negative")
    last_year_practical_amount = fields.Float(compute="_compute_lastyear_planned_amount",
                                              string="Last Year Practical Amount", digits=0, track_visibility="onchange")
    last_year_practical_amount_neg = fields.Float(
        string="Last Year Practical Amount [Negative]", compute="_compute_negative", digits=0, track_visibility="onchange")

    last_2_year_practical_amount_neg = fields.Float(
        compute="_compute_negative", string="Last 2 Year Practical Amount", digits=0, track_visibility="onchange")

    last_2_year_planned_amount_100 = fields.Float(compute="_compute_last2year_planned_amount",
                                                  string="Last 2 Year Planned Amount", digits=0, track_visibility="onchange")

    last_2_year_planned_amount_100_neg = fields.Float(
        compute="_compute_negative", string="Last 2 Year Practical Amount (Negative)", digits=0, track_visibility="onchange")

    budget_template = fields.Boolean(
        string="Budget Template", store=True, copy=False, default=False)

    tax_currency_rate = fields.Float(string="Tax Currency Rate", default=1450)
    
    ### Ohnmar
    no_overwrite = fields.Boolean('No Overwrite from Template',default=False,help="Normally Extended Budget is overwrited by Template Budget. If you want not to overwrite, make this checked on.")
    ### Ohnmar
    

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        res = super(Budget, self).read_group(domain, fields, groupby,
                                             offset=offset, limit=limit, orderby=orderby, lazy=lazy)
        for line in res:
            if '__domain' in line:
                lines = self.search(line['__domain'])
                total_last_practical = 0.0
                total_last_2_practical = 0.0
                total_last_2_planned_100 = 0.0
                total_planned_100 = 0.0
                total_planned_amount_revised = 0.0
                total_variance = 0.0
                for record in lines:
                    total_last_practical += record.last_year_practical_amount_neg
                    total_planned_100 += record.planned_amount_100_neg
                    total_last_2_practical += record.last_2_year_practical_amount_neg
                    total_last_2_planned_100 += record.last_2_year_planned_amount_100_neg
                    total_planned_amount_revised += record.planned_amount_revised_neg
                    total_variance += record.last_year_variance_amount
                line['last_year_practical_amount_neg'] = total_last_practical
                line['planned_amount_100_neg'] = total_planned_100
                line['last_2_year_practical_amount_neg'] = total_last_2_practical
                line['last_2_year_planned_amount_100_neg'] = total_last_2_planned_100
                line['planned_amount_revised_neg'] = total_planned_amount_revised
                line['last_year_variance_amount'] = total_variance
        return res

    @api.onchange('planned_amount_revised')
    def _compute_negative(self):
        for budget in self:
            if budget.account_id.account_type == 'Expenses':
                budget.planned_amount_revised_neg = budget.planned_amount_revised * -1
                budget.planned_amount_100_neg = budget.planned_amount_100 * -1
                budget.last_2_year_planned_amount_100_neg = budget.last_2_year_planned_amount_100 * -1
            else:
                budget.planned_amount_revised_neg = budget.planned_amount_revised
                budget.planned_amount_100_neg = budget.planned_amount_100
                budget.last_2_year_planned_amount_100_neg = budget.last_2_year_planned_amount_100

            budget.last_year_practical_amount_neg = budget.last_year_practical_amount * -1
            budget.last_2_year_practical_amount_neg = budget.last_2_year_practical_amount * -1

    def update_planned_amount(self):
        for record in self:
            record[("planned_amount")] = record.proposed_amount

    @api.onchange('percentage')
    def _compute_proposed_amount(self):
        for budget in self:
            last_budget = 0
            if budget.last_year_planned_amount:
                last_budget = budget.last_year_planned_amount
                percen = budget.percentage / 100
                budget.proposed_amount = last_budget + (last_budget * percen)
            else:
                budget.proposed_amount = 0

    @api.onchange('planned_amount_revised', 'planned_amount_100', 'ccm_budget_percent')
    def _compute_allowed_amount(self):
        for rec in self:
            calc = 0
            if rec.planned_amount_revised > 0:
                calc = rec.planned_amount_revised
                rec.planned_amount = calc
            else:
                calc = (rec.planned_amount_100 * rec.ccm_budget_percent) / 100
                rec.planned_amount = calc

    @api.onchange('start_date', 'end_date')
    @api.depends('account_id')
    def _compute_planned_amount(self):
        # warning_msg = []
        _logger.debug('######################### _compute_planned_amount START')
        for budget in self:
            # this year calculation
            # if not budget.account_id:
            # warning_msg.append("Please choose the account code first")
            # if warning_msg:
            # raise Warning(_(''.join(warning_msg)))
            """
            aml_obj = self.env['account.move.line']
            domain = [('account_id', '=',
                       budget.account_id.id),
                      ('date', '>=', budget.start_date),
                      ('date', '<=', budget.end_date)
                      ]
            where_query = aml_obj._where_calc(domain)
            aml_obj._apply_ir_rules(where_query, 'read')
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            # select = "SELECT sum(debit)-sum(credit) from " + \
            #     from_clause + " where " + where_clause
            """
            select = """
            SELECT sum(debit)-sum(credit) 
            from (select debit,credit,date,company_id,account_id,move_id from account_move_line where date >= 'from_date' and date <= 'to_date') aml
            left join account_move am on am.id=aml.move_id
            left join account_account acc on acc.id=aml.account_id
            where 
                acc.code = 'my_account_id' AND am.state='posted'
                AND  aml.date >= 'from_date'
                AND  aml.date <= 'to_date'
                AND 
                (
                    aml.company_id IS NULL 
                    OR  
                    (
                        my_company_id
                    )
                )
            """
            select = select.replace("my_account_id",str(budget.account_id.code))
            select = select.replace("from_date",str(budget.start_date))
            select = select.replace("to_date",str(budget.end_date))
            if str(budget.end_date)<='2022-06-30':
                select = select.replace("my_company_id","aml.company_id in (1)")
            else:
                select =  select.replace("my_company_id","aml.company_id in ("+str(budget.company_id.id)+")")
            self.env.cr.execute(select)
            practical_amount = self.env.cr.fetchone()[0] or 0
            budget.practical_amount = practical_amount
            budget.different_amount = budget.planned_amount - practical_amount
        _logger.debug('######################### _compute_planned_amount END')

    @api.onchange('start_date', 'end_date')
    @api.depends('account_id')
    def _compute_lastyear_planned_amount(self):
        _logger.debug('######################### _compute_lastyear_planned_amount START')
        for budget in self:
            # last year calculation
            start_date = budget.start_date + relativedelta(years=-1)
            end_date = budget.end_date + relativedelta(years=-1)
            # last_year_budget = self.sudo().search([('start_date', '=', start_date), (
            #     'end_date', '=', end_date), ('account_id', '=', budget.account_id.id)], limit=1)
            #last_year_budget = self.sudo().search([('start_date', '=', start_date), (
            #    'end_date', '=', end_date), ('account_id.code', '=', budget.account_id.code)], limit=1, order="id desc")
            last_year_budget = self.sudo().search_read([('start_date', '=', start_date), (
                'end_date', '=', end_date), ('account_id.code', '=', budget.account_id.code),('company_id','=',budget.company_id.id)],['planned_amount','planned_amount_100','practical_amount'], limit=1, order="id desc")
            if len(last_year_budget)>0:
                last_year_budget = last_year_budget[0]
            else:
                last_year_budget = {}
            budget.last_year_planned_amount = last_year_budget.get('planned_amount') or 0
            budget.last_year_planned_amount_100 = last_year_budget.get('planned_amount_100') or 0
            budget.last_year_practical_amount = last_year_budget.get('practical_amount') or 0
            budget.last_year_variance_amount = budget.planned_amount_100 - \
                (last_year_budget.get('planned_amount_100') or 0)
        _logger.debug('######################### _compute_lastyear_planned_amount END')

    @api.onchange('start_date', 'end_date')
    @api.depends('account_id')
    def _compute_last2year_planned_amount(self):
        _logger.debug('######################### _compute_last2year_planned_amount START')
        for budget in self:
            # 2 years ago calculations
            start_date = budget.start_date + relativedelta(years=-2)
            end_date = budget.end_date + relativedelta(years=-2)
            # last_2_year_budget = self.sudo().search([('start_date', '=', start_date), (
            #     'end_date', '=', end_date), ('account_id', '=', budget.account_id.id)], limit=1)
            if str(end_date)<='2022-06-30':
                if budget.company_id.id==4:
                    last_2_year_budget = self.sudo().search_read([('start_date', '=', start_date), (
                        'end_date', '=', end_date), ('account_id.code', '=', budget.account_id.code),('company_id','=',1)],['planned_amount','planned_amount_100','practical_amount'], limit=1, order="id desc")
                else:#to get Null
                    last_2_year_budget = self.sudo().search_read([('account_id.code', '=', budget.account_id.code),('account_id.code', '=', 'NULL')],['planned_amount','planned_amount_100','practical_amount'], limit=1, order="id desc")
            else:
                last_2_year_budget = self.sudo().search_read([('start_date', '=', start_date), (
                    'end_date', '=', end_date), ('account_id.code', '=', budget.account_id.code),('company_id','=',budget.company_id.id)],['planned_amount','planned_amount_100','practical_amount'], limit=1, order="id desc")
            if len(last_2_year_budget)>0:
                last_2_year_budget = last_2_year_budget[0]
            else:
                last_2_year_budget = {}
            budget.last_2_year_planned_amount = last_2_year_budget.get('planned_amount') or 0
            budget.last_2_year_practical_amount = last_2_year_budget.get('practical_amount') or 0
            budget.last_2_year_planned_amount_100 = last_2_year_budget.get('planned_amount_100') or 0

            # lastdomain = [('account_id', '=',
            #                budget.account_id.id),
            #               ('date', '>=', start_date),
            #               ('date', '<=', end_date)
            #               ]
            # lastwhere_query = aml_obj._where_calc(lastdomain)
            # aml_obj._apply_ir_rules(lastwhere_query, 'read')
            # from_clause, where_clause, where_clause_params = lastwhere_query.get_sql()
            # select = "SELECT sum(debit)-sum(credit) from " + \
            #     from_clause + " where " + where_clause
            # self.env.cr.execute(select, where_clause_params)
            
            # budget.last_2_year_variance_amount = last_2_year_budget.planned_amount - \
            #     budget.practical_amount
            budget.last_2_year_variance_amount = budget.planned_amount_100 - \
                (last_2_year_budget.get('planned_amount') or 0)
        _logger.debug('######################### _compute_last2year_planned_amount END')
            

    @api.depends('start_date', 'end_date')
    def _compute_duration_days(self):
        for record in self:
            ed = datetime.strptime(str(record.end_date), "%Y-%m-%d")
            sd = datetime.strptime(str(record.start_date), "%Y-%m-%d")
            record.duration_days = (ed - sd).days + 1

    @api.depends('end_date')
    def _compute_state(self):
        for record in self:
            end_date = datetime.strptime(str(record.end_date),
                                         DEFAULT_SERVER_DATE_FORMAT)
            fd = self.env.user.company_id.fiscalyear_last_day
            fm = self.env.user.company_id.fiscalyear_last_month
            now = datetime.now()
            e_fiscal_date = datetime.strptime(
                "%s-%s-%s" % (now.year, fm, fd),
                DEFAULT_SERVER_DATE_FORMAT
            )
            if now >= e_fiscal_date:
                e_fiscal_date = datetime.strptime(
                    "%s-%s-%s" % (now.year + 1, fm, fd),
                    DEFAULT_SERVER_DATE_FORMAT
                ) + timedelta(days=1)
            s_fiscal_date = datetime.strptime(
                "%s-%s-%s" % (e_fiscal_date.year - 1, fm, fd),
                DEFAULT_SERVER_DATE_FORMAT
            ) + timedelta(days=1)
            if end_date < s_fiscal_date:
                record.state = '1'
            elif end_date > e_fiscal_date:
                record.state = '3'
            else:
                record.state = '2'

    def copy(self, default=None):
        default = dict(default or {})
        name = self.name
        cc = self.search_count([('name', '=like', _("Copy of %s") % name)])
        if not cc:
            new_name = _("Copy of %s") % name
        else:
            new_name = _("Copy of %s (%r)") % (name, cc)
        default['name'] = new_name
        (default['start_date'],
         default['end_date']) = self._get_suggested_dates()

        return super(Budget, self).copy(default)

    @api.constrains('account_id', 'start_date', 'end_date')
    def _check_account_time_period(self):
        err_msg = ""
        for record in self:
            err_msg = self._get_error_message(record)
            if err_msg:
                raise exceptions.ValidationError(err_msg)

    @api.onchange('account_id')
    def _onchange_account_id(self):
        # if (
        #         self.account_id.id
        #         and self.account_id.id is not self._origin.account_id.id
        # ):
        #     (self.start_date,
        #      self.end_date) = self._get_suggested_dates()
        #     self.name = _("%s Budget %s") % (
        #         self.account_id.code,
        #         datetime.strptime(
        #             str(self.end_date),
        #             DEFAULT_SERVER_DATE_FORMAT
        #         ).year
        #     )
        if self.account_id:
            self.name = self.account_id.name

    # @api.onchange('name')
    # def _onchange_name(self):
    #     """Suggest an account for the budget"""
    #     if self.name:
    #         possible_accounts = self.name.split(" ")
    #         for possible_account in possible_accounts:
    #             if possible_account.isdigit():
    #                 new_acc = self.env["account.account"].search(
    #                     [('code', '=', possible_account)],
    #                     limit=1)
    #                 if new_acc:
    #                     self.account_id = new_acc
    #                     return

    def _cron_compute_state(self):
        res = self.search([('state', '!=', '1')])
        for record in res:
            record._compute_state()

    def _get_suggested_dates(self):
        temp_date = self.search([('account_id', '=', self.account_id.id)],
                                limit=1, order='end_date DESC').end_date
        if temp_date:
            latest_date = datetime.strptime(str(temp_date),
                                            DEFAULT_SERVER_DATE_FORMAT)
            fiscal_day = self.env.user.company_id.fiscalyear_last_day
            fiscal_month = self.env.user.company_id.fiscalyear_last_month
            e_fiscal_date = datetime.strptime(
                "%s-%s-%s" % (latest_date.year, fiscal_month, fiscal_day),
                DEFAULT_SERVER_DATE_FORMAT
            )
            if latest_date >= e_fiscal_date:
                e_fiscal_date = datetime.strptime(
                    "%s-%s-%s" % (latest_date.year + 1,
                                  fiscal_month,
                                  fiscal_day),
                    DEFAULT_SERVER_DATE_FORMAT
                )
            if latest_date + timedelta(days=2) > e_fiscal_date:
                latest_date += timedelta(days=2)
                start_date = latest_date
                end_date = datetime.strptime(
                    "%s-%s-%s" % (latest_date.year, fiscal_month, fiscal_day),
                    DEFAULT_SERVER_DATE_FORMAT
                )
            else:
                latest_date += timedelta(days=1)
                start_date = latest_date
                end_date = datetime.strptime(
                    "%s-%s-%s" % (latest_date.year, fiscal_month, fiscal_day),
                    DEFAULT_SERVER_DATE_FORMAT
                )
            return str(start_date), str(end_date)
        else:
            return self._default_start_date(), self._default_end_date()

    def _get_error_message(self, record):
        if record:
            date_from = datetime.strptime(str(record.start_date),
                                          DEFAULT_SERVER_DATE_FORMAT)
            date_to = datetime.strptime(str(record.end_date),
                                        DEFAULT_SERVER_DATE_FORMAT)
            fiscal_d = self.env.user.company_id.fiscalyear_last_day
            fiscal_m = self.env.user.company_id.fiscalyear_last_month
            e_fiscal_date = datetime.strptime(
                "%s-%s-%s" % (date_to.year, fiscal_m, fiscal_d),
                DEFAULT_SERVER_DATE_FORMAT
            )
            s_fiscal_date = datetime.strptime(
                "%s-%s-%s" % (date_to.year - 1, fiscal_m, fiscal_d),
                DEFAULT_SERVER_DATE_FORMAT
            )

            periods = self.search([('account_id', '=', record.account_id.id),
                                   ('start_date', '<=', record.end_date),
                                   ('end_date', '>=', record.start_date),
                                   ('id', '!=', record.id)])
            err_msg = []
            if (date_to > e_fiscal_date or
                    date_from < s_fiscal_date):
                err_msg.append(_("the year of the dates must be identical"))
            if date_from >= date_to:
                err_msg.append(_("the end date must be subsequent "
                                 "to the start date"))
            if len(periods) > 0:
                err_msg.append(_("the time period should be unique and "
                                 "shouldn't overlap another budget with the "
                                 "same account"))
            separator = _("and")
            if len(err_msg) is not 0:
                return (" \n%s " % separator).join(str(msg) for msg in err_msg)
            return ""
