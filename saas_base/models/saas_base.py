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

from openerp import api, models, fields


class SaasClient(models.AbstractModel):
    _name = 'saas_base.client'
    
    users_len = fields.Integer('Count users', readonly=True)
    file_storage = fields.Integer('File storage (MB)', readonly=True)
    db_storage = fields.Integer('DB storage (MB)', readonly=True)
    expiration_datetime = fields.Datetime('Expiration', track_visibility='onchange')
