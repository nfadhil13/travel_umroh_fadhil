from odoo import models, fields, api

class PesawatLine(models.Model):
    _name = 'airline.line'

    travel_package_id = fields.Many2one('travel.package', string='Paket Perjalanan', ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Airlines', required=True )
    departure_date = fields.Date(string='Tanggal Keberangkatan')
    departure_city = fields.Char(string='Kota Keberangkatan')
    arrival_city = fields.Char(string='Kota tujuan')

    