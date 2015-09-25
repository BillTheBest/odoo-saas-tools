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

import werkzeug
from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.addons.web.controllers.main import login_redirect
from openerp.addons.saas_portal.controllers.main import SaasPortal


def signup_redirect():
    url = '/web/signup?'
    redirect_url = '%s?%s' % (request.httprequest.base_url, werkzeug.urls.url_encode(request.params))
    return """<html><head><script>
        window.location = '%sredirect=' + encodeURIComponent("%s");
    </script></head></html>
    """ % (url, redirect_url)


class SaasPortalDemo(SaasPortal):

    @http.route(['/demo/<string:version>/<string:plan_url>'], type='http', auth='public', website=True)
    def show_plan(self, version, plan_url, **post):
        domain = [('odoo_version', '=', version), ('page_url', '=', plan_url),
                  ('state', '=', 'confirmed')]
        plan = request.env['saas_portal.plan'].sudo().search(domain)
        if not plan:
            # TODO: maybe in this case we can redirect to saas_portal_templates.select_template
            return request.website.render("saas_portal_demo.unavailable_plan")
        values = {'plan': plan[0]}
        return request.website.render("saas_portal_demo.show_plan", values)

    @http.route('/demo/new_database', type='http', auth='public', website=True)
    def new_demo_database(self, **post):
        if not request.session.uid:
            return signup_redirect()
        plan_id = int(post.get('plan_id'))

        return self.create_new_database(plan_id)
