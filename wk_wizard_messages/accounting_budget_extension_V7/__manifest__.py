# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2018 brain-tec AG (http://www.braintec-group.com)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################
{
    'name': "Budget Extension",
    'summary': """Create budgets easily. Compare budgets in a financial report.""",
    'description': """
        Budget Extension module for extending reports:
            - Add new, extended budgets to an account for a fiscal year and show their information in a financial report.
            - Compare the budgets grouped by account and sorted by the end date.
            - Let the system calculate the recommended period length for the budget.
    """,
    'author': "brain-tec",
    'website': 'http://www.braintec-group.com/',
    'category': 'Advanced Reporting',
    'version': '1.0.0',
    'price': 30.00,
    'currency': 'EUR',
    'license': 'OPL-1',
    'images': [
        'static/description/main_screenshot.png'
    ],
    'depends': [
        'account_reports',
    ],
    'data': [
        #'views/account_financial_report_inheritance.xml',
        'views/budget.xml',
        'views/opex_view.xml',
        'views/capex_view.xml',
        'views/budget_templates.xml',
        'views/opex_capex_config.xml',
        'security/ir.model.access.csv',
        'data/budget.xml',
        'data/paper_format.xml',
        'reports/report.xml',
        'reports/opex_report.xml',
        'reports/capex_report.xml',
    ],
}
