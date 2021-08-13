from odoo import models, fields, api

class SaleDocument(models.Model):
    _name = 'sale.document'

    name = fields.Char(string='Nama', required=True)
    sale_order_id = fields.Many2one('sale.order', string='Sale Orders', ondelete='cascade')
    photo = fields.Binary(string='Foto', required=True)