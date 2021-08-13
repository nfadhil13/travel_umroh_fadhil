from odoo import models, fields, api

class PesertaLine(models.Model):
    _name = 'peserta.line'

    room_type_map = {"d": "Sachin Double",  "t": "Triple", "q": "Quad"}

    travel_package_id = fields.Many2one('travel.package', string='Paket Perjalanan', ondelete='cascade')
    res_partner_id = fields.Many2one('res.partner', string='Jamaah')
    name = fields.Char(string='Nama di Passport')
    sale_order_id = fields.Many2one('sale.order', string='Sales Orders')
    gender = fields.Selection([('pria', 'Man'), ('wanita', 'Woman')], string='Jenis Kelamin')
    room_type = fields.Selection([('d', 'Double'), ('t', 'Triple'), ('q', 'Quad')], string='Tipe Kamar')
    
    def getRoomType(self, value):
        return self.room_type_map[value]
    
