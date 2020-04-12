""" Leave Type """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class HrLeaveType(models.Model):
    """ inherit Hr Leave Type """
    _inherit = 'hr.leave.type'

    monthly_leave_limit = fields.Boolean()
    leave_limit = fields.Float()



