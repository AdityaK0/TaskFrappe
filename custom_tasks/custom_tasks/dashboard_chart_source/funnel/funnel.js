frappe.provide('frappe.chart_sources');

frappe.chart_sources['funnel'] = {
    method: 'custom_tasks.create_chart.get_purchase_funnel_chart',

    get: function (chart, args, callback) {
        frappe.call({
            method: this.method,
            args: args,
            callback: function (r) {
                if (r.message) {
                    callback(r.message);
                }
            }
        });
    }
};
