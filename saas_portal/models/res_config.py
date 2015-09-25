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

from openerp import models, fields
from openerp.addons.web.http import request
import urlparse

class SaasPortalConfigWizard(models.TransientModel):
    _name = 'saas_portal.config.settings'
    _inherit = 'res.config.settings'

    base_saas_domain = fields.Char('Base SaaS domain')

    def get_default_base_saas_domain(self, cr, uid, ids, context=None):
        base_saas_domain = self.pool.get("ir.config_parameter").get_param(cr, uid, "saas_portal.base_saas_domain", default=None, context=context)
        if base_saas_domain is None:
            domain = self.pool.get("ir.config_parameter").get_param(cr, uid, "web.base.url", context=context)
            try:
                base_saas_domain = urlparse.urlsplit(domain).netloc.split(':')[0]
            except Exception:
                pass
        return {'base_saas_domain': base_saas_domain or False}

    def set_base_saas_domain(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "saas_portal.base_saas_domain", record.base_saas_domain or '', context=context)
