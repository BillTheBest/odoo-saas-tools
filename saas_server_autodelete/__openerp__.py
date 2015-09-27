# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (c) 2014 - Present All Rights Reserved
#    Author: Ivan Yelizariev  <yelizariev@it-projects.info>
#    Author: Carlos Almeida <carlos.almeida@thinkopensolutions.com.br>
#    Author: Cesar Lage <kaerdsar@gmail.com>\\
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
    'name': 'SaaS Server - Autodelete expired databases',
    'version': '1.0.0',
    'author': 'Ivan Yelizariev, Carlos Almeida, Cesar Lage ',
    'category': 'SaaS',
    'website': 'https://it-projects.info',
    'depends': ['saas_server'],
    'data': [
        'data/ir_cron.xml',
        ],
    'installable': True,
}
