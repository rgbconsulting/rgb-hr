# -*- coding: utf-8 -*-
##############################################################################
#
#   HR Time Control
#   Copyright 2016 RGB Consulting, SL
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "HR Time Control",
    'version': '1.0',
    'depends': ['hr', 'report', 'edi'],
    'license': 'AGPL-3',
    'author': "RGB Consulting SL",
    'website': "http://www.rgbconsulting.com",
    'category': 'HR',

    'summary': """Employee attendance management""",

    'description': """
HR Time Control
===============
* This module adds employee attendance management
* The module is not compatible with Odoo's *hr_attendance* module.
    """,

    'data': [
        'security/hr_time_control_security.xml',
        'security/ir.model.access.csv',
        'report/attendance_report.xml',
        'views/templates.xml',
        'views/hr_employee_view.xml',
        'views/time_action_view.xml',
        'views/time_control_view.xml',
        'views/time_logs_view.xml',
        'wizard/time_control_wizard.xml',
    ],

    'demo': [
    ],

}
