from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    travel_package_id = fields.Many2one('travel.package', string='Paket perjalanan', domain=[("state", "=", "confirm")],)
    document = fields.One2many(
        comodel_name='sale.document',
        inverse_name='sale_order_id',
        string='Dokumen',
    )
    passport = fields.One2many(
        comodel_name='sale.passport',
        inverse_name='sale_order_id',
        string='passport',
    ) 