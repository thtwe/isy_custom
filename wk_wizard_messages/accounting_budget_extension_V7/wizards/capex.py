# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CapexReportWizard(models.TransientModel):
    _name = 'capex.report.wizard'
    _description = 'Capex Report Wizard'

    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
        }

        return self.env.ref('accounting_budget_extension_V7.report_budget_capex').report_action(self, data=data)


class BudgetCapexReport(models.AbstractModel):
    _name = 'report.accounting_budget_extension_v7.budget_capex_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        capex_lines = self.env['budget.capex'].search([], order='sequence asc')
        for req_line in capex_lines:
            docs.append({
                'name': req_line.name,
                'jul_total': req_line.jul_total,
                'aug_total': req_line.aug_total,
                'sep_total': req_line.sep_total,
                'oct_total': req_line.oct_total,
                'nov_total': req_line.nov_total,
                'dec_total': req_line.dec_total,
                'jan_total': req_line.jan_total,
                'feb_total': req_line.feb_total,
                'mar_total': req_line.mar_total,
                'apr_total': req_line.apr_total,
                'may_total': req_line.may_total,
                'jun_total': req_line.jun_total,
                'budget_total': req_line.budget_total,
                'actual_total': req_line.actual_total,
                'percentage': req_line.percentage,
                'capex_type_id': req_line.capex_type_id,
            })
        
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'docs': docs,
        }

        