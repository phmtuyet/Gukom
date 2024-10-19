# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    pack_production = fields.Boolean(string='Packing Production')
    package_type_id = fields.Many2one('stock.package.type',
                                      string='Package Type')
