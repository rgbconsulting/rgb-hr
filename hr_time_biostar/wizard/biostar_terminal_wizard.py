# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

import csv
import pytz
from datetime import datetime
from pytz import timezone
from subprocess import check_output

from openerp import models, api, fields, _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class BiostarTerminalWizard(models.TransientModel):
    _name = "hr.time.biostar.wizard"

    terminal_id = fields.Many2one(string="Terminal", comodel_name='hr.biostar.terminal', required=True)
    process_logs = fields.Boolean(string="Process imported logs",
                                  help="Process attendances of all imported logs",
                                  default=lambda self: int(self.env['ir.config_parameter'].get_param(
                                      'hr_time_biostar.process_logs', default=1)))
    clear_logs = fields.Boolean(string="Clear terminal logs",
                                help="Clear logs stored in device after import success.",
                                default=lambda self: int(self.env['ir.config_parameter'].get_param(
                                    'hr_time_biostar.clear_logs', default=0)))

    def _convert_timestamp(self, timestamp, tz):
        tz = timezone(tz or 'utc')
        date = datetime.fromtimestamp(timestamp, tz)
        utc_date = date.astimezone(pytz.UTC)
        return utc_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    @api.multi
    def action_get_logs(self):
        if not self.terminal_id:
            raise Warning(_('Select one terminal.'))
        self.terminal_id.action_get_logs(self.process_logs,self.clear_logs)
