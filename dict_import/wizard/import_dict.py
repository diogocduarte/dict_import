# -*- coding: utf-8 -*-
from openerp import api, fields, models
_logger = logging.getLogger(__name__)


class DictImport(models.TransientModel):
    _name = "dict.import"
    _description = "Dictionary Import"
    dict_text = fields.Text('Type')

    @api.multi
    def import_action(self):

        print ".---------------  hello -"
        return {'type': 'ir.actions.act_window_close'}