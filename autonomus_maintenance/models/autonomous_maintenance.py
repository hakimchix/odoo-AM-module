from datetime import timedelta
from odoo import models, fields, api

class AutonomousMaintenanceTaskEvent(models.Model):
    _name = 'autonomous.maintenance.task.event'
    _description = 'Autonomous Maintenance Task Event'

    task_id = fields.Many2one('autonomous.maintenance.task', 'Maintenance Task', required=True)
    scheduled_date = fields.Date('Scheduled Date', required=True)
    state = fields.Selection([('pending', 'Pending'), ('OK', 'OK'),('NOK', 'NOK'), ('missed', 'Missed')], 'Status', default='pending')
    date_completed = fields.Date('Completion Date')
    equipment_id = fields.Many2one(related='task_id.equipment_id', string='Equipment', store=True)
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Very High')
    ], 'Priority', default='1')
    user_id = fields.Many2one(related='task_id.equipment_id.owner_user_id', string='Assigned to', store=True)

    @api.model
    def kanban_getcolor(self, state):
        colors = {
            'pending': 0,  # Default color (grey)
            'OK': 10,      # Green
            'NOK': 1,      # Red
            'missed': 2    # Brown
        }
        return colors.get(state, 0) 
    
    

    @api.model
    def update_missed_tasks(self):
        events = self.search([('state', '=', 'pending')])
        for event in events:
            if event.scheduled_date + timedelta(days=event.task_id.frequency_days // 3) < fields.Date.today():
                event.write({'state': 'missed'}) 
    @api.model
    def create_events(self):
        tasks = self.env['autonomous.maintenance.task'].search([])
        for task in tasks:
            next_date = task.next_event_date
            while next_date <= fields.Date.today() + timedelta(days=30):  # Adjust as needed for how far in advance to schedule
                self.create({
                    'task_id': task.id,
                    'scheduled_date': next_date,
                    'state': 'pending',
                })
                next_date += timedelta(days=task.frequency_days)

    @api.model
    def write(self, vals):
     res = super(AutonomousMaintenanceTaskEvent, self).write(vals)
     for event in self:
        if event.exists():  # Check if the record exists before proceeding
            if 'state' in vals:
                if vals['state'] in ['OK', 'NOK']:
                   
                    event.date_completed = fields.Date.today()
                  
                
        else:
            # Handle the case where the record does not exist
            # You can log an error or take appropriate action here
            pass
     return res



class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    task_event_ids = fields.One2many('autonomous.maintenance.task.event', 'equipment_id', string='Task Events')
    
   
    def open_autonomous_maintenance_task_event_action(self):
   

     action = self.env.ref('autonomus_maintenance.autonomous_maintenance_task_event_action')  # Replace with your actual action reference
     if action:
        action['domain'] = [('equipment_id', '=', self.id)]  # Filter events for this equipment
        action['context'] = dict(self._context, active_id=self.id)  # Pass equipment ID

     return action

    def open_task_events(self):
        """
        Opens a form view to display all task events for the current equipment.
        """

        action = self.env.ref('autonomus_maintenance.view_task_event_kanban_action')  # Replace with actual values
        action['domain'] = [('equipment_id', '=', self.id)]  # Filter by current equipment
        action['context'] = dict(self._context, active_id=self.id)  # Pass equipment ID
        #print(action.domain,action.context)

        return {
            'type': 'ir.actions.act_window',
            'name': ('tasks event by equipement'),
            'view_mode': 'kanban,tree,calendar',
            'res_model': 'autonomous.maintenance.task.event',
            'views': [(False, 'kanban'), (False, 'tree'), (False, 'calendar')],
            'view_id': 'view_task_event_kanban',
            'domain': [('equipment_id', '=', self.id)],
            #'target': 'new',
            'context':  dict(self._context, active_id=self.id),
        }
        #return action