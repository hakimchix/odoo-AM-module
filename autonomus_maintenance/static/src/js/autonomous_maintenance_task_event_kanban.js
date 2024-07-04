odoo.define('autonomous_maintenance.TaskEventKanban', function (require) {
    "use strict";

    var KanbanRecord = require('web.KanbanRecord');
    var rpc = require('web.rpc');

    KanbanRecord.include({
        events: _.extend({}, KanbanRecord.prototype.events, {
            'click .btn-primary': '_onCompleteClick',
            'click .btn-warning': '_onNextStageClick',
        }),

        _onCompleteClick: function (event) {
            var self = this;
            var recordId = $(event.currentTarget).data('id');
            rpc.query({
                model: 'autonomous.maintenance.task.event',
                method: 'kanban_quick_action',
                args: ['mark_as_complete', recordId],
            }).then(function (result) {
                self.trigger_up('kanban_record_update', {id: recordId});
            });
        },

        _onNextStageClick: function (event) {
            var self = this;
            var recordId = $(event.currentTarget).data('id');
            rpc.query({
                model: 'autonomous.maintenance.task.event',
                method: 'kanban_quick_action',
                args: ['move_to_next_stage', recordId],
            }).then(function (result) {
                self.trigger_up('kanban_record_update', {id: recordId});
            });
        },
    });
});
