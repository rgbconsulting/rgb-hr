# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from datetime import datetime

from openerp import fields, models, api, _
from openerp.exceptions import except_orm
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class TimeControl(models.Model):
    _name = 'hr.time.control'

    attendance_date = fields.Date(required=True, index=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', required=True)
    entry_date = fields.Datetime()
    exit_date = fields.Datetime()
    hours = fields.Float(compute='_hours_compute', readonly=True, store=True)
    attendance_error = fields.Boolean(compute='_error_check')

    @api.one
    @api.depends('entry_date', 'exit_date')
    def _hours_compute(self):
        if self.entry_date and self.exit_date:
            entry_date = datetime.strptime(self.entry_date, DEFAULT_SERVER_DATETIME_FORMAT)
            exit_date = datetime.strptime(self.exit_date, DEFAULT_SERVER_DATETIME_FORMAT)
            self.hours = (exit_date - entry_date).seconds / 3600.0
        else:
            self.hours = 0

    @api.one
    @api.depends('entry_date', 'exit_date')
    def _error_check(self):
        self.attendance_error = not (self.entry_date and self.exit_date)

    @api.one
    @api.onchange('entry_date')
    def _attendance_date_check(self):
        if not self.attendance_date:
            self.attendance_date = self.entry_date

    @api.one
    @api.constrains('entry_date', 'exit_date')
    def _check_date_validity(self):
        if self.exit_date and self.entry_date and self.exit_date < self.entry_date:
            raise except_orm(_("Error with dates!"), _("Exit date is earlier than entry date"))
