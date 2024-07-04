from odoo import models, fields, api
from datetime import date, timedelta

class AutonomousMaintenanceTask(models.Model):
    _name = 'autonomous.maintenance.task'
    _description = 'Autonomous Maintenance Task'

    name = fields.Char('Task Name', required=True)
    equipment_id = fields.Many2one('maintenance.equipment', 'Equipment', required=True)
    description = fields.Text('Description')
    frequency_days = fields.Integer('Frequency (Days)', required=True, help="Number of days between each maintenance task.")
    phase = fields.Integer('Phase (Days)', required=True, help="Number of days before the first occurrence.")
    task_mode = fields.Selection([('run', 'Run'), ('down', 'Down')], 'Mode', required=True)
    assigned_user_id = fields.Many2one('res.users', 'Assigned User')
    last_event_date = fields.Date('Last Event Date')
    next_event_date = fields.Date('Next Event Date', compute='_compute_next_event_date', store=True)
    autonomous_maintenance_task_event_ids = fields.One2many('autonomous.maintenance.task.event', 'task_id', string='Task Events')
    
    @api.model
    def create(self, vals):
        task = super(AutonomousMaintenanceTask, self).create(vals)
        task._generate_task_events()
        return task

    def write(self, vals):
        res = super(AutonomousMaintenanceTask, self).write(vals)
        for task in self:
            task._generate_task_events()
        return res
    
    
    @api.depends('last_event_date', 'frequency_days')
    def _compute_next_event_date(self):
        for task in self:
            if task.last_event_date:
                task.next_event_date = task.last_event_date + timedelta(days=task.frequency_days)
            else:
                task.next_event_date = fields.Date.today() + timedelta(days=task.phase)
    def action_complete_task(self):
        for task in self:
            # Mark all pending task events as completed
            pending_events = task.autonomous_maintenance_task_event_ids.filtered(lambda event: event.state == 'pending')
            for event in pending_events:
                event.write({
                    'state': 'completed',
                    'date_completed': fields.Date.today()
                })
            # Update the last event date and calculate the next event date
            task.last_event_date = fields.Date.today()
            task._compute_next_event_date()

    def _generate_task_events(self):
        self.ensure_one()
        today = date.today()
        last_event_date = fields.Date.from_string(self.last_event_date) if self.last_event_date else today

        # Retrieve future task events
        future_events = self.env['autonomous.maintenance.task.event'].search([('task_id', '=', self.id), ('scheduled_date', '>', today)])
        future_event_dates = future_events.mapped('scheduled_date')

        # Create new task events based on the updated schedule
        next_event_date = last_event_date + timedelta(days=self.frequency_days)
        new_events = []
        while next_event_date <= today + timedelta(days=90):  # Generate events for the next year
            if next_event_date not in future_event_dates:
                new_events.append({
                    'task_id': self.id,
                    'scheduled_date': next_event_date,
                    'state': 'pending'
                })
            next_event_date += timedelta(days=self.frequency_days)
        
        # Remove future task events that have different dates
        future_events_to_remove = future_events.filtered(lambda e: e.scheduled_date not in [event['scheduled_date'] for event in new_events])
        future_events_to_remove.unlink()

        # Create new task events
        self.env['autonomous.maintenance.task.event'].create(new_events)
                    
    @api.model
    def create_schedule(self):
        tasks = self.search([])
        for task in tasks:
            next_date = task.next_event_date
            self.env['autonomous.maintenance.task.event'].create({
                'task_id': task.id,
                'scheduled_date': next_date,
            })

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    autonomous_maintenance_task_ids = fields.One2many('autonomous.maintenance.task', 'equipment_id', 'Autonomous Maintenance Tasks')

class AutonomousMaintenanceDefect(models.Model):
    _name = 'autonomous.maintenance.defect'
    _description = 'Autonomous Maintenance Defect'

    name = fields.Char('Defect Name', required=True)
    task_id = fields.Many2one('autonomous.maintenance.task', 'Autonomous Maintenance Task', required=True)
    description = fields.Text('Description')
    detected_date = fields.Date('Detected Date', default=fields.Date.today)
    state = fields.Selection([('new', 'New'), ('in_progress', 'In Progress'), ('resolved', 'Resolved')], 'Status', default='new')
   