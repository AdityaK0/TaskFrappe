# Copyright (c) 2024, aditya and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry
from erpnext.accounts.general_ledger import make_gl_entries

class GatePass(Document):
    def validate(self):
        self.validate_quantities()
    
    def validate_quantities(self):
        for item in self.items:
            if not item.quantity or item.quantity <= 0:
                frappe.throw(_("Quantity must be greater than 0 for item {0}").format(item.item_code))
            
            # Check if sufficient stock exists
            actual_qty = frappe.db.get_value("Bin", 
                {"item_code": item.item_code, "warehouse": self.warehouse},
                "actual_qty") or 0
            
            if actual_qty < item.quantity:
                frappe.throw(_("Insufficient stock for item {0} in warehouse {1}").format(
                    item.item_code, self.warehouse))
    
    def on_submit(self):
        self.update_stock_ledger()
        self.make_gl_entries()
    
    def update_stock_ledger(self):
        # Create stock entry for item deduction
        stock_entry = frappe.new_doc("Stock Entry")
        stock_entry.stock_entry_type = "Material Issue"
        stock_entry.purpose = "Material Issue"
        stock_entry.from_warehouse = self.warehouse
        stock_entry.reference_doctype = "Gate Pass"
        stock_entry.reference_name = self.name
        
        for item in self.items:
            stock_entry.append("items", {
                "item_code": item.item_code,
                "qty": item.quantity,
                "basic_rate": item.rate,
                "s_warehouse": self.warehouse,
                "conversion_factor": 1.0,
                "transfer_qty": item.quantity
            })
        
        stock_entry.insert()
        stock_entry.submit()
    
    def make_gl_entries(self):
        # Create GL entries for accounting impact
        gl_entries = []
        
        # Debit Expense Account
        gl_entries.append({
            "account": "Cost of Goods Sold - TC",
            "debit": self.total_amount,
            "credit": 0,
            "against": "Stock In Hand - TC",
            "remarks": f"Gate Pass: {self.name}",
            "posting_date": self.posting_date,
            "voucher_type": "Gate Pass",
            "voucher_no": self.name
        })
        
        # Credit Stock Account
        gl_entries.append({
            "account": "Stock In Hand - TC",
            "debit": 0,
            "credit": self.total_amount,
            "against": "Cost of Goods Sold - TC",
            "remarks": f"Gate Pass: {self.name}",
            "posting_date": self.posting_date,
            "voucher_type": "Gate Pass",
            "voucher_no": self.name
        })
        
        make_gl_entries(gl_entries)

def create_custom_doctype():
    """Function to create the Gate Pass DocType"""
    # Create Child DocType first
    if not frappe.db.exists("DocType", "Gate Pass Item"):
        child_doctype = frappe.new_doc("DocType")
        child_doctype.name = "Gate Pass Item"
        child_doctype.module = "Stock"
        child_doctype.istable = 1
        child_doctype.fields = [
            {
                "fieldname": "item_code",
                "fieldtype": "Link",
                "label": "Item Code",
                "options": "Item",
                "reqd": 1
            },
            {
                "fieldname": "quantity",
                "fieldtype": "Float",
                "label": "Quantity",
                "reqd": 1
            },
            {
                "fieldname": "rate",
                "fieldtype": "Currency",
                "label": "Rate",
                "reqd": 1
            },
            {
                "fieldname": "amount",
                "fieldtype": "Currency",
                "label": "Amount",
                "read_only": 1
            }
        ]
        child_doctype.insert()

    # Create Parent DocType
    if not frappe.db.exists("DocType", "Gate Pass"):
        doctype = frappe.new_doc("DocType")
        doctype.name = "Gate Pass"
        doctype.module = "Stock"
        doctype.custom = 1
        doctype.fields = [
            {
                "fieldname": "warehouse",
                "fieldtype": "Link",
                "label": "Warehouse",
                "options": "Warehouse",
                "reqd": 1
            },
            {
                "fieldname": "posting_date",
                "fieldtype": "Date",
                "label": "Posting Date",
                "reqd": 1,
                "default": "Today"
            },
            {
                "fieldname": "items",
                "fieldtype": "Table",
                "label": "Items",
                "options": "Gate Pass Item",
                "reqd": 1
            },
            {
                "fieldname": "total_amount",
                "fieldtype": "Currency",
                "label": "Total Amount",
                "read_only": 1
            }
        ]
        doctype.permissions = [
            {
                "role": "Stock Manager",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1,
                "submit": 1,
                "cancel": 1
            }
        ]
        doctype.insert()

def create_gate_pass_workspace():
    """Function to create Gate Pass workspace"""
    if not frappe.db.exists("Workspace", "Gate Pass Management"):
        workspace = frappe.new_doc("Workspace")
        workspace.name = "Gate Pass Management"
        workspace.module = "Stock"
        workspace.label = "Gate Pass Management"
        workspace.category = "Modules"
        workspace.is_standard = 0
        
        # Add links
        workspace.append("links", {
            "label": "Gate Pass",
            "type": "DocType",
            "link": "Gate Pass",
            "onboard": 1
        })
        
        workspace.insert()
