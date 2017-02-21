# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    external_code = fields.Char()
    attendance_count = fields.Integer(string='# of Attendances', compute='_count_attendances', readonly=True)

    def _count_attendances(self):
        for rec in self:
            rec.attendance_count = self.env['hr.time.control'].search_count([('employee_id', '=', rec.id)])

    @api.multi
    def action_attendances_view(self):
        result = {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.time.control',
            'domain': [('employee_id', '=', self.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'context': {'default_employee_id': self.id}
        }
        return result
