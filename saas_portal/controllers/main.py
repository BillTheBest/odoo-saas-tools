# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (c) 2014 - Present All Rights Reserved
#    Author: Ivan Yelizariev  <yelizariev@it-projects.info>
#    Author: Cesar Lage <kaerdsar@gmail.com>
#    Author: D.H. Bahr <dhbahr@gmail.com>
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

from ast import literal_eval
import openerp
from openerp import SUPERUSER_ID, exceptions
from openerp.tools.translate import _
from openerp.addons.web import http
from openerp.addons.web.http import request
import werkzeug
import simplejson


class SignupError(Exception):
    pass


class SaasPortal(http.Controller):

    @http.route(['/saas_portal/trial_check'], type='json', auth='public', website=True)
    def trial_check(self, **post):
        if self.exists_database(post['dbname']):
            return {"error": {"msg": "database already taken"}}
        return {"ok": 1}

    @http.route(['/saas_portal/add_new_client'], type='http', auth='public', website=True)
    def add_new_client(self, **post):
        dbname = self.get_full_dbname(post.get('dbname'))
        plan = self.get_plan(post.get('plan_id'))
        url = plan.create_new_database(dbname)[0]
        return werkzeug.utils.redirect(url)

    def get_config_parameter(self, param):
        config = request.registry['ir.config_parameter']
        full_param = 'saas_portal.%s' % param
        return config.get_param(request.cr, SUPERUSER_ID, full_param)

    def get_full_dbname(self, dbname):
        full_dbname = '%s.%s' % (dbname, self.get_config_parameter('base_saas_domain'))
        return full_dbname.replace('www.', '')

    def get_plan(self, plan_id=None):
        plan = request.registry['saas_portal.plan']
        if not plan_id:
            domain = [('state', '=', 'confirmed')]
            plan_ids = request.registry['saas_portal.plan'].search(request.cr, SUPERUSER_ID, domain)
            if plan_ids:
                plan_id = plan_ids[0]
            else:
                raise exceptions.Warning(_('There is no plan configured'))
        return plan.browse(request.cr, SUPERUSER_ID, plan_id)

    def exists_database(self, dbname):
        full_dbname = self.get_full_dbname(dbname)
        return openerp.service.db.exp_db_exist(full_dbname)

    @http.route(['/publisher-warranty/'], type='http', auth='public', website=True)
    def publisher_warranty(self, **post):
        # check addons/mail/update.py::_get_message for arg0 value
        arg0 = post.get('arg0')
        if arg0:
            arg0 = literal_eval(arg0)
        messages = []
        return simplejson.dumps({'messages':messages})
