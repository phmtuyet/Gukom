# -*- coding: utf-8 -*-

from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    package_id = fields.Many2one('stock.quant.package', string='Package')

    def action_print_package_label(self):
        return self.env.ref(
            'stock.action_report_quant_package_barcode').report_action(self)

    def button_mark_done(self):
        res = super().button_mark_done()
        # Put in pack production
        for record in self:
            if record.state == 'done':
                if record.picking_type_id.pack_production:
                    record.action_put_in_pack()
        return res

    def action_put_in_pack(self):
        # Put pack all move finish production
        self.ensure_one()
        package = self.env['stock.quant.package'].create(
            {'package_type_id': self.picking_type_id.package_type_id.id})
        self.move_finished_ids.move_line_ids.write(
            {'result_package_id': package.id})
        self.package_id = package.id
