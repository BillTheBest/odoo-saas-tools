# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (c) 2015 - Present All Rights Reserved
#    Author: Ivan Yelizariev  <yelizariev@it-projects.info>
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
from openerp import models


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _auth_oauth_validate(self, cr, uid, provider, access_token, context=None):
        validation = super(ResUsers, self)._auth_oauth_validate(cr, uid, provider, access_token, context=None)
        client_id = validation.get('client_id')
        if client_id:
            p = self.pool['auth.oauth.provider'].browse(cr, uid, provider, context=context)
            assert client_id == p.client_id, "wrong client_id"
        return validation
