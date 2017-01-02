# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import models, api


class AttendanceWizardReport(models.AbstractModel):
    _name = 'report.hr_time_control.attendance_template'

    @api.model
    def _process_data(self, attendances):
        recs = {}

        for atd in attendances:
            employee_id = atd.employee_id.id
            if employee_id in recs:
                recs[employee_id]['attendances'] += atd
                recs[employee_id]['total_hours'] += atd.hours
                if atd.attendance_date not in recs[employee_id]['distinct_days']:
                    recs[employee_id]['distinct_days'].append(atd.attendance_date)
            else:
                recs[employee_id] = {
                    'name': atd.employee_id.name,
                    'distinct_days': [atd.attendance_date],
                    'attendances': atd,
                    'total_hours': atd.hours,
                }
        return recs

    @api.multi
    def render_html(self, data):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('hr_time_control.attendance_template')
        if data:
            date_from = data['form'].get('date_from')
            date_to = data['form'].get('date_to')
            employee_ids = data['form'].get('employee_ids')
            attendances = self.env[report.model].search([('employee_id', 'in', employee_ids),
                                                         ('attendance_date', '>=', date_from),
                                                         ('attendance_date', '<=', date_to)], order='attendance_date')
            working_time = data['form'].get('working_time')
        else:
            attendances = self.env[report.model].browse(self.ids).sorted(key=lambda rec: rec.attendance_date)
            date_from = attendances[0].attendance_date
            date_to = attendances[-1].attendance_date
            working_time = 8
        # Prepare template data
        recs = self._process_data(attendances)

        docargs = {
            'working_time': working_time,
            'recs': recs,
            'doc_model': report.model,
            'date_from': date_from,
            'date_to': date_to,
        }
        return report_obj.render('hr_time_control.attendance_template', docargs)
