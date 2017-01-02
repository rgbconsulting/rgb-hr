# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models, api


class TimeControlWizard(models.TransientModel):
    _name = 'hr.time.control.wizard'

    date_from = fields.Date(default=fields.Date.context_today, required=True)
    date_to = fields.Date(default=fields.Date.context_today, required=True)
    employee_ids = fields.Many2many(comodel_name='hr.employee')
    working_time = fields.Float(default=8)

    @api.multi
    def print_report(self):
        self.ensure_one()
        data = {}
        data['form'] = self.read(['date_from', 'date_to', 'employee_ids', 'working_time'])[0]
        return self.env['report'].get_action(self, 'hr_time_control.attendance_template', data=data)
