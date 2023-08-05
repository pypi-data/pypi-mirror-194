# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.tools.translate import _


class smp_group_config(models.Model):
    _name = 'smp.sm_group_config'

    name = fields.Char(string=_("Name"), required=True)
    online_shop = fields.Char(string=_("OnlineShop"))

    _order = "name asc"

    def fetch_db_data(self, config_data):
        self.write({
            'online_shop': config_data.get('onlineShop')
        })
