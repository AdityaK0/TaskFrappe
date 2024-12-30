# Copyright (c) 2024, aditya and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    # Define the columns for the report
    columns = [
        _("Item Name") + ":Data:200",
        _("Item Code") + ":Data:100",
        _("Valuation Rate") + ":Currency:120",
        _("Last Purchase Rate") + ":Currency:120",
        _("Purchase Order") + ":Link/Purchase Order:150",
        _("Purchase Receipt") + ":Link/Purchase Receipt:150",
        _("Purchase Invoice") + ":Link/Purchase Invoice:150",
        _("Balance Quantity") + ":Float:120",
        _("In-Quantity") + ":Float:120",
        _("Out-Quantity") + ":Float:120"
    ]
    
    # Fetch the data
    data = get_data()
    return columns, data

def get_data():
    # Query to fetch stock ledger entries and join with Item table for item_name
    query = """
        SELECT
            i.item_name,
            sle.item_code,
            sle.valuation_rate,
            sle.last_purchase_rate,
            sle.purchase_order,
            sle.purchase_receipt,
            sle.purchase_invoice,
            sle.balance_qty,
            sle.in_qty,
            sle.out_qty
        FROM
            `tabStock Ledger Entry` sle
        LEFT JOIN
            `tabItem` i ON sle.item_code = i.item_code
        ORDER BY
            sle.posting_date
    """
    
    result = frappe.db.sql(query, as_dict=True)
    return result
