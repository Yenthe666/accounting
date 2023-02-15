# -*- coding: utf-8 -*-
{
    'name': "Invoice legal terms",

    'summary': """
        Configure legal terms per tax. The terms will be displayed on the invoice pdf.
    """,

    'description': """
        Configure legal terms per tax. The terms will be displayed on the invoice pdf.
    """,

    'author': "Mainframe Monkey",
    'website': "http://www.mainframemonkey.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    'license': 'LGPL-3',

    # always loaded
    'data': [
        'views/account_tax_views.xml',
        'report/report_invoice.xml',
    ],
}