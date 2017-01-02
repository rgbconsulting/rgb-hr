# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models


class TimeAction(models.Model):
    _name = 'hr.time.action'

    name = fields.Char(required=True)
    action_type = fields.Selection(selection=[('1', 'Sign in'), ('2', 'Sign out'), ('0', 'Other')])
    action_external_code = fields.Char()
