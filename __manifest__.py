{
    'name': "ePrescription Module",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'web'],

    # always loaded
    'data': [
        # Security
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/ir_sequence.xml',
        
        # Views
        'views/views/prescription.xml',
        
        'views/actions/actions.xml',
        'views/menuitems.xml',
        
        # Reports
        'reports/paperformats.xml',
        'reports/prescription_qr.xml',
        'reports/report_actions.xml',
        
        # Templates
        # 'static/src/xml/qr_scanner.xml',
        'views/views/qr_scan.xml',
    ],
    
    'assets': {
        "web.assets_frontend": [
            "prescription_scanner/static/src/css/style.css",
            "prescription_scanner/static/src/js/scanner.js",
            "prescription_scanner/static/src/js/prescription.js",
            "prescription_scanner/static/src/js/dispense.js",
            "prescription_scanner/static/src/xml/qr_scanner.xml",
            "prescription_scanner/static/src/xml/prescription.xml",
            "prescription_scanner/static/src/xml/dispense.xml",
        ],
    },
    
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

