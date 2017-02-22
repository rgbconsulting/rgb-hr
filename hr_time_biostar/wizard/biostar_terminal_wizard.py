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
        # Get parametrers
        if not self.terminal_id:
            raise Warning(_('Select one terminal.'))
        address = self.terminal_id.address
        port = self.terminal_id.port
        local_tz = self.env.context.get('tz') or self.env.user.tz or 'UTC'
        bs_command = self.env['ir.config_parameter'].get_param('hr_time_biostar.bs_command') or 'bs_command'
        filename = '/tmp/' + datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT) + ".csv"
        # Execute getlog command
        try:
            cmd_out = check_output([bs_command, 'getlog', address, port, filename])
        except BaseException as e:
            raise Warning(_('Biostar device error') + " : " + str(e))
        # Import device logs
        with open(filename) as csvfile:
            hr_time_logs = self.env['hr.time.logs']
            log_list = self.env['hr.time.logs']
            reader = csv.DictReader(csvfile)
            for row in reader:
                log_data = {
                    'date': self._convert_timestamp(int(row['datetime']), local_tz),
                    'employee_code': row['userid'],
                    'action_code': '{},{},{}'.format(row['maincode'], row['subcode'], row['param']), }
                log_list += hr_time_logs.create(log_data)
        if self.process_logs:
            log_list.process_logs()
        if self.clear_logs:
            try:
                cmd_out = check_output([bs_command, 'clearlog', address, port])
            except BaseException as e:
                raise Warning(_('Biostar device error') + " : " + str(e))
