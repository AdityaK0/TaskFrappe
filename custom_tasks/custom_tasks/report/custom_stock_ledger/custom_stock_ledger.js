// Copyright (c) 2024, aditya and contributors
// For license information, please see license.txt

frappe.query_reports["Custom Stock Ledger"] = {
    "filters": [
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_user_default("Company"),
            "reqd": 1
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "warehouse",
            "label": __("Warehouse"),
            "fieldtype": "Link",
            "options": "Warehouse"
        },
        {
            "fieldname": "item_code",
            "label": __("Item"),
            "fieldtype": "Link",
            "options": "Item",
            // "get_query": function() {
            //     return {
            //         query: "erpnext.controllers.queries.item_query"
            //     }
            // }
        },
        // {
        //     "fieldname": "item_group",
        //     "label": __("Item Group"),
        //     "fieldtype": "Link",
        //     "options": "Item Group"
        // },
        // {
        //     "fieldname": "include_zero_qty",
        //     "label": __("Include Zero Quantity"),
        //     "fieldtype": "Check",
        //     "default": 0
        // }
    ],
    "onload":function(report){
        report.page.add_inner_button(__('Download Excel Report'), function() {
            const filters = report.get_values(); 
            
                    frappe.call({
                        method: "custom_tasks.custom_tasks.report.custom_stock_ledger.custom_stock_ledger.downloadExcel",
                        args: {
                            filters: filters
                        },
                        callback: function (r) {
                            
                            if (r.message!=0) {
     
                                const link = document.createElement('a');
                                link.href = `data:application/pdf;base64,${r.message.file_base64}`;
                                link.download = r.message.filename;
                                document.body.appendChild(link);
                                link.click();
                                document.body.removeChild(link);
    
                            }
                            else
                            {
                                console.log("Can't Download the excel because of NO DATA !!!!")
                            }
                        }
                    });
    
    
                  
              
        });
    }
};