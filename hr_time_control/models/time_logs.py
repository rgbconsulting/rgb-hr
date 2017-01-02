# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models, api, _
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import Warning


class TimeLogs(models.Model):
    _name = 'hr.time.logs'

    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    employee_external_code = fields.Char()
    date = fields.Datetime(required=True, default=fields.Datetime.now())
    action = fields.Many2one(comodel_name='hr.time.action', string='Action')
    processed = fields.Boolean()
    error = fields.Boolean()

    def _process_signin(self, employee_id):
        time_control_model = self.env['hr.time.control']
        log_date = datetime.strptime(self.date, DEFAULT_SERVER_DATETIME_FORMAT).date()
        control_rec = time_control_model.search([('attendance_date', '=', log_date), ('entry_date', '=', False),
                                                 ('exit_date', '>', self.date), ('employee_id', '=', employee_id)],
                                                order='exit_date', limit=1)
        if control_rec:
            control_rec.entry_date = self.date
            control_rec.attendance_error = False
        else:
            time_control_model.create({
                'employee_id': employee_id,
                'attendance_date': log_date,
                'entry_date': self.date,
                'attendance_error': True
            })

    def _process_signout(self, employee_id):
        time_control_model = self.env['hr.time.control']
        log_date = datetime.strptime(self.date, DEFAULT_SERVER_DATETIME_FORMAT).date()
        control_rec = time_control_model.search(
            [('attendance_date', '=', log_date), ('exit_date', '=', False), ('employee_id', '=', employee_id)],
            order='entry_date desc', limit=1)
        if control_rec:
            control_rec.exit_date = self.date
            control_rec.attendance_error = False
        else:
            time_control_model.create({
                'employee_id': employee_id,
                'attendance_date': log_date,
                'exit_date': self.date,
                'attendance_error': True
            })

    @api.multi
    def process_logs(self):
        if any(log.processed for log in self):
            raise Warning(_('All the selected logs must be unprocessed to perform this action'))
        else:
            employee_model = self.env['hr.employee']
            # Iterate records sorted by date
            for log in self.sorted(key=lambda rec: rec.date):
                log.error = False
                # Assign log employee_id
                log_employee = log.employee_id
                if not log_employee and log.employee_external_code:
                    log_employee = employee_model.search(
                        [('employee_external_code', '=like', log.employee_external_code)],
                        limit=1)
                    if log_employee:
                        log.employee_id = log_employee
                # If no employee mark as error and skip
                if not log_employee:
                    log.error = True
                    continue
                # Process log
                if log.action.action_type == '1':
                    log._process_signin(log_employee.id)
                    log.processed = True
                elif log.action.action_type == '2':
                    log._process_signout(log_employee.id)
                    log.processed = True
                else:
                    log.error = True
                    continue
