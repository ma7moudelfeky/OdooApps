""" Hr Leave """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta

class HrLeave(models.Model):
    """ inherit Hr Leave """
    _inherit = 'hr.leave'

    holiday_take = fields.Float(compute='_compute_holiday_take')
    holiday_take_plus_duration = fields.Float(compute='_compute_holiday_take_plus_duration')
    remain_leave = fields.Float(compute='_compute_remain_leave')
    leave_limit = fields.Float(related='holiday_status_id.leave_limit', store=True)
    first_day_month = fields.Date(compute='_compute_first_day_month')
    last_day_month = fields.Date(compute='_compute_first_day_month')

    @api.depends('holiday_take', 'number_of_days_display')
    def _compute_holiday_take_plus_duration(self):
        """ Compute holiday_take_plus_duration value """
        for rec in self:
            rec.holiday_take_plus_duration = rec.holiday_take + rec.number_of_days_display

    @api.depends('holiday_status_id')
    def _compute_holiday_take(self):
        """ Compute holiday_take value """
        for rec in self:
            if rec.holiday_status_id.monthly_leave_limit:
                holiday = rec.env['hr.leave'].search([
                    ('employee_id', '=', rec.employee_id.id),
                    ('holiday_status_id', '=', rec.holiday_status_id.id),
                    ('request_date_from', '>=', rec.first_day_month),
                    ('request_date_to', '<=', rec.last_day_month),
                    ('state', '=', 'validate')
                ])
                for h in holiday:
                    rec.holiday_take += h.number_of_days_display

    @api.depends('request_date_from')
    def _compute_first_day_month(self):
        """ Compute first_day_month value """
        for rec in self:
            rec.first_day_month = rec.request_date_from.replace(day=1)
            rec.last_day_month = (rec.request_date_from + relativedelta(months=+1, day=1,
                                                             days=-1))

    @api.depends('leave_limit', 'holiday_take')
    def _compute_remain_leave(self):
        """ Compute remain_leave value """
        for rec in self:
            rec.remain_leave = rec.leave_limit - rec.holiday_take

    # @api.onchange('holiday_status_id')
    # def _onchange_holiday_status_id(self):
    #     """ holiday_status_id """
    #     for rec in self:
    #         if rec.holiday_status_id.monthly_leave_limit:
    #             if rec.holiday_take_plus_duration > rec.leave_limit:
    #                 raise ValidationError('Your Leave Limit By Month Is :  ' +
    #                                       str(rec.leave_limit) +
    #                                       '\n' + 'You Take :  ' +
    #                                       str(rec.holiday_take) +
    #                                       '\n' + 'Your Available Leaves Is :  ' +
    #                                       str(rec.remain_leave))
    #
    # @api.onchange('request_date_from')
    # def _onchange_request_date_from(self):
    #     """ request_date_from """
    #     for rec in self:
    #         if rec.holiday_status_id.monthly_leave_limit:
    #             if rec.holiday_take_plus_duration > rec.leave_limit:
    #                 raise ValidationError('Your Leave Limit By Month Is :  ' +
    #                                       str(rec.leave_limit) +
    #                                       '\n' + 'You Take :  ' +
    #                                       str(rec.holiday_take) +
    #                                       '\n' + 'Your Available Leaves Is :  ' +
    #                                       str(rec.remain_leave))
    #
    # @api.onchange('request_date_to')
    # def _onchange_request_date_to(self):
    #     """ request_date_to """
    #     for rec in self:
    #         if rec.holiday_status_id.monthly_leave_limit:
    #             if rec.holiday_take_plus_duration > rec.leave_limit:
    #                 raise ValidationError('Your Leave Limit By Month Is :  ' +
    #                                       str(rec.leave_limit) +
    #                                       '\n' + 'You Take :  ' +
    #                                       str(rec.holiday_take) +
    #                                       '\n' + 'Your Available Leaves Is :  ' +
    #                                       str(rec.remain_leave))

    @api.model
    def create(self, vals):
        """ Override create() """
        # vals ={'field': value}  -> dectionary contains only new filled fields
        res = super(HrLeave, self).create(vals)
        for rec in res:
            if rec.holiday_status_id.monthly_leave_limit:
                if rec.holiday_take_plus_duration > rec.leave_limit:
                    raise ValidationError('Your Leave Limit By Month Is :  ' +
                                          str(rec.leave_limit) +
                                          '  .\n' + 'You Take :  ' +
                                          str(rec.holiday_take) +
                                          '  .\n' + 'Your Available Leaves Is :  ' +
                                          str(rec.remain_leave)+
                                          '  .\n' )
        return res
    
    @api.multi
    def action_approve(self):
        """ inherit action_approve() """
        for rec in self:
            if rec.holiday_take_plus_duration > rec.leave_limit:
                    raise ValidationError('Your Leave Limit By Month Is :  ' +
                                          str(rec.leave_limit) +
                                          '  .\n' + 'You Take :  ' +
                                          str(rec.holiday_take) +
                                          '  .\n' + 'Your Available Leaves Is :  ' +
                                          str(rec.remain_leave)+
                                          '  .\n')
        res = super(HrLeave, self).action_approve()

