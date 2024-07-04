# -*- coding: utf-8 -*-
# from odoo import http


# class AutonomusMaintenance(http.Controller):
#     @http.route('/autonomus_maintenance/autonomus_maintenance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/autonomus_maintenance/autonomus_maintenance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('autonomus_maintenance.listing', {
#             'root': '/autonomus_maintenance/autonomus_maintenance',
#             'objects': http.request.env['autonomus_maintenance.autonomus_maintenance'].search([]),
#         })

#     @http.route('/autonomus_maintenance/autonomus_maintenance/objects/<model("autonomus_maintenance.autonomus_maintenance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('autonomus_maintenance.object', {
#             'object': obj
#         })

