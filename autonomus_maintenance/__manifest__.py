# -*- coding: utf-8 -*-
{
    'name': "Autonomus Maintenance",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "chiguer",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list

    'version': '0.1',
'category': 'Manufacturing',
    'depends': ['base', 'maintenance', 'calendar','web'],
    # any module necessary for this one to work correctly


    # always loaded
    'data': ['data/ir_cron_data.xml',
        'security/ir.model.access.csv',
        'views/autonomous_maintenance_task_views.xml',
        'views/autonomous_maintenance_views.xml',
        'views/autonomous_maintenance_actions.xml',
        'views/autonomous_maintenance_menu.xml','views/equipement_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': ['autonomus_maintenance/static/src/js/kanban_card_click.js'
                        
        ],},
    'installable': True,
    'application': True,
}

