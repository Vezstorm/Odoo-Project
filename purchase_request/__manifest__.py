{
    'name': 'Purchase Request',
    'description': 'This module allows users to raise a purchase request',
    'author': 'Ibrahim',
    'depends': ['base', 'mail', 'purchase', 'hr'],
    'license':'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'demo':[
    ],
}