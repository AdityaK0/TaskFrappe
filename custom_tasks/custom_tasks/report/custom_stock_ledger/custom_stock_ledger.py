# Copyright (c) 2024, aditya and contributors
# For license information, please see license.txt

import frappe

from frappe import _
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Link",
            "options": "Item",
            "width": 150
        },
        {
            "label": _("Item Code"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 120
        },
        {
            "label": _("Valuation Rate"),
            "fieldname": "valuation_rate",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Last Purchase Rate"),
            "fieldname": "last_purchase_rate",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Purchase Order"),
            "fieldname": "purchase_order",
            "fieldtype": "Link",
            "options": "Purchase Order",
            "width": 130
        },
        {
            "label": _("Purchase Receipt"),
            "fieldname": "purchase_receipt",
            "fieldtype": "Link",
            "options": "Purchase Receipt",
            "width": 130
        },
        {
            "label": _("Purchase Invoice"),
            "fieldname": "purchase_invoice",
            "fieldtype": "Link",
            "options": "Purchase Invoice",
            "width": 130
        },
        {
            "label": _("Balance Qty"),
            "fieldname": "balance_qty",
            "fieldtype": "Float",
            "width": 100
        },
        {   
            "label": _("In Qty"),
            "fieldname": "in_qty",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("Out Qty"),
            "fieldname": "out_qty",
            "fieldtype": "Float",
            "width": 100
        }
    ]

def get_data(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND sle.posting_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND sle.posting_date <= %(to_date)s"
    if filters.get("item_code"):
        conditions += " AND sle.item_code = %(item_code)s"
    if filters.get("warehouse"):
        conditions += " AND sle.warehouse = %(warehouse)s"

    query = """
        SELECT 
            sle.item_code,
            item.item_name,
            sle.valuation_rate,
            item.last_purchase_rate,
            CASE 
                WHEN sle.voucher_type = 'Purchase Receipt' 
                THEN (SELECT pri.purchase_order 
                     FROM `tabPurchase Receipt Item` pri 
                     WHERE pri.parent = sle.voucher_no 
                     AND pri.item_code = sle.item_code 
                     LIMIT 1)
                ELSE NULL 
            END as purchase_order,
            CASE 
                WHEN sle.voucher_type = 'Purchase Receipt' 
                THEN sle.voucher_no 
                ELSE NULL 
            END as purchase_receipt,
            CASE 
                WHEN sle.voucher_type = 'Purchase Invoice' 
                THEN sle.voucher_no 
                ELSE NULL 
            END as purchase_invoice,
            sle.qty_after_transaction as balance_qty,
            CASE WHEN sle.actual_qty > 0 THEN sle.actual_qty ELSE 0 END as in_qty,
            CASE WHEN sle.actual_qty < 0 THEN ABS(sle.actual_qty) ELSE 0 END as out_qty
        FROM 
            `tabStock Ledger Entry` sle
        JOIN 
            `tabItem` item ON sle.item_code = item.name
        WHERE 
            sle.docstatus = 1 
            {conditions}
        ORDER BY 
            sle.posting_date, sle.posting_time
    """.format(conditions=conditions)

    return frappe.db.sql(query, filters, as_dict=1)




import frappe
from frappe.utils import cstr
import io
import base64
import xlsxwriter
from frappe.utils.xlsxutils import build_xlsx_response

@frappe.whitelist()
def downloadExcel(filters):
    try:
        if isinstance(filters, str):
            filters = frappe.parse_json(filters)
            
        data = get_data(filters)  
        
        if not data:
            return 0
            
        output = io.BytesIO()
        
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Stock Ledger')
        
        header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'bg_color': '#F0F0F0',
            'border': 1
        })
        
        cell_format = workbook.add_format({
            'align': 'left',
            'border': 1
        })
        
        number_format = workbook.add_format({
            'align': 'right',
            'border': 1,
            'num_format': '#,##0.00'
        })
        
        headers = [
            'Item Name',
            'Item Code',
            'Valuation Rate',
            'Last Purchase Rate',
            'Purchase Order',
            'Purchase Receipt',
            'Purchase Invoice',
            'Balance Quantity',
            'In-Quantity',
            'Out-Quantity'
        ]
        
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
            worksheet.set_column(col, col, 15)
        
        for row, item in enumerate(data, start=1):
            worksheet.write(row, 0, item.get('item_name'), cell_format)
            worksheet.write(row, 1, item.get('item_code'), cell_format)
            worksheet.write(row, 2, item.get('valuation_rate'), number_format)
            worksheet.write(row, 3, item.get('last_purchase_rate'), number_format)
            worksheet.write(row, 4, item.get('purchase_order'), cell_format)
            worksheet.write(row, 5, item.get('purchase_receipt'), cell_format)
            worksheet.write(row, 6, item.get('purchase_invoice'), cell_format)
            worksheet.write(row, 7, item.get('balance_qty'), number_format)
            worksheet.write(row, 8, item.get('in_qty'), number_format)
            worksheet.write(row, 9, item.get('out_qty'), number_format)
        
        workbook.close()
        
        output.seek(0)
        
        xlsx_data = output.getvalue()
        file_base64 = base64.b64encode(xlsx_data).decode()
        
        return {
            'file_base64': file_base64,
            'filename': 'Stock_Ledger_Report.xlsx'
        }
        
    except Exception as e:
        frappe.log_error(f"Excel Download Error: {str(e)}")
        return 0