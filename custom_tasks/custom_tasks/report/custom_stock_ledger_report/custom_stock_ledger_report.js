// Copyright (c) 2024, aditya and contributors
// For license information, please see license.txt

frappe.query_reports["Custom Stock Ledger Report"] = {
    "onload": function(report) {
        // Add custom button for Excel export
        report.page.add_inner_button(__('Download Excel'), function() {
            report.download("xls");  // Downloads the report as Excel
        });
    }
};
