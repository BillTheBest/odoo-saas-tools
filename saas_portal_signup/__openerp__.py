# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (c) 2015 - Present All Rights Reserved
#    Author: Cesar Lage <kaerdsar@gmail.com>
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
    'name': 'SaaS Portal Sign Up',
    'version': '1.0.0',
    'author': 'Cesar Lage',
    'category': 'SaaS',
    'website': 'https://it-projects.info',
    'depends': ['auth_signup', 'saas_portal'],
    'data': ['views/signup.xml'],
    'installable': True,

    'description': '''
Module to book a new client in SaaS Portal from sign up
    ''',
}
