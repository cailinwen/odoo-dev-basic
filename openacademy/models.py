# -*- coding: utf-8 -*-

from openerp import models, fields, api

class openacademy(models.Model):
    _name = 'openacademy.openacademy'

    name = fields.Char()


class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string="标题", required=True,help="name required",index=True)
    description = fields.Text(string="描述")
    responsible_id = fields.Many2one('res.users',
        ondelete='set null', string="Responsible", index=True)

    session_ids = fields.One2many(
        'openacademy.session', 'course_id', string="Sessions")


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")

    instructor_id = fields.Many2one('res.partner', string="Instructor")
    course_id = fields.Many2one('openacademy.course',
        ondelete='cascade', string="Course", required=True)

    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats



class SessionExtension(models.Model):
    _inherit = 'openacademy.session'
    note = fields.Text()


class SessionCopy(models.Model):
    _name = 'openacademy.session.copy'
    _inherit = 'openacademy.session'
    copy = fields.Text()



class Child0(models.Model):
    _name = 'delegation.child0'

    field_0 = fields.Integer()

class Child1(models.Model):
    _name = 'delegation.child1'

    field_1 = fields.Integer()

class Delegating(models.Model):
    _name = 'delegation.parent'

    _inherits = {
        'delegation.child0': 'child0_id',
        'delegation.child1': 'child1_id',
    }

    child0_id = fields.Many2one('delegation.child0', required=True, ondelete='cascade')
    child1_id = fields.Many2one('delegation.child1', required=True, ondelete='cascade')
