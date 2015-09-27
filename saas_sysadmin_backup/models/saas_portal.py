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

import urllib2
import simplejson
import werkzeug
import requests

from openerp import models, fields, api
from openerp.exceptions import Warning

import logging
_logger = logging.getLogger(__name__)


class SaasPortalClient(models.Model):
    _inherit = 'saas_portal.client'
    
    backup = fields.Boolean('Backup on Modify', help="Backs up first before deleting \
                            or upgrading", default=True)
    
    @api.multi 
    def action_backup(self):
        '''
        call to backup database
        '''
        self.ensure_one()
        if not self[0].backup:
            return
        state = {
            'd': self.name,
            'client_id': self.client_id,
        }

        url = self.server_id._request_server(path='/saas_server/backup_database', state=state, client_id=self.client_id)[0]
        res = requests.get(url, verify=(self.server_id.request_scheme == 'https' and self.server_id.verify_ssl))
        _logger.info('delete database: %s', res.text)
        if res.ok != True:
            msg = """Status Code - %s 
            Reason - %s
            URL - %s
            """ % (res.status_code, res.reason, res.url)
            raise Warning(msg)
        data = simplejson.loads(res.text)
        if data[0]['status'] != 'success':
            warning = data[0].get('message', 'Could not backup database; please check your logs')
            raise Warning(warning)
        return True
    
    @api.multi
    def delete_database(self):
        self.action_backup()
        return super(SaasPortalClient, self).delete_database()
    
 
    @api.multi
    def upgrade_database(self):
        self.action_backup()
        return super(SaasPortalClient, self).upgrade_database()