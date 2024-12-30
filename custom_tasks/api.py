import frappe
import json

def get_supplier_purchase_data():
    data = {}
    suppliers = frappe.get_all("Supplier", fields=["name"])

    for supplier in suppliers:
        pos = frappe.db.count("Purchase Order", filters={"supplier": supplier.name, "docstatus": 1})
        prs = frappe.db.count("Purchase Receipt", filters={"supplier": supplier.name, "docstatus": 1})
        pis = frappe.db.count("Purchase Invoice", filters={"supplier": supplier.name, "docstatus": 1})

        data[supplier.name] = {
            "Purchase Orders": pos,
            "Purchase Receipts": prs,
            "Purchase Invoices": pis,
        }
    return data

def prepare_chart_data():
    """Prepare the data for the chart."""
    chart_data = {
        "labels": ["Supplier 1", "Supplier 2", "Supplier 3"],
        "datasets": [
            {
                "name": "Purchase Orders",
                "values": [5, 10, 15]
            },
            {
                "name": "Purchase Receipts",
                "values": [4, 9, 14]
            },
            {
                "name": "Purchase Invoices",
                "values": [3, 8, 13]
            }
        ]
    }
    return chart_data


def create_external_chart():
    """Create and save the chart in Frappe using external API."""
    chart_name = "Supplier Purchase Funnel"
    
    # Check if the chart already exists
    if frappe.db.exists("Dashboard Chart", chart_name):
        return "Chart already exists."

    chart_data = {
        "labels": ["Supplier 1", "Supplier 2", "Supplier 3"],
        "datasets": [
            {
                "name": "Purchase Orders",
                "values": [5, 10, 15]
            },
            {
                "name": "Purchase Receipts",
                "values": [4, 9, 14]
            },
            {
                "name": "Purchase Invoices",
                "values": [3, 8, 13]
            }
        ]
    }

    # Create the chart if it doesn't exist
    chart = frappe.get_doc({
        "doctype": "Dashboard Chart",
        "chart_name": chart_name,
        "chart_type": "Custom",
        "data": json.dumps(chart_data),  # Store the prepared chart data
        "filters_json": json.dumps({"supplier": "TechCorp Solutions"}),  # Example filter
        "type": "bar",  # Chart type (bar chart)
        "is_public": 1  # Make the chart public
    })
    chart.insert()
    return "Chart created successfully."




@frappe.whitelist()
def setup_purchase_funnel():
    """Setup the supplier purchase funnel."""
    try:
        create_external_chart()
        frappe.db.commit()
        return "Purchase Funnel setup complete!"
    except Exception as e:
        frappe.log_error(f"Error in setting up purchase funnel: {str(e)}")
        return f"Error: {str(e)}"
