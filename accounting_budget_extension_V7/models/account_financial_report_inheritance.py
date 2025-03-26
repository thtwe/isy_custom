# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2018 brain-tec AG (http://www.braintec-group.com)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################
import copy
from . import static
from datetime import datetime, timedelta
from odoo import fields, models, api, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, float_is_zero


class AccountReportExtension(models.AbstractModel):
    """Adds the handling if the filter is set to budget_comparison"""
    _inherit = "account.financial.html.report"

    def _apply_date_filter(self, options):
        """Adds new lines to the periods"""
        super(AccountReportExtension, self)._apply_date_filter(options)
        res = options
        cmp_filter = options['comparison'].get('filter', False)
        if res and cmp_filter == 'budget_comparison':
            dt_to = options['date'].get('date_to', False)
            if dt_to:
                columns = [_("Budget Theoretical Amount"),
                           _("Budget Set Amount"),
                           _("Budget Difference"),
                           "%"]
                res['comparison']['number_period'] = len(columns)
                res['comparison']['periods'] = []
                dt_from = False
                if options['date'].get('date_from'):
                    date_from = options['date'].get('date_from')
                    dt_from = datetime.strptime(date_from, "%Y-%m-%d")
                dt_to = datetime.strptime(dt_to, "%Y-%m-%d")
                if dt_from:
                    bid = 1
                    for column in columns:
                        dt_f_s = dt_from.strftime(DEFAULT_SERVER_DATE_FORMAT)
                        dt_t_s = dt_to.strftime(DEFAULT_SERVER_DATE_FORMAT)
                        vals = {'date_from': dt_f_s,
                                'date_to': dt_t_s,
                                'string': column,
                                'budget_id': bid
                                }
                        res['comparison']['periods'].append(vals)
                        bid += 1
                else:
                    for column in columns:
                        dt_t_s = dt_to.strftime(DEFAULT_SERVER_DATE_FORMAT)
                        vals = {'date': dt_t_s, 'string': column}
                        res['comparison']['periods'].append(vals)
                res['comparison']['string'] = 'Budget Comparison'
            else:
                res['comparison']['number_period'] = 0
                res['comparison']['periods'] = []
        return res


class FinancialReportExtensionCalculation(models.Model):
    _inherit = 'account.financial.html.report.line'

    def _get_lines(self, financial_report, currency_table, options, linesdicts):
        """Overriden default function which returns the data of the report

        Returns
        ----------
        list
            List with all the calculated data of the report
        """
        budget_codes = {}
        to_calc = []
        return self.ext_get_lines(financial_report, currency_table, options,
                                  linesdicts, budget_codes, to_calc)

    def ext_get_lines(self, financial_report, currency_table, options,
                      linesdicts, budget_codes, to_calc):
        """Calculates the data of the report with or without budget filter

        Returns
        ----------
        final_result_table : list
            List with all the calculated data of the report
        """
        final_result_table = []
        comparison_table = [options.get('date')]
        comparison_table += (options.get('comparison')
                             and options['comparison'].get('periods', [])
                             or [])
        currency_precision = self.env.user.company_id.currency_id.rounding
        rfilter = options['comparison'].get('filter', False)

        # build comparison table
        for line in self:
            res = []
            debit_credit = len(comparison_table) == 1
            domain_ids = {'line'}
            k = 0

            # Studer Nicola Extension
            if rfilter == 'budget_comparison':
                # List of all account ids found by the _eval_formula method
                acc_ids = None
                # Dictionary with the budgets amounts of an account
                budget_theoretical_amounts = {}
                # Dictionary with the balances of all accounts
                budget_origin_amounts = {}
                for period in comparison_table:
                    date_from = period.get('date_from', False)
                    date_to = (period.get('date_to', False)
                               or period.get('date', False))
                    date_from, date_to, strict_range = line.with_context(
                        date_from=date_from,
                        date_to=date_to)._compute_date_range()

                    # Check if the period is a period of the module extension
                    # Declaration of the budget_id:
                    #   budget_id = 1 <-- Budget Theoretical Amount
                    #   budget_id = 2 <-- Budget Set Amount
                    #   budget_id = 3 <-- Budget Difference

                    if (not budget_codes.get(line.code, False)
                            and line.formulas):
                        budget_codes.update({(line.code
                                              if line.code else 'stni_no_code'
                                              ): [0.0, 0.0, 0.0, 0.0]})

                    budget_id = period.get('budget_id', False)
                    if budget_id and acc_ids is not None and date_from:
                        if budget_id != 3 and budget_id != 4:
                            r = line.with_context(
                                date_from=date_from,
                                date_to=date_to,
                                strict_range=strict_range,
                            )._eval_formula_budget(
                                acc_ids,
                                budget_id)
                            budget_codes[(line.code
                                          if line.code else 'stin_no_code'
                                          )][budget_id-1] = (
                                r['line']['balance'])
                            if budget_id == 1:
                                budget_theoretical_amounts = r
                        else:
                            res_diff = {}
                            balance = 0
                            for key in acc_ids:
                                if str(key).isdigit():
                                    bb = (budget_theoretical_amounts[key]
                                          ['balance'])
                                    boa = budget_origin_amounts[key]['balance']
                                    res_diff.update({key: {'balance': boa - bb,
                                                           }})
                                    balance += res_diff[key]['balance']
                            res_diff.update({'line': {'balance': balance}})
                            r = res_diff
                            budget_codes[(line.code
                                          if line.code else 'stni_no_code'
                                          )][budget_id-1] = balance
                    else:
                        r = line.with_context(date_from=date_from,
                                              date_to=date_to,
                                              strict_range=strict_range,
                                              )._eval_formula2(
                            financial_report,
                            debit_credit,
                            currency_table,
                            linesdicts[k],
                            budget_id,
                            budget_codes,
                            to_calc,)
                        budget_origin_amounts = r

                    debit_credit = False
                    if type(r) is dict:
                        temp = r
                        r = []
                        r.append(temp)
                    res.extend(r)
                    for column in r:
                        domain_ids.update(column)
                        if len(list(column.keys())) > 1:
                            acc_ids = list(column.keys())
                    k += 1

                # Correct wrong lines with 4 times the same value
                if len(res) == 4:
                    if (res[0]['line']['balance'] == res[1]['line']['balance']
                        and res[0]['line']['balance'] == (
                                    res[2]['line']['balance'])
                            and res[0]['line']['balance']):
                        for i in range(3):
                            res[i+1]['line']['balance'] = 0

            # For each other filter
            else:
                for period in comparison_table:
                    date_from = period.get('date_from', False)
                    date_to = (period.get('date_to', False)
                               or period.get('date', False))
                    date_from, date_to, strict_range = line.with_context(
                        date_from=date_from,
                        date_to=date_to
                    )._compute_date_range()
                    r = line.with_context(date_from=date_from,
                                          date_to=date_to,
                                          strict_range=strict_range
                                          )._eval_formula(
                        financial_report,
                        debit_credit,
                        currency_table,
                        linesdicts[k])
                    debit_credit = False
                    res.extend(r)
                    for column in r:
                        domain_ids.update(column)
                    k += 1
            res = line._put_columns_together(res, domain_ids)
            if line.hide_if_zero and all(
                    [float_is_zero(k, precision_rounding=currency_precision)
                     for k in res['line']]):
                continue
            # Studer Nicola end of extension
            # Post-processing ; creating line dictionary,
            # building comparison, computing total for extended, formatting
            vals = {
                'id': line.id,
                'name': line.name,
                'level': line.level,
                'class': ('o_account_reports_totals_below_sections'
                          if self.env.user.company_id.totals_below_sections
                          else ''),
                'columns': [{'name': l} for l in res['line']],
                'unfoldable': (len(domain_ids) > 1
                               and line.show_domain != 'always'),
                'unfolded': (line.id in options.get('unfolded_lines', [])
                             or line.show_domain == 'always'),
                'page_break': line.print_on_new_page,
            }

            if (financial_report.tax_report
                and line.domain and not line.action_id):
                vals['caret_options'] = 'tax.report.line'

            if line.action_id:
                vals['action_id'] = line.action_id.id
            domain_ids.remove('line')
            lines = [vals]
            groupby = line.groupby or 'aml'
            if (line.id in options.get('unfolded_lines', [])
                    or line.show_domain == 'always'):
                if line.groupby:
                    domain_ids = sorted(list(domain_ids),
                                        key=lambda q: line._get_gb_name(q))
                for domain_id in domain_ids:
                    name = line._get_gb_name(domain_id)
                    vals = {
                        'id': domain_id,
                        'name': (name and len(name) >= 45 and name[0:40]
                                 + '...' or name),
                        'level': line.level,
                        'parent_id': line.id,
                        'columns': [{'name': l} for l in res[domain_id]],
                        'caret_options': (groupby == 'account_id'
                                          and 'account.account'
                                          or groupby),
                    }
                    if line.financial_report_id.name == 'Aged Receivable':
                        vals['trust'] = self.env['res.partner'].browse(
                            [domain_id]
                        ).trust
                    lines.append(vals)
                if (domain_ids
                        and self.env.user.company_id.totals_below_sections):
                    lines.append({
                        'id': 'total_' + str(line.id),
                        'name': _('Total') + ' ' + line.name,
                        'level': line.level,
                        'class': 'o_account_reports_domain_total',
                        'parent_id': line.id,
                        'columns': copy.deepcopy(lines[0]['columns']),
                    })
            for vals in lines:
                if len(comparison_table) == 2 and not options.get('groups'):
                    vals['columns'].append(line._build_cmp(
                        vals['columns'][0]['name'],
                        vals['columns'][1]['name']
                    ))
                    for i in [0, 1]:
                        vals['columns'][i] = line._format(vals['columns'][i])
                # Studer Nicola Extension
                elif (rfilter == "budget_comparison"
                      and not options.get('groups')
                        and options['comparison'].get('number_period', 0) > 0):
                    vals['columns'][4] = line._build_cmp(
                        vals['columns'][0]['name'],
                        vals['columns'][1]['name']
                    )
                    for i in range(4):
                        vals['columns'][i] = line._format(vals['columns'][i])
                # Studer Nicola end of extension
                else:
                    vals['columns'] = [line._format(v)
                                       for v in vals['columns']]
                if not line.formulas:
                    vals['columns'] = [{'name': ''} for k in vals['columns']]
            if len(lines) == 1:
                new_lines = line.children_ids.ext_get_lines(financial_report,
                                                            currency_table,
                                                            options,
                                                            linesdicts,
                                                            budget_codes,
                                                            to_calc
                                                            )
                if new_lines and line.formulas:
                    if self.env.user.company_id.totals_below_sections:
                        divided_lines = self._divide_line(lines[0])
                        result = ([divided_lines[0]]
                                  + new_lines
                                  + [divided_lines[-1]])
                    else:
                        result = [lines[0]] + new_lines
                else:
                    result = lines + new_lines
            else:
                result = lines
            final_result_table += result

        # Studer Nicola Extension
        if (len(to_calc) > 0 and rfilter == 'budget_comparison'
                and comparison_table[0].get('date_to', False)):
            while static.check_calculations(
                to_calc, budget_codes, final_result_table, self
            ):
                pass
        # Studer Nicola end of extension
        return final_result_table

    def _eval_formula_budget(self, acc_ids, budget_id):
        """Calculate the balance for each column if the comparison is enabled.

        Returns
        ----------
        res : dict
            Dictionary which contains the new balance value
        """
        if acc_ids:
            res = {}
            balance = 0.0
            for key in acc_ids:
                if str(key).isdigit():

                    date_to = datetime.strptime(
                        self.env.context['date_to'], "%Y-%m-%d"
                    )
                    date_from = datetime.strptime(
                        self.env.context['date_from'], "%Y-%m-%d"
                    )
                    fiscal_d = self.env.user.company_id.fiscalyear_last_day
                    fiscal_m = self.env.user.company_id.fiscalyear_last_month
                    e_fiscal_date = datetime.strptime(
                        "%s-%s-%s" % (date_to.year, fiscal_m, fiscal_d),
                        DEFAULT_SERVER_DATE_FORMAT
                    )
                    if date_from > e_fiscal_date:
                        e_fiscal_date = datetime.strptime(
                            "%s-%s-%s" % (e_fiscal_date.year + 1,
                                          fiscal_m, fiscal_d),
                            DEFAULT_SERVER_DATE_FORMAT
                        )
                    s_fiscal_date = datetime.strptime(
                        "%s-%s-%s" % (e_fiscal_date.year - 1,
                                      fiscal_m, fiscal_d),
                        DEFAULT_SERVER_DATE_FORMAT
                    ) + timedelta(days=1)
                    if date_from < s_fiscal_date:
                        s_fiscal_date = datetime.strptime(
                            "%s-%s-%s" % (date_from.year, fiscal_m, fiscal_d),
                            DEFAULT_SERVER_DATE_FORMAT
                        )
                        if date_from < s_fiscal_date:
                            s_fiscal_date = datetime.strptime(
                                "%s-%s-%s" % (
                                    s_fiscal_date.year - 1, fiscal_m, fiscal_d
                                ),
                                DEFAULT_SERVER_DATE_FORMAT
                            )

                    budget_ids = self.env['budgetextension.budget'].search(
                        [('account_id', '=', key),
                         ('start_date', '>=', s_fiscal_date),
                         ('end_date', '<=', e_fiscal_date)]
                    )
                    # Calculate theoretical amount
                    planned_amount = 0.0
                    if budget_id == 1:
                        for budget in budget_ids:
                            sd = datetime.strptime(str(budget.start_date),
                                                   DEFAULT_SERVER_DATE_FORMAT)
                            ed = datetime.strptime(str(budget.end_date),
                                                   DEFAULT_SERVER_DATE_FORMAT)
                            actual_duration = (date_to - date_from).days + 1
                            if sd <= date_from and ed <= date_to:
                                actual_duration = (ed - date_from).days + 1
                            elif ed >= date_to and sd >= date_from:
                                actual_duration = (date_to - sd).days + 1
                            elif sd >= date_from and ed <= date_to:
                                actual_duration = (ed - sd).days + 1
                            if actual_duration >= 0:
                                planned_amount += (budget.planned_amount
                                                   / budget.duration_days
                                                   * actual_duration)

                    # Calculate set amount
                    elif budget_id == 2:
                        for budget in budget_ids:
                            planned_amount += budget.planned_amount
                    if budget_id in [1, 2]:
                        res.update({key: {'balance': planned_amount}})
                    balance += res[key]['balance']
            res.update({'line': {'balance': balance}})
            return res
        return {'line': {'balance': 0.0}}

    def _eval_formula2(self, financial_report, debit_credit, currency_table,
                       linesdicts, budget_id, budget_codes, to_calc):
        res = super(FinancialReportExtensionCalculation, self)._eval_formula(
            financial_report, debit_credit, currency_table, linesdicts)
        res = res[0]
        if len(res) == 1 and budget_id and not self.domain:
            balance = 0.0
            formulas = self._split_formulas()
            if formulas.get('balance', False):
                formula = formulas['balance'].strip().replace('.balance', '')
                to_calc.append({'line_id': self.id,
                                'budget_id': budget_id,
                                'formula': formula,
                                'code': (self.code if self.code
                                         else 'stni_no_code')
                                })
            return {'line': {'balance': balance}}
        return res
