
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'



    no_ktp = fields.Char(string='No KTP')
    father_name = fields.Char(string="Nama Ayah")
    mother_name = fields.Char(string="Nama Ibu")
    birth_place = fields.Char(string='Tempat Lahir')
    birth_date = fields.Date(string='Tanggal Lahir')
    mahram = fields.Many2one('res.partner', string='Mahram', required=False, domain=[("is_company", "=", "True")])
    age = fields.Integer(
        string='Umur',
        compute='_compute_age',
        store=False,
    )
    blood_type = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O')
    ],
        string='Golongan darah'
    )
    gender = fields.Selection([
        ('pria', 'Man'),
        ('wanita', 'Woman')
    ],
        string='Jenis Kelamin'
    )
    status = fields.Selection([
        ('belum', 'Single'),
        ('nikah', 'Married'),
        ('cerai', 'Divorce')
    ],
        string='Status'
    )

    @api.depends('birth_date')
    def _compute_age(self):
        today = fields.Date.today()
        for res_partner in self:
            if res_partner.birth_date:
                delta = today - res_partner.birth_date
                res_partner.age = int (delta.days / 365)
            else:
                res_partner.age = 0
