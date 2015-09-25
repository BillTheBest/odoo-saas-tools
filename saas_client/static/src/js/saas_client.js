/*
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
*/
openerp.saas_client = function(instance){
    var _t = instance.web._t,
       _lt = instance.web._lt;

    instance.web.WebClient.include({
        _ab_location: function(dbuuid) {
            var ab_register = _.str.sprintf('%s/%s', this._ab_register_value, dbuuid);
            $('#announcement_bar_table').find('.url a').attr('href', ab_register);
            return _.str.sprintf(this._ab_location_value, dbuuid);
        },
        show_annoucement_bar: function(){
            var self = this;
            var config_parameter = new instance.web.Model('ir.config_parameter');
            var _super = self._super;
            return config_parameter.call('search_read', [[['key', 'in', ['saas_client.ab_location', 'saas_client.ab_register']]], ['key', 'value']]).then(function(res) {
                _.each(res, function(r){
                    if (r.key == 'saas_client.ab_location'){
                        self._ab_location_value = r.value;
                    } else if (r.key == 'saas_client.ab_register'){
                        self._ab_register_value = r.value;
                    }
                })
                if (!self._ab_location_value)
                    return;
                _super.apply(self);
        })
        }
    })
}