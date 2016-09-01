# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Dictionary Import',
    'version': '1.1',
    'category': 'Web',
    'summary': 'Implements dictionary import',
    'description': """
Dictionary Import Module
========================

Dictionary Import Module for Complex Migration Problems

It allows importing different objects with a specific order while setting your own ID's

""",
    'website': 'https://diogocduarte.github.io',
    'depends': [
        'web',
    ],
    'data': [
        'wizard/import_dict.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'qweb': [],
}
