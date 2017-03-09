# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from datetime import datetime

from openerp import fields, models, api, _
from openerp.exceptions import Warning
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from time_action import ACTION_SIGN_IN, ACTION_SIGN_OUT


class TimeLogs(models.Model):
    _name = 'hr.time.logs'

    date = fields.Datetime(default=fields.Datetime.now(), required=True, index=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    employee_code = fields.Char(string="Employee code")
    action_id = fields.Many2one(comodel_name='hr.time.action', string='Action')
    action_code = fields.Char(string="Action code")
    processed = fields.Boolean()
    error = fields.Boolean()
    name = fields.Char(compute='_compute_line_name',readonly=True)

    @api.one
    @api.depends('employee_code', 'date')
    def _compute_line_name(self):
        self.name = self.date +' - '+ self.employee_code or ''

    def _process_signin(self):
        employee_id = self.employee_id.id
        entry_date = self.date
        att_date = str(datetime.strptime(entry_date, DEFAULT_SERVER_DATETIME_FORMAT).date())
        time_control_model = self.env['hr.time.control']
        control_rec = time_control_model.search([('employee_id', '=', employee_id), ('attendance_date', '=', att_date),
                                                 ('entry_date', '=', False), ('exit_date', '>=', entry_date)],
                                                order='exit_date', limit=1)
        if control_rec:
            control_rec.entry_date = self.date
            control_rec.attendance_error = False
        else:
            time_control_model.create({
                'employee_id': employee_id,
                'attendance_date': att_date,
                'entry_date': entry_date,
                'attendance_error': True
            })

    def _process_signout(self):
        employee_id = self.employee_id.id
        exit_date = self.date
        att_date = str(datetime.strptime(exit_date, DEFAULT_SERVER_DATETIME_FORMAT).date())
        time_control_model = self.env['hr.time.control']
        control_rec = time_control_model.search([('employee_id', '=', employee_id), ('attendance_date', '=', att_date),
                                                 ('exit_date', '=', False), ('entry_date', '<=', exit_date)],
                                                order='entry_date desc', limit=1)
        if control_rec:
            control_rec.exit_date = self.date
            control_rec.attendance_error = False
        else:
            time_control_model.create({
                'employee_id': employee_id,
                'attendance_date': att_date,
                'exit_date': exit_date,
                'attendance_error': True
            })

    @api.multi
    def process_logs(self):
        if any(log.processed for log in self):
            raise Warning(_('All the selected logs must be unprocessed to perform this action'))
        else:
            employee_model = self.env['hr.employee']
            action_model = self.env['hr.time.action']
            # Iterate records sorted by date
            for log in self.sorted(key=lambda rec: rec.date):
                log.processed = True
                log.error = False
                # Assign log employee_id
                if not log.employee_id and log.employee_code:
                    employee = employee_model.search([('external_code', '=', log.employee_code)], limit=1)
                    if employee:
                        log.employee_id = employee
                    else:
                        log.error = True
                # Assign log action_id
                if not log.action_id and log.action_code:
                    action = action_model.search([('external_code', '=', log.action_code)], limit=1)
                    if action:
                        log.action_id = action
                    else:
                        log.error = True
                # Process attendance events
                if not log.error and log.employee_id and log.action_id:
                    if log.action_id.action_type == ACTION_SIGN_IN:
                        log._process_signin()
                    elif log.action_id.action_type == ACTION_SIGN_OUT:
                        log._process_signout()
