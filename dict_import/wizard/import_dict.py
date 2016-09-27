# -*- coding: utf-8 -*-
from openerp import api, fields, models
import ast
import cgitb
import sys
import re
from openerp.tools.misc import ustr
from openerp.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class DictImport(models.TransientModel):
    _name = "dict.import"
    _description = "Dictionary Import"

    dict_text = fields.Text('Dict')
    data_file = fields.Binary(string='Import File')

    def ref(self, reference):
        r = reference.split('.')
        if len(r) == 1:
            r.insert(0, 'dict_import')
        refid = '.'.join(r)
        return self.env.ref(refid)

    @api.multi
    def import_action(self):
        for wz in self:
            lines = []
            if wz.dict_text:
                lines = wz.dict_text.splitlines()
            i = 0
            msg = False

            for l in lines:
                i += 1
                # this will transform: ref(reference1) into self.ref('reference1').id
                lin = re.sub(r"ref\((.*)\)", r"self.ref('\1').id", l)
                try:
                    d = eval(lin)
                except Exception:
                    import traceback
                    _logger.error(traceback.format_exc())
                    self._cr.rollback()
                    break

                d.update({'action': d.get('action', 'create')})

                for k, v in d['data'].iteritems():
                    if isinstance(v, dict):
                        d['data'][k] = [(0, 0, v)]

                # ir.model.data
                iid = d['data'].get('.id', False)
                # if iid is empty same as False
                iid = False if iid == '' else iid
                d['data'].pop(".id", None)

                if d['action'] == 'create':
                    # create record
                    rec = self.env[d['model']].create(d['data'])

                if d['action'] == 'write':
                    # get record
                    rec = self.env[d['model']].browse(d['data']['id'])
                    rec.write(d['data'])

                # create external reference id
                if iid:
                    self.env['ir.model.data'].create({'module': 'dict_import',
                                                      'name': iid,
                                                      'model': d['model'],
                                                      'res_id': rec.id,
                                                      'noupdate': 1})
                self._cr.commit()

        #{'type': 'ir.actions.act_window_close'}
