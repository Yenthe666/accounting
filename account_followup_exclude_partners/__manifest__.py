# -*- coding: utf-8 -*-
{
    'name': "Account followup exclude partners",

    'summary': """
        Exclude partners for payment reminders
        """,

    'description': """
        Exclude partners for payment reminders
    """,

    'author': "Mainframe Monkey",
    'website': "http://www.mainframemonkey.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['account_followup'],

    # always loaded
    'data': [
        'views/res_partner_views.xml',
    ],
}