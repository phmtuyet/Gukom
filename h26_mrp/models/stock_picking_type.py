# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    pack_production = fields.Boolean(string='Packing Production')
    package_type_id = fields.Many2one('stock.package.type',
                                      string='Package Type')
    backorder_strategy_mo = fields.Selection([
        ('manual', 'Manual'),
        ('create', 'Create'),
        ('no_create', 'No Create')], string="Backorder Strategy MO",
        default='manual')
    stay_on_finished_mo = fields.Boolean(
        string='Stay on Finished MO',
        default=True,
        help="Stay on Finished MO after create Backorder"
    )
