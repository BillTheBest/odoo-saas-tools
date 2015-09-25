# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (c) 2014 - Present All Rights Reserved
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

from openerp import SUPERUSER_ID
from openerp import models


class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    def init(self, cr, force=False):
        super(IrConfigParameter, self).init(cr, force=force)
        if force:
            IMD = self.pool['ir.model.data']
            oauth_oe = IMD.xmlid_to_object(cr, SUPERUSER_ID,
                                           'saas_server.saas_oauth_provider')
            dbuuid = self.get_param(cr, SUPERUSER_ID, 'database.uuid')
            oauth_oe.write({'client_id': dbuuid})
