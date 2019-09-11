# -*- coding: utf-8 -*-
from odoo import fields, models


class Course(models.Model):
    _name = 'open_academy_vietlai.course'
    _description = 'Course'

    name = fields.Char(name='Title', required=True)
    description = fields.Text()

    responsible_id = fields.Many2one('open_academy_vietlai.partner', string="Responsible")
    session_ids = fields.One2many('open_academy_vietlai.session', 'course_id', string="Sessions")

    level = fields.Selection([(1, 'Easy'), (2, 'Medium'), (3, 'Hard')], string="Difficulty Level")


class Session(models.Model):
    _name = 'open_academy_vietlai.session'
    _description = 'Session'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection([('draft', "Draft"), ('confirmed', "Confirmed"), ('done', "Done")], default='draft')

    start_date = fields.Date(default=fields.Date.context_today)
    duration = fields.Float(digits=(6, 2), help="Duration in days", default=1)

    instructor_id = fields.Many2one('open_academy_vietlai.partner', string="Instructor")
    course_id = fields.Many2one('open_academy_vietlai.course', ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many('open_academy_vietlai.partner', string="Attendees")
    #them moi
    seats = fields.Integer()

    ###
    ## Using computed fields
    ###
    taken_seats = fields.Float(compute='_compute_taken_seats', store=True)

    @api.depends('seats', 'attendee_ids')
    def _compute_taken_seats(self):
        for session in self:
            if not session.seats:
                session.taken_seats = 0.0
            else:
                session.taken_seats = 100.0 * len(session.attendee_ids) / session.seats

    ###
    ## using onchange
    ###
    @api.onchange('seats', 'attendee_ids')
    def _change_taken_seats(self):
        if self.taken_seats > 100:
            return {'warning': {
                'title':   'Too many attendees',
                'message': 'The room has %s available seats and there is %s attendees registered' % (self.seats, len(self.attendee_ids))
            }}

    ###
    ## using python constrains
    ###
    @api.constrains('seats', 'attendee_ids')
    def _check_taken_seats(self):
        for session in self:
            if session.taken_seats > 100:
                raise exceptions.ValidationError('The room has %s available seats and there is %s attendees registered' % (session.seats, len(session.attendee_ids)))

    ###
    ## using SQL constrains
    ###
    _sql_constraints = [
        # possible only if taken_seats is stored
        ('session_full', 'CHECK(taken_seats <= 100)', 'The room is full'),
    ]