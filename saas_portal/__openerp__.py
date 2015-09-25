# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (c) 2014 - Present All Rights Reserved
#    Author: Ivan Yelizariev  <yelizariev@it-projects.info>
#    Author: Cesar Lage <kaerdsar@gmail.com>
#    Author: D.H. Bahr <dhbahr@gmail.com>
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
    'name': 'SaaS Portal',
    'version': '1.0.0',
    'author': 'Ivan Yelizariev, Cesar Lage, D.H. Bahr',
    'category': 'SaaS',
    'website': 'https://it-projects.info',
    'depends': ['oauth_provider', 'website', 'auth_signup', 'saas_base', 'saas_utils'],
    'data': [
        'data/plan_sequence.xml',
        'views/wizard.xml',
        'views/saas_portal.xml',
        'views/res_config.xml',
        ],
    'installable': True,
}
