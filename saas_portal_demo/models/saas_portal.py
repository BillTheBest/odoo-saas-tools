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

from openerp import models, fields, api


class SaasPortalPlan(models.Model):
    _name = 'saas_portal.plan'
    _inherit = 'saas_portal.plan'
    
    page_url = fields.Char('Page URL', placeholder='some-name')
    odoo_version = fields.Char('Odoo Version', placeholder='8.0')
    app_store_module_ids = fields.Many2many('saas_portal.module',
                                            'saas_portal_plan_module',
                                            'plan_id', 'module_id',
                                            'Modules')


class SaaSPortalModule(models.Model):
    _name = 'saas_portal.module'
    
    name = fields.Char('Name')
    technical_name = fields.Char('Technical Name')
    summary = fields.Text('Summary')
    author = fields.Char('Author')
    url = fields.Char('URL')
    module_id = fields.Many2one('ir.module.module', required=False)
    
    @api.onchange('module_id')
    def onchange_module_id(self):
        if self.module_id:
            self.name = self.module_id.shortdesc
            self.technical_name = self.module_id.name
            self.summary = self.module_id.summary
            self.author = self.module_id.author
            self.url = self.module_id.url
        else:
            self.name, self.technical_name, self.summary, self.author, self.url  = [False] * 5
            
    _sql_constraints = [
        ('technical_name_uniq', 'unique(technical_name)', 'The module already exists!'),
    ]
