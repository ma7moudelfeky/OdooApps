# -*- coding: utf-8 -*-
from odoo import http

# class JcbLeaveLimit(http.Controller):
#     @http.route('/jcb_leave_limit/jcb_leave_limit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/jcb_leave_limit/jcb_leave_limit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('jcb_leave_limit.listing', {
#             'root': '/jcb_leave_limit/jcb_leave_limit',
#             'objects': http.request.env['jcb_leave_limit.jcb_leave_limit'].search([]),
#         })

#     @http.route('/jcb_leave_limit/jcb_leave_limit/objects/<model("jcb_leave_limit.jcb_leave_limit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('jcb_leave_limit.object', {
#             'object': obj
#         })