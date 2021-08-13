import xlsxwriter
import datetime
import base64

from odoo import models, fields, api
try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO

class TravelPackage(models.Model):
    _name = 'travel.package'

    name = fields.Char(string='Reference', readonly=True, default='/')
    product_id =fields.Many2one(
        'product.product', 
        string='Produk',
        required=True, 
        readonly=True, 
        states={'draft': [('readonly', False)]}
    )
    departure_date = fields.Date(
            string='Tanggal Keberangkatan',
            required=True, 
            readonly=True, 
            states={'draft': [('readonly', False)]}
        )
    return_date = fields.Date(
            string = "Tanggal Kepulangan",
            required=True, 
            readonly=True, 
            states={'draft': [('readonly', False)]}
        )
    quota = fields.Integer(
            string='Kuota maksimum',
            readonly=True, 
            states={'draft': [('readonly', False)]}
        )
    taken_quota_percentage = fields.Float(
        string = "Quota terambil",
        compute = "_taken_seats",
        readonly=True
    )
    note = fields.Text(string='Catatan')
    hotel_line_ids = fields.One2many(
        comodel_name='hotel.line',
        inverse_name='travel_package_id',
        string='Hotel Lines',
        readonly=True, 
        states={'draft': [('readonly', False)]}
    ) 
    airline_line_ids = fields.One2many(
        comodel_name='airline.line',
        inverse_name='travel_package_id',
        string='Airline Lines',
        readonly=True, 
        states={'draft': [('readonly', False)]}
    )
    acara_line_ids = fields.One2many(
        comodel_name='acara.line',
        inverse_name='travel_package_id',
        string='Schedule Lines',
        readonly=True, 
        states={'draft': [('readonly', False)]}        
    )
    peserta_line_ids = fields.One2many(
        comodel_name='peserta.line',
        inverse_name='travel_package_id',
        string='Jamaah Lines',
        readonly = True,
        states={'draft': [('readonly', False)]}
    )
    state = fields.Selection([
                ('draft', 'Draft'),
                ('confirm', 'Confirmed')
            ], 
            string='Status', readonly=True, copy=False, default='draft', track_visibility='onchange'
        )

    jamaah_data_file = fields.Binary(string='Jamaah Data File')    
    filename = fields.Char(string='Filename')
        

    def update_jamaah(self):
        order_ids = self.env['sale.order'].search([('travel_package_id', '=', self.id), ('state', 'not in', ('draft', 'cancel'))])
        if order_ids:
            self.peserta_line_ids.unlink()
            for order in order_ids:
                for passport in order.passport:
                    peserta_data = {
                        'travel_package_id' : self.id,
                        'res_partner_id': passport.res_partner_id.id,
                        'name': passport.name,
                        'sale_order_id': order.id,
                        'gender': passport.res_partner_id.gender,
                        'room_type': passport.room_type
                    }
                    peserta_data
                    self.peserta_line_ids.create(peserta_data)

    def action_confirm(self):
        self.write({'state': 'confirm'})

    def print_jamaah_xls(self):
		# Membuat Worksheet
        folder_title = self.name + "-" + str(datetime.datetime.now()) + ".xlsx"
        file_data = BytesIO()
        workbook = xlsxwriter.Workbook(file_data)
        ws = workbook.add_worksheet((self.name))  

				# Menambahkan style
        style = workbook.add_format({'left': 1, 'top': 1,'right':1,'bold': True,'fg_color': '#339966','font_color': 'white','align':'center'})
        style.set_text_wrap()
        style.set_align('vcenter')
        style_bold = workbook.add_format({'left': 1, 'top': 1,'right':1,'bottom':1,'bold': True,'align':'center','num_format':'_(Rp* #,##0_);_(Rp* (#,##0);_(* "-"??_);_(@_)'})
        style_bold_orange = workbook.add_format({'left': 1, 'top': 1,'right':1,'bold': True,'align':'center','fg_color': '#FF6600','font_color': 'white'})
        style_no_bold = workbook.add_format({'left': 1,'right':1,'bottom':1})
        style_date = workbook.add_format({'left': 1,'right':1,'bottom':1,'num_format': 'd mmm yyyy'})

        # Membuat Column Header
        ws.merge_range('A1:D1',  "Data Jamaah")
        ws.set_column(1, 1, 10)
        ws.set_column(1, 2, 40)
        ws.set_column(1, 3, 25)
        ws.set_column(1, 4, 25)
        ws.set_column(1, 5, 25)
        ws.set_column(1, 6, 25)
        ws.set_column(1, 7, 10)
        ws.set_column(1, 8, 40)
        ws.set_column(1, 9, 25)
        ws.set_column(1, 10, 25)
        ws.set_column(1, 11, 25)
        ws.set_column(1, 12, 25)
        ws.set_column(1, 13, 25)
        ws.set_column(1, 14, 25)
        ws.write(3, 0,'NO ', style_bold_orange)
        ws.write(3, 1,'TITLE ', style_bold_orange)
        ws.write(3, 2, 'GENDER', style_bold_orange)
        ws.write(3, 3, 'FULL NAME', style_bold_orange)
        ws.write(3, 4, 'TEMPAT LAHIR', style_bold_orange)
        ws.write(3, 5, 'NO PASSPORT', style_bold_orange)
        ws.write(3, 6, 'PASSPORT ISSUED', style_bold_orange)
        ws.write(3, 7, 'PASSPORT EXPIRED', style_bold_orange)
        ws.write(3, 8, 'IMIGRASI', style_bold_orange)
        ws.write(3, 9, 'MAHRAM', style_bold_orange)        
        ws.write(3, 10, 'USIA', style_bold_orange)
        ws.write(3, 11, 'NIK', style_bold_orange)     
        ws.write(3, 12,'ORDER', style_bold_orange)      
        ws.write(3, 13,'ROOM TYPE', style_bold_orange)  
        ws.write(3, 14,'ALAMAT', style_bold_orange) 

        row_count = 4
        count = 1

				# Mengisi data pada setiap baris & kolom
        for peserta in self.peserta_line_ids:
            peserta_res_partner = peserta.res_partner_id
            partner_passport = self.env['sale.passport'].search([('res_partner_id', '=', peserta_res_partner.id)])
            ws.write(row_count, 0, str(count), style_no_bold)
            ws.write(row_count, 1,peserta_res_partner.title.display_name, style_no_bold)
            ws.write(row_count, 2,peserta_res_partner.gender, style_no_bold)
            ws.write(row_count, 3,peserta_res_partner.name, style_no_bold)
            ws.write(row_count, 4,peserta_res_partner.birth_place, style_no_bold)
            ws.write(row_count, 5, partner_passport.passport_number, style_no_bold)
            ws.write(row_count, 6, partner_passport.passport_issued_date, style_date)
            ws.write(row_count, 7, partner_passport.passport_expire_date, style_date)
            ws.write(row_count, 8, peserta_res_partner.city, style_no_bold)
            ws.write(row_count, 9, peserta_res_partner.mahram.name, style_no_bold)
            ws.write(row_count, 10, peserta_res_partner.age ,style_no_bold)
            ws.write(row_count, 11, peserta_res_partner.no_ktp, style_no_bold)
            ws.write(row_count, 12, peserta.sale_order_id.name, style_no_bold)
            ws.write(row_count, 13, peserta.getRoomType(peserta.room_type), style_no_bold)
            ws.write(row_count, 14, peserta_res_partner.street ,style_no_bold)
            count+=1
            row_count+=1

        row_count+=3
        ws.write(row_count, 2,'NO ', style_bold_orange)
        ws.write(row_count, 3,'AIRLINES ', style_bold_orange)
        ws.write(row_count, 4, 'DEPARTURE DATE', style_bold_orange)
        ws.write(row_count, 5, 'DEPARTURE CITY', style_bold_orange)
        ws.write(row_count, 6, 'ARRIVAL CITY', style_bold_orange)
        row_count+=1
        count = 1
        for airline in self.airline_line_ids:
            ws.write(row_count, 2, str(count) , style_no_bold)
            ws.write(row_count, 3,airline.partner_id.name , style_no_bold)
            ws.write(row_count, 4, airline.departure_date, style_date)
            ws.write(row_count, 5, airline.departure_city, style_no_bold)
            ws.write(row_count, 6, airline.arrival_city, style_no_bold)


				# Menyimpan data di field data_file
        workbook.close()        
        out = base64.encodestring(file_data.getvalue())
        self.write({'jamaah_data_file': out, 'filename': folder_title})

        return self.view_form()

    def view_form(self):        
        view = self.env.ref('travel_umroh_fadhil.jamaah_excel_report_wizard_form')
        return {
            'name': ('Jamaah EXCEL export'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'travel.package',
            'views': [(view.id, 'form')],
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        } 

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('travel.package')
        return super(TravelPackage, self).create(vals)   

    def name_get(self):
        return [(this.id, this.name + "#" + " " + this.product_id.partner_ref) for this in self]
    
    @api.depends('quota', 'peserta_line_ids')
    def _taken_seats(self):
        for r in self:
            if not r.quota:
                r.taken_quota_percentage = 0.0
            else:
                r.taken_quota_percentage = 100.0 * len(r.peserta_line_ids) / r.quota