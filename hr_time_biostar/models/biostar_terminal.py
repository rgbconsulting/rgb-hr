# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import models, api, fields


class BiostarTerminal(models.Model):
    _name = "hr.biostar.terminal"

    name = fields.Char(required=True)
    address = fields.Char(required=True)
    port = fields.Char(required=True)
    code = fields.Char()
