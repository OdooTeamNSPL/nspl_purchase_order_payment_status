{
    'name': 'Purchase Order Payment Status',
    'version': '19.0.1',
    'summary': 'Track purchase order payments with status indicators and quick payment insights',
    'description': """
This module allows you to track and manage purchase order payments efficiently.

✔ Color-coded payment status: Paid, Partial, Unpaid, Overdue  
✔ Automatic calculation of amount due  
✔ View due amount and payment status directly in purchase orders

A simple and effective tool for better payment visibility and control in purchase workflows.
""",
    'category': 'Purchases',
    'sequence': 3,
    'author': 'Namah Softech Private Limited',
    'contributors': 'Mohit Nare',
    'website': 'http://namahsoftech.com/',
    'license': 'OPL-1',
    'price': 15.99,
    'currency': 'USD',
    'support': 'support@namahsoftech.com',
    'depends': ['purchase', 'account' ,'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_view.xml',
    ],
    'images': ['static/description/img/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
