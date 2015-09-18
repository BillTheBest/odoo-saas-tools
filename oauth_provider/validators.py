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

# Portions taken from https://github.com/evonove/django-oauth-toolkit/

##############################################################################
# Copyright (c) 2013, Massimiliano Pippi, Federico Frenguelli and contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met: 
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies, 
# either expressed or implied, of the FreeBSD Project.
##############################################################################

from openerp import SUPERUSER_ID
import logging
try:
    from oauthlib.oauth2 import RequestValidator, MobileApplicationServer
except:
    pass
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT

log = _logger = logging.getLogger(__name__)

from openerp.http import request as request

class OAuth2Validator(RequestValidator):

    def _extract_basic_auth(self, req):
        """
        Return authentication string if request contains basic auth credentials, else return None
        """
        auth = req.headers.get('HTTP_AUTHORIZATION', None)
        if not auth:
            return None

        auth_type, auth_string = auth.split(' ')
        if auth_type != "Basic":
            return None

        return auth_string

    def _authenticate_basic_auth(self, req):
        """
        Authenticates with HTTP Basic Auth.

        Note: as stated in rfc:`2.3.1`, client_id and client_secret must be encoded with
        "application/x-www-form-urlencoded" encoding algorithm.
        """
        auth_string = self._extract_basic_auth(req)
        if not auth_string:
            return False

        encoding = req.encoding or 'utf-8'

        auth_string_decoded = base64.b64decode(auth_string).decode(encoding)
        client_id, client_secret = map(unquote_plus, auth_string_decoded.split(':', 1))

        if self._load_application(client_id, req) is None:
            log.debug("Failed basic auth: Application %s does not exist" % client_id)
            return False
        elif req.client.client_secret != client_secret:
            log.debug("Failed basic auth: wrong client secret %s" % client_secret)
            return False
        else:
            return True

    def _authenticate_request_body(self, req):
        """
        Try to authenticate the client using client_id and client_secret parameters
        included in body.

        Remember that this method is NOT RECOMMENDED and SHOULD be limited to clients unable to
        directly utilize the HTTP Basic authentication scheme. See rfc:`2.3.1` for more details.
        """
        #TODO: check if oauthlib has already unquoted client_id and client_secret
        client_id = req.client_id
        client_secret = req.client_secret

        if not client_id or not client_secret:
            return False

        if self._load_application(client_id, req) is None:
            log.debug("Failed body auth: Application %s does not exists" % client_id)
            return False
        elif req.client.client_secret != client_secret:
            log.debug("Failed body auth: wrong client secret %s" % client_secret)
            return False
        else:
            return True

    def _load_application(self, client_id, req, create=True):
        """
        If req.client was not set, load application instance for given client_id and store it
        in req.client
        """
        if not req.client:
            app_obj = request.registry['oauth.application']
            app_id = app_obj.search(request.cr, SUPERUSER_ID, [('client_id','=',client_id)])
            if app_id:
                app_id = app_id[0]
            elif create:
                app_id = app_obj.create(request.cr, SUPERUSER_ID, {'client_id':client_id})
            if app_id:
                req.client = app_obj.browse(request.cr, SUPERUSER_ID, app_id)
        return req.client

    def validate_client_id(self, client_id, req, *args, **kwargs):
        # Simple validity check, does client exist? Not banned?
        return self._load_application(client_id, req)

    def validate_redirect_uri(self, client_id, redirect_uri, req, *args, **kwargs):
        # Is the client allowed to use the supplied redirect_uri? i.e. has
        # the client previously registered this EXACT redirect uri.
        return True #TODO

    def validate_scopes(self, client_id, scopes, client, req, *args, **kwargs):
        # Is the client allowed to access the requested scopes?
        return True #TODO

    def validate_response_type(self, client_id, response_type, client, req, *args, **kwargs):
        # Clients should only be allowed to use one type of response type, the
        # one associated with their one allowed grant type.
        # In this case it must be "code".
        return response_type=='token'

    def authenticate_client(self, req, *args, **kwargs):
        """
        Check if client exists and it's authenticating itself as in rfc:`3.2.1`

        First we try to authenticate with HTTP Basic Auth, and that is the PREFERRED
        authentication method.
        Whether this fails we support including the client credentials in the request-body, but
        this method is NOT RECOMMENDED and SHOULD be limited to clients unable to directly utilize
        the HTTP Basic authentication scheme. See rfc:`2.3.1` for more details
        """
        # Whichever authentication method suits you, HTTP Basic might work
        authenticated = self._authenticate_basic_auth(req)

        if not authenticated:
            authenticated = self._authenticate_request_body(req)

        return authenticated

    def authenticate_client_id(self, client_id, req, *args, **kwargs):
        """
        If we are here, the client did not authenticate itself as in rfc:`3.2.1` and we can
        proceed only if the client exists and it's not of type 'Confidential'.
        Also assign Application instance to req.client.
        """
        if self._load_application(client_id, req) is not None:
            log.debug("Application %s has type %s" % (client_id, req.client.client_type))
            return req.client.client_type != Application.CLIENT_CONFIDENTIAL
        return False

    def save_bearer_token(self, token, req, *args, **kwargs):
        """
        Save access and refresh token, If refresh token is issued, remove old refresh tokens as
        in rfc:`6`
        """
        # Remember to associate it with req.scopes, req.user and
        # req.client. The two former will be set when you validate
        # the authorization code. Don't forget to save both the
        # access_token and the refresh_token and set expiration for the
        # access_token to now + expires_in seconds.

        #if req.refresh_token:
        #    # remove used refresh token
        #    try:
        #        RefreshToken.objects.get(token=req.refresh_token).delete()
        #    except RefreshToken.DoesNotExist:
        #        assert()  # TODO though being here would be very strange, at least log the error
        ACCESS_TOKEN_EXPIRE_SECONDS = 60*60
        expires = datetime.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
        #if req.grant_type == 'client_credentials':
        #    req.user = req.client.user

        access_token_obj = request.registry['oauth.access_token']
        access_token = access_token_obj.create(request.cr, SUPERUSER_ID, {
            'user_id': req.user.id,
            'scope': token['scope'],
            'expires': expires.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            'token': token['access_token'],
            'application_id': req.client.id
        })

        #if 'refresh_token' in token:
        #    refresh_token = RefreshToken(
        #        user=req.user,
        #        token=token['refresh_token'],
        #        application=req.client,
        #        access_token=access_token
        #    )
        #    refresh_token.save()

        # TODO check out a more reliable way to communicate expire time to oauthlib
        token['expires_in'] = ACCESS_TOKEN_EXPIRE_SECONDS

    def validate_bearer_token(self, token, scopes, req):
        """
        When users try to access resources, check that provided token is valid
        """
        if not token:
            return False

        access_token_obj = request.registry['oauth.access_token']
        access_token_id = access_token_obj.search(request.cr, SUPERUSER_ID,
                                               [('token','=',token)])
        if not access_token_id:
            return False
        access_token_id = access_token_id[0]
        access_token = access_token_obj.browse(request.cr, SUPERUSER_ID, access_token_id)
        if access_token.is_valid(scopes):
            req.client = access_token.application_id
            req.user = access_token.user_id
            req.scopes = scopes

            return True
        return False


validator = OAuth2Validator()
server = MobileApplicationServer(validator)
