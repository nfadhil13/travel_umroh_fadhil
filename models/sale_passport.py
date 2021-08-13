from odoo import models, fields, api

class SaleDokumen(models.Model):
    _name = 'sale.passport'

    name = fields.Char(string='Nama dalam Passport')
    sale_order_id = fields.Many2one('sale.order', string='Sales Orders', ondelete='cascade')
    res_partner_id = fields.Many2one('res.partner', string='Jamaah', required=False)
    passport_number = fields.Char(string='Nomor Passport')
    passport_issued_date = fields.Date(string='Tanggal Password mulai berlaku', required=True)
    passport_expire_date = fields.Date(string='Masa berlaku Passport (sampai)', required=True)
    room_type = fields.Selection(
            [
                ("d","Doube "),
                ("t","Triple"),
                ("q", "Quad")
            ], 
            string='Room Type',
            required=True
        )
    photo = fields.Binary(string='Photo', required=True)