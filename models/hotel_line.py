from odoo import models, fields, api

class HotelLine(models.Model):
    _name = 'hotel.line'

    travel_package_id = fields.Many2one(
        'travel.package',
         string='Kasir'
         )
    res_partner_id = fields.Many2one('res.partner',required=True, string = "Hotel", domain=[("is_company", "=", "True")],)
    start_date = fields.Date(string='Tanggal Mulai', required=True)
    end_date = fields.Date(string = "Tanggal Berakhir", required=True)
    city = fields.Char(related = "res_partner_id.city")





    