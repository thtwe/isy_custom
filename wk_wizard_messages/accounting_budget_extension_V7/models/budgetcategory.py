
# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta
from odoo import api, exceptions, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

class BudgetCategory(models.Model):
     _name = 'budget.category'
    _description = 'Budget Category'
    name = fields.Char(string = 'Budget Category', translate=True, required=True)
    