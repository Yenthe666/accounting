# -*- coding: utf-8 -*-
{
    'name': "Auto invoice advance on confirmed sale orders",

    'summary': """
        Automatically create an advance invoice of confirmed sales for a configured percentage
        """,

    'description': """
        Automatically create an advance invoice of confirmed sales for a configured percentage
    """,

    'author': "Mainframe Monkey",
    'website': "https://www.mainframemonkey.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale'],

    # always loaded
    'data': [
        'data/ir_cron.xml',
        'views/res_config_settings.xml',
    ],
}
