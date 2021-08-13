from odoo import models, fields, api

class AcaraLine(models.Model):
    _name = 'acara.line'

    travel_package_id = fields.Many2one('travel.package', string='Paket perjalanan', ondelete='cascade')
    name = fields.Char(string='Nama', required=True)
    date = fields.Date(string='Tanggal', required=True)

