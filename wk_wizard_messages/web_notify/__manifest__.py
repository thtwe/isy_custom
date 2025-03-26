# pylint: disable=missing-docstring
# Copyright 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Web Notify',
    'summary': """
        Send notification messages to user""",
    'version': '1.0.0',
    'license': 'AGPL-3',
    'author': 'ACSONE SA/NV,'
              'AdaptiveCity,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/web',
    'depends': [
        'web',
        'bus',
        'base',
    ],
    'data': [
        'views/web_notify.xml'
    ],
    'demo': [
        'views/res_users_demo.xml'
    ],
    'assets': {
        'web.assets_backend': [
            '/web_notify/static/src/scss/webclient.scss',
            '/web_notify/static/src/js/web_client.js',
            '/web_notify/static/src/js/widgets/notification.js',
        ],
    },
    'installable': True,
}
