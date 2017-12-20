# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def action_create_user(self):
        user_env = self.sudo().env['res.users']
        for rec in self:
            if not rec.user_id:
                name = rec.name.strip()
                user = user_env.with_context(no_reset_password=True).create({
                    'name': name,
                    'login': name.replace(' ', '_').lower(),
                    'email': rec.work_email,
                    'employee_ids': [(4, rec.id)]
                })
                # Remove default user groups
                default_groups = ['base.group_user', 'base.group_partner_manager']
                for group in default_groups:
                    group_obj = self.env.ref(group, False)
                    group_obj.sudo().write({'users': [(3, user.id)]})
