# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (c) 2015 - Present All Rights Reserved
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

import requests
import werkzeug
import datetime
import simplejson

import openerp
from openerp.addons.saas_utils import connector, database
from openerp.addons.web.http import request
from openerp.tools import config
from openerp import models, fields, api, SUPERUSER_ID
from openerp import http


class SaasConfig(models.TransientModel):
    _name = 'saas.config'

    def _default_database_id(self):
        return self._context.get('active_id')

    action = fields.Selection([('edit', 'Edit'), ('upgrade', 'Configure'), ('delete', 'Delete')],
                                'Action')
    database_id = fields.Many2one('saas_portal.client', string='Database', default=_default_database_id)
    server_id = fields.Many2one('saas_portal.server', string='Server', related='database_id.server_id', readonly=True)
    update_addons = fields.Char('Update Addons', size=256)
    install_addons = fields.Char('Install Addons', size=256)
    uninstall_addons = fields.Char('Uninstall Addons', size=256)
    fix_ids = fields.One2many('saas.config.fix', 'config_id', 'Fixes')
    param_ids = fields.One2many('saas.config.param', 'config_id', 'Parameters')
    description = fields.Text('Result')

    @api.multi
    def execute_action(self):
        res = False
        method = '%s_database' % self.action
        if hasattr(self, method):
            res = getattr(self, method)()
        return res

    @api.multi
    def delete_database(self):
        return self.database_id.delete_database()

    @api.multi
    def upgrade_database(self):
        obj = self[0]
        scheme = request.httprequest.scheme
        payload = {
            'update_addons': (obj.update_addons or '').split(','),
            'install_addons': (obj.install_addons or '').split(','),
            'uninstall_addons': (obj.uninstall_addons or '').split(','),
            'fixes': [[x.model, x.method] for x in obj.fix_ids],
            'params': [[x.key, x.value] for x in obj.param_ids],
        }
        state = {
            'data': payload,
        }
        url = self.server_id._request_server(
            path='/saas_server/upgrade_database',
            client_id=self.database_id.client_id,
            state=state,
        )[0]
        res = requests.get(url, verify=(self.server_id.request_scheme == 'https' and self.server_id.verify_ssl))
        if res.ok != True:
            msg = """Status Code - %s
Reason - %s
URL - %s
            """ % (res.status_code, res.reason, res.url)
            raise Warning(msg)
        obj.write({'description': res.text})
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'saas.config',
            'res_id': obj.id,
            'target': 'new'
        }


class SaasConfigFix(models.TransientModel):
    _name = 'saas.config.fix'

    model = fields.Char('Model', required=1, size=64)
    method = fields.Char('Method', required=1, size=64)
    config_id = fields.Many2one('saas.config', 'Config')

class SaasConfigParam(models.TransientModel):
    _name = 'saas.config.param'

    def _get_keys(self):
        return [
            ('saas_client.max_users', 'Max Users'),
        ]

    key = fields.Selection(selection=_get_keys, string='Key', required=1, size=64)
    value = fields.Char('Value', required=1, size=64)
    config_id = fields.Many2one('saas.config', 'Config')

class SaasPortalCreateClient(models.TransientModel):
    _name = 'saas_portal.create_client'

    def _default_plan_id(self):
        return self._context.get('active_id')

    def _default_name(self):
        plan_id = self._default_plan_id()
        if plan_id:
            plan = self.env['saas_portal.plan'].browse(plan_id)
            return plan.generate_dbname(raise_error=False)[0]
        return ''

    name = fields.Char('Database name', required=True, default=_default_name)
    plan_id = fields.Many2one('saas_portal.plan', string='Plan', readonly=True, default=_default_plan_id)
    partner_id = fields.Many2one('res.partner', string='Partner')

    @api.multi
    def apply(self):
        wizard = self[0]
        url = wizard.plan_id.create_new_database(dbname=wizard.name, partner_id=wizard.partner_id.id)
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'name': 'Create Client',
            'url': url
        }


class SaasPortalDuplicateClient(models.TransientModel):
    _name = 'saas_portal.duplicate_client'

    def _default_client_id(self):
        return self._context.get('active_id')

    def _default_partner(self):
        client_id = self._default_client_id()
        if client_id:
            client = self.env['saas_portal.client'].browse(client_id)
            return client.partner_id
        return ''
    
    def _default_expiration(self):
        client_id = self._default_client_id()
        if client_id:
            client = self.env['saas_portal.client'].browse(client_id)
            return client.plan_id.expiration
        return ''

    name = fields.Char('Database Name', required=True)
    client_id = fields.Many2one('saas_portal.client', string='Base Client', readonly=True, default=_default_client_id)
    expiration = fields.Integer('Expiration', default=_default_expiration)
    partner_id = fields.Many2one('res.partner', string='Partner', default=_default_partner)

    @api.multi
    def apply(self):
        wizard = self[0]
        url = wizard.client_id.duplicate_database(dbname=wizard.name, partner_id=wizard.partner_id.id, expiration=None)
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'name': 'Duplicate Client',
            'url': url
        }
