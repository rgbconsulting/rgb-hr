# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models

# time action constants
ACTION_OTHER = '0'
ACTION_SIGN_IN = '1'
ACTION_SIGN_OUT = '2'


class TimeAction(models.Model):
    _name = 'hr.time.action'

    name = fields.Char(required=True)
    action_type = fields.Selection(
        selection=[(ACTION_SIGN_IN, 'Sign in'), (ACTION_SIGN_OUT, 'Sign out'), (ACTION_OTHER, 'Other')], required=True)
    external_code = fields.Char()
