/** @odoo-module */
import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";
import { KanbanRecord } from "@web/views/kanban/kanban_record";

patch(KanbanRecord.prototype, {
    events: Object.assign({}, KanbanRecord.prototype.events, {
        'click .show_task_events': '_onShowTaskEventsClick',
    }),
    _onShowTaskEventsClick(event) {
        event.stopPropagation();
        const recordId = this.props.record.id.raw_value;
        this.trigger_up('do_action', {
            action: {
                type: 'ir.actions.act_window',
                res_model: 'autonomous.maintenance.task.event',
                view_mode: 'kanban,tree,form,calendar',
                views: [[false, 'kanban'], [false, 'tree'], [false, 'form'], [false, 'calendar']],
                domain: [['equipment_id', '=', recordId]],
                target: 'current',
            },
        });
    },
});

registry.category("views").add("autonomous_maintenance_task_event_kanban.KanbanView", KanbanRecord);
