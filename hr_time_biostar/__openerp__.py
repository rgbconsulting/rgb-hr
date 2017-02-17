# -*- coding: utf-8 -*-
##############################################################################
#
#   HR Time Biostar
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
    'name': "HR Time Biostar",
    'version': '1.0',
    'depends': ['hr_time_control'],
    'license': 'AGPL-3',
    'author': "RGB Consulting SL",
    'website': "http://www.rgbconsulting.com",
    'category': 'Project',
    'summary': """HR Time Biostar""",
    'description': """
HR Time Biostar
==============================

This module extends hr_time_control to support biostart devices.
    """,

    'data': [
        'views/biostar_terminal.xml',
        'wizard/biostar_terminal_wizard.xml',
        'security/ir.model.access.csv',
        'data/config.xml',
        'data/actions.xml',
    ],

    'demo': [
    ],
}
