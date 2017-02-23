# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from datetime import datetime

from openerp import fields, models, api
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class TimeControl(models.Model):
    _name = 'hr.time.control'

    attendance_date = fields.Date(required=True, index=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', required=True)
    entry_date = fields.Datetime()
    exit_date = fields.Datetime()
    hours = fields.Float(compute='_hours_compute', readonly=True, store=True)
    attendance_error = fields.Boolean()

    @api.one
    @api.depends('entry_date', 'exit_date')
    def _hours_compute(self):
        if self.entry_date and self.exit_date:
            entry_date = datetime.strptime(self.entry_date, DEFAULT_SERVER_DATETIME_FORMAT)
            exit_date = datetime.strptime(self.exit_date, DEFAULT_SERVER_DATETIME_FORMAT)
            self.hours = (exit_date - entry_date).seconds / 3600.0
        else:
            self.hours = 0
