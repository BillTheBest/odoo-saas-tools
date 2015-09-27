# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (c) 2014 - Present All Rights Reserved
#    Author: Ivan Yelizariev  <yelizariev@it-projects.info>
#    Author: Cesar Lage <kaerdsar@gmail.com>
#    Author: Salton Massally <salton.massally@gmail.com>
#    Author: D.H. Bahr <dhbahr@gmail.com>
#    Author: José Andrés Hernández Bustio <jbustio@gmail.com>
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
    'name': 'SaaS Server',
    'version': '1.0.0',
    'author': 'Ivan Yelizariev, Cesar Lage, Salton Massally, D.H. Bahr, José Andrés Hernández Bustio',
    'category': 'SaaS',
    'website': 'https://it-projects.info',
    'depends': ['auth_oauth', 'saas_base', 'saas_utils', 'website'],
    'data': [
        'views/saas_server.xml',
        'views/res_config.xml',
        'data/auth_oauth_data.xml',
        'data/ir_config_parameter.xml',
        'data/pre_install.yml',
    ],
    'installable': True,
}
