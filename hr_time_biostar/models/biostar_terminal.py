# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

import csv
import pytz
from datetime import datetime
from pytz import timezone
from subprocess import check_output

from openerp import models, api, fields, _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class BiostarTerminal(models.Model):
    _name = "hr.biostar.terminal"

    name = fields.Char(required=True)
    address = fields.Char(required=True)
    port = fields.Char(required=True)
    code = fields.Char()
    auto_get = fields.Boolean(string="Auto get logs")

    def _convert_timestamp(self, timestamp, tz):
        tz = pytz.timezone(tz or 'utc')
        date = datetime.fromtimestamp(timestamp, tz)
        utc_date = date.astimezone(pytz.UTC)
        db_date = utc_date - date.utcoffset()
        return db_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    @api.one
    def action_get_logs(self, process_logs, clear_logs):
        # Get parametrers
        address = self.address
        port = self.port
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
                    'action_code': '{},{},{}'.format(row['maincode'], row['subcode'], row['param']),}
                log_list += hr_time_logs.create(log_data)
        if process_logs:
            log_list.process_logs()
        if clear_logs:
            try:
                cmd_out = check_output([bs_command, 'clearlog', address, port])
            except BaseException as e:
                raise Warning(_('Biostar device error') + " : " + str(e))

    @api.model
    def cron_action(self, process_logs=False, clear_logs=False):
        terminals = self.search([('auto_get', '=', True)])
        if terminals:
            for t in terminals:
                t.action_get_logs(process_logs, clear_logs)
