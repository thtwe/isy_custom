# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, exceptions, fields, models, _

class BudgetGrouping(models.Model):
    _name = 'budgetextension.grouping'
    _description = 'Grouping'

    name = fields.Char(
    	string='Group Name',
    	store=True,
    	)

