# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (c) 2015 - Present All Rights Reserved
#    Author: Salton Massally <salton.massally@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of the GNU General Public License is available at:
#    <http://www.gnu.org/licenses/gpl.html>.
##############################################################################

{
    'name': 'SaaS Sysadmin backup',
    'summary': "System Administration Backup Framework for SAAS Tools",
    'version': '1.0.0',
    'author': 'Salton Massally <smassally@idtlabs.sl> (iDT Labs)',
    'category': 'SaaS',
    'website': 'idtlabs.sl',
    'depends': ['saas_sysadmin'],
    'data': [
        'views/saas_portal_views.xml',
        ],
    'installable': True,
}
