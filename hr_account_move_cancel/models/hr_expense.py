# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import models, api, _
from openerp.exceptions import Warning


class AccountInvoice(models.Model):
    _inherit = 'hr.expense.expense'

    @api.multi
    def act_draft(self):
        if self.account_move_id:
            raise Warning(_('Account move must be previously deleted in order to be able to cancel the expense.'))
        else:
            self.write({'state': 'draft'})
