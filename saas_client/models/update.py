# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (c) 2015 - Present All Rights Reserved
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

from openerp.models import AbstractModel
from openerp.tools.config import config

class publisher_warranty_contract(AbstractModel):
    _inherit = "publisher_warranty.contract"

    def update_notification(self, cr, uid, ids, cron_mode=True, context=None):
        url = self.pool['ir.config_parameter'].get_param(cr, uid, 'saas_client.publisher_warranty_url')
        print 'update_notification', url
        if not url:
            return
        config.options["publisher_warranty_url"] = url

        return super(publisher_warranty_contract, self).update_notification(cr, uid, ids, cron_mode, context)
