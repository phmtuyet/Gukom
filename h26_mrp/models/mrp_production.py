# -*- coding: utf-8 -*-

from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    package_id = fields.Many2one('stock.quant.package', string='Package',
                                 copy=False)

    def action_print_package_label(self):
        return self.env.ref(
            'stock.action_report_quant_package_barcode').report_action(
            self.package_id)

    def button_mark_done(self):
        ctx = self.env.context.copy()
        # Backorder Strategy
        # no_create: no create Backorder MO
        # create: auto create Backorder MO
        if 'no_create' in self.picking_type_id.mapped('backorder_strategy_mo'):
            ctx.update({'skip_backorder': True})
        elif 'create' in self.picking_type_id.mapped('backorder_strategy_mo'):
            quantity_issues = self._get_quantity_produced_issues()
            mo_ids_to_backorder = self.env['mrp.production']
            for order in quantity_issues:
                mo_ids_to_backorder |= order
            ctx.update({'auto_create_backorder': True,
                        'mo_ids_to_backorder': mo_ids_to_backorder.ids})
        res = super(MrpProduction, self.with_context(ctx)).button_mark_done()
        # Put in pack production
        for record in self:
            if record.state == 'done':
                if record.picking_type_id.pack_production:
                    record.action_put_in_pack()
        # Denied return BackOrder Form view after created
        if (isinstance(res, dict)
                and res.get('res_model') == 'mrp.production'
                and True in self.picking_type_id.mapped('stay_on_finished_mo')):
            return True
        return res

    def action_put_in_pack(self):
        # Put pack all move finish production
        self.ensure_one()
        package = self.env['stock.quant.package'].create(
            {'package_type_id': self.picking_type_id.package_type_id.id})
        self.move_finished_ids.move_line_ids.write(
            {'result_package_id': package.id})
        self.package_id = package.id

    def _action_generate_backorder_wizard(self, quantity_issues):
        # Denied show popup create backorder with auto create
        if self._context.get('auto_create_backorder'):
            return True
        return super(MrpProduction, self)._action_generate_backorder_wizard(
            quantity_issues)
