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
