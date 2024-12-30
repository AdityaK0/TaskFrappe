import frappe
from frappe import _
import random
from datetime import datetime, timedelta

def create_test_item():
    """Create a test item if it doesn't exist"""
    if not frappe.db.exists("Item", "TEST-ITEM-001"):
        item = frappe.get_doc({
            "doctype": "Item",
            "item_code": "TEST-ITEM-001",
            "item_name": "Test Item",
            "item_group": "All Item Groups",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "is_purchase_item": 1,
            "standard_rate": 1000,
            "opening_stock": 100
        })
        try:
            item.insert()
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"Error creating test item: {str(e)}")

def get_default_warehouse():
    """Get the default warehouse from the first company"""
    default_company = frappe.defaults.get_defaults().get('company')
    warehouse = frappe.db.get_value('Warehouse', {'company': default_company, 'is_group': 0}, 'name')
    return warehouse

def create_test_data():
    try:
        create_test_item()
        
        default_warehouse = get_default_warehouse()
        if not default_warehouse:
            frappe.throw("No warehouse found. Please set up a warehouse first.")

        suppliers = [
            "TechCorp Solutions",
            "Global Industries",
            "Prime Vendors",
            "Superior Supplies"
        ]
        
        created_suppliers = []
        for supplier_name in suppliers:
            if not frappe.db.exists("Supplier", supplier_name):
                supplier = frappe.get_doc({
                    "doctype": "Supplier",
                    "supplier_name": supplier_name,
                    "supplier_group": "All Supplier Groups",
                    "supplier_type": "Company"
                })
                supplier.insert()
                created_suppliers.append(supplier_name)
                frappe.db.commit()
        
        for supplier in created_suppliers:
            num_pos = random.randint(5, 10)
            for i in range(num_pos):
                try:
                    po = create_purchase_order(supplier, default_warehouse)
                    frappe.db.commit()
                    
                    if random.random() > 0.2:  
                        pr = create_purchase_receipt(po, default_warehouse)
                        frappe.db.commit()
                        
                        if random.random() > 0.3:  
                            pi = create_purchase_invoice(pr)
                            frappe.db.commit()
                except Exception as e:
                    frappe.log_error(f"Error creating documents for supplier {supplier}: {str(e)}")
                    continue

    except Exception as e:
        frappe.log_error(f"Error in create_test_data: {str(e)}")
        raise

def create_purchase_order(supplier, warehouse):
    po = frappe.get_doc({
        "doctype": "Purchase Order",
        "supplier": supplier,
        "transaction_date": datetime.now() - timedelta(days=random.randint(0, 30)),
        "schedule_date": datetime.now() + timedelta(days=random.randint(1, 10)),
        "items": [{
            "item_code": "TEST-ITEM-001",
            "qty": random.randint(1, 100),
            "rate": random.randint(100, 1000),
            "warehouse": warehouse,
            "schedule_date": datetime.now() + timedelta(days=random.randint(1, 10))
        }]
    })
    po.insert()
    po.submit()
    return po

def create_purchase_receipt(po, warehouse):
    pr = frappe.get_doc({
        "doctype": "Purchase Receipt",
        "supplier": po.supplier,
        "posting_date": datetime.now(),
        "items": [{
            "item_code": po.items[0].item_code,
            "qty": po.items[0].qty,
            "rate": po.items[0].rate,
            "warehouse": warehouse,
            "purchase_order": po.name,
            "purchase_order_item": po.items[0].name,
            "stock_uom": "Nos"
        }]
    })
    pr.insert()
    pr.submit()
    return pr

def create_purchase_invoice(pr):
    pi = frappe.get_doc({
        "doctype": "Purchase Invoice",
        "supplier": pr.supplier,
        "posting_date": datetime.now(),
        "bill_no": f"BILL-{random.randint(1000, 9999)}",  
        "items": [{
            "item_code": pr.items[0].item_code,
            "qty": pr.items[0].qty,
            "rate": pr.items[0].rate,
            "purchase_receipt": pr.name,
            "purchase_receipt_item": pr.items[0].name,
            "stock_qty": pr.items[0].qty,
            "warehouse": pr.items[0].warehouse
        }]
    })
    pi.insert()
    pi.submit()
    return pi

def cleanup_test_data():
    """Optional: Function to cleanup test data if needed"""
    try:
        pos = frappe.get_all("Purchase Order", filters={"docstatus": 1})
        prs = frappe.get_all("Purchase Receipt", filters={"docstatus": 1})
        pis = frappe.get_all("Purchase Invoice", filters={"docstatus": 1})
        
        for pi in pis:
            doc = frappe.get_doc("Purchase Invoice", pi.name)
            if doc.docstatus == 1:
                doc.cancel()
            doc.delete()
            
        for pr in prs:
            doc = frappe.get_doc("Purchase Receipt", pr.name)
            if doc.docstatus == 1:
                doc.cancel()
            doc.delete()
            
        for po in pos:
            doc = frappe.get_doc("Purchase Order", po.name)
            if doc.docstatus == 1:
                doc.cancel()
            doc.delete()
            
        suppliers = ["TechCorp Solutions", "Global Industries", "Prime Vendors", "Superior Supplies"]
        for supplier in suppliers:
            if frappe.db.exists("Supplier", supplier):
                frappe.delete_doc("Supplier", supplier)
                
        if frappe.db.exists("Item", "TEST-ITEM-001"):
            frappe.delete_doc("Item", "TEST-ITEM-001")
            
        frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(f"Error in cleanup_test_data: {str(e)}")
        raise