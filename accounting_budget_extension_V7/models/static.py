# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2018 brain-tec AG (http://www.braintec-group.com)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################
import re
from odoo.tools.safe_eval import safe_eval

formula_regex = "[a-zA-Z1-9]\w+"


def is_float(num):
    """Checks if the parameter can be converted to float

    Returns
    ----------
    bool
        Returns True if the argument can be successfully converted to float.
    """
    try:
        float(str(num))
    except ValueError:
        return False
    return True


def calc_balance(formula, budget_id, budget_codes, old_balance=0):
    """Calculate the balance with the formula

    Keyword parameters
    ----------
    formula : string
        formula which contains the keys to calculate the balance
    budget_codes : dict
        Dict with the codes and their calculated values.
    old_balance : float, optional
        Integer which contains the old balance of the line in case
        the calculation fails.
    """
    b = None
    formula = formula.strip().replace('.balance', '')
    keys = re.findall(formula_regex, formula)

    # noinspection PyBroadException
    try:
        if all(is_float(v[budget_id-1])
               for v in (budget_codes[k] for k in keys)):
            vals = {}
            for key in keys:
                vals[key] = budget_codes[key][budget_id-1]
            b = safe_eval(formula, vals)
    except Exception:
        b = old_balance
    return b


def check_calculations(to_calc, budget_codes, final_result_table, obj):
    """Tries to calculate the values of lines which couldn't be calculated.

    Keyword parameters
    ----------
    to_calc : dict
        Dict with the lines which values need to be calculated.
    budget_codes : dict
        Dict with the codes and their calculated values.

    Returns
    ----------
    changes : bool
        If a line could be calculated it returns True
    """
    changes = False
    k = 0
    for calc_dict in to_calc:
        formula_keys = re.findall(formula_regex, calc_dict['formula'])
        if all(key in budget_codes.keys() for key in formula_keys):
            calculated = False
            cond = (line for line in final_result_table
                    if line['id'] == calc_dict['line_id']
                    and budget_codes.get(calc_dict['code'], False)
                    and line['columns'][0].get('name', False))
            for line in cond:
                new_balance = 0
                if calc_dict['budget_id'] != 4:
                    new_balance = (calc_balance(
                                    calc_dict['formula'],
                                    calc_dict['budget_id'],
                                    budget_codes
                                   ))
                    line['columns'][calc_dict['budget_id']] = obj[0]._format(
                        {'name': new_balance}
                    )
                    (budget_codes[
                        calc_dict['code']
                    ][calc_dict['budget_id'] - 1]) = (
                        new_balance
                    )
                else:
                    if 'no_format_name' in line['columns'][0]:
                        line['columns'][4] = obj[0]._build_cmp(
                            line['columns'][0]['no_format_name'],
                            line['columns'][1]['no_format_name']
                        )
                    else:
                        line['columns'][4] = obj[0]._build_cmp(
                            line['columns'][0]['name'],
                            line['columns'][1]['name']
                        )
                if new_balance:
                    calculated = True
                    changes = True
            if calculated:
                del to_calc[k]
        k += 1
    return changes
