# -*- coding: utf-8 -*-

{
    'name': 'Social Partner',
    'category': 'Partner',
    'summary': 'Social Partner',
    'version': '1.0',
    'description': """Add social networks to customers""",
    'depends': ['base', 'crm', 'contacts', 'website'],
    'data': [
        'views/res_partner_view.xml',
        'views/partner_template.xml',
    ],
    'application': False,
    'installable': True,
}
