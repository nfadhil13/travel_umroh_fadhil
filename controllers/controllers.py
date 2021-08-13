# -*- coding: utf-8 -*-
# from odoo import http


# class TravelUmrohFadhil(http.Controller):
#     @http.route('/travel_umroh_fadhil/travel_umroh_fadhil/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/travel_umroh_fadhil/travel_umroh_fadhil/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('travel_umroh_fadhil.listing', {
#             'root': '/travel_umroh_fadhil/travel_umroh_fadhil',
#             'objects': http.request.env['travel_umroh_fadhil.travel_umroh_fadhil'].search([]),
#         })

#     @http.route('/travel_umroh_fadhil/travel_umroh_fadhil/objects/<model("travel_umroh_fadhil.travel_umroh_fadhil"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('travel_umroh_fadhil.object', {
#             'object': obj
#         })
