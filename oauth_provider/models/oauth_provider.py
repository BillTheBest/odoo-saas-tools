# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (c) 2014 - Present All Rights Reserved
#    Author: Ivan Yelizariev  <yelizariev@it-projects.info>
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
from openerp import models, fields
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

import uuid

class OauthApplication(models.Model):
    CLIENT_ID_CHARACTER_SET = r'_-.:;=?!@0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    _name = 'oauth.application'
    _rec_name = 'client_id'

    def generate_client_id(self):
        return str(uuid.uuid1())

    client_id = fields.Char('Client ID', select=True, required=True, default=generate_client_id)
    token_ids = fields.One2many('oauth.access_token', 'application_id', 'Tokens')

    _sql_constraints = [
        ('client_id_uniq', 'unique (client_id)', 'client_id should be unique!'),
    ]


class OauthAccessToken(models.Model):
    _name = 'oauth.access_token'

    application_id = fields.Many2one('oauth.application', string='Application')
    token = fields.Char('Access Token', required=True)
    user_id = fields.Many2one('res.users', string='User', required=True)
    expires = fields.Datetime('Expires', required=True)
    scope = fields.Char('Scope')

    def is_valid(self, cr, uid, ids, scopes=None, context=None):
        """
        Checks if the access token is valid.

        :param scopes: An iterable containing the scopes to check or None
        """
        res = {}
        for t in self.browse(cr, uid, ids, context=context):
            res[t.id] = datetime.now() >= datetime.strptime(t.expires, DEFAULT_SERVER_DATETIME_FORMAT) and self._allow_scopes(cr, uid, t, scopes)
        return res

    def is_expired(self, cr, uid, ids, context=None):
        res = {}
        for t in self.browse(cr, uid, ids, context=context):
            res[t.id] = datetime.now() >= self.expires
        return res

    def _allow_scopes(self, cr, uid, token, scopes, context=None):
        if not scopes:
            return True

        provided_scopes = set(self.scope.split())
        resource_scopes = set(scopes)

        return resource_scopes.issubset(provided_scopes)

    def allow_scopes(self, cr, uid, ids, scopes, context=None):
        """
        Check if the token allows the provided scopes

        :param scopes: An iterable containing the scopes to check
        """
        res = {}
        for t in self.browse(cr, uid, ids, context=context):
            res[t.id] = self._allow_scopes(cr, uid, t, scopes, context=context)
        return res
