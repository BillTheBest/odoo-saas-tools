# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (c) 2015 - Present All Rights Reserved
#    Author: Ivan Yelizariev  <yelizariev@it-projects.info>
#    Author: D.H. Bahr <dhbahr@gmail.com>
#    Author: Carlos Almeida <carlos.almeida@thinkopensolutions.com.br>
#    Author: José Andrés Hernández Bustio <jbustio@gmail.com>
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

import openerp
from openerp import models, fields, api
from openerp.addons.saas_utils import connector, database
from openerp import http
from contextlib import closing

class SaasPricingPrice(models.Model):
    _name = 'saas_pricing.price'
    
    name = fields.Char('Price name')
    interval = fields.Char('Price interval')
    price = fields.Float('Price', digits=(16,2))
    stripe_planid = fields.Char('Stripe Plan id')
    stripe_currency = fields.Many2one('res.currency')
    trial_period_days = fields.Char('Stripe trial period days')
    
class SaasPricingPlan(models.Model):
    _inherit = 'saas_portal.plan'
    
    pricing_ids = fields.Many2many('saas_pricing.price', 'saas_pricing_plan')
    
    
