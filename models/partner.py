# -*- coding: utf-8 -*-, api
from odoo import fields, models


class Partner(models.Model):
    _name = 'open_academy_vietlai.partner'
    _description = 'Partner'

    name = fields.Char()

    instructor = fields.Boolean(default=False)
    session_ids = fields.Many2many('open_academy_vietlai.session', string="Attended Sessions", readonly=True)
