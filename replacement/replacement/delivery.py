import frappe
# frappe.init(site="husna.erpgulf.com")
# frappe.connect()
import sys
from frappe import _
import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def validate_returned_quantity(doc_name):
    try:
        doc = frappe.get_doc('Delivery Note', doc_name)
        differences = {}

        # Validate quantity for each item
        for item in doc.items:
            difference = validate_item_quantity(item, doc)
            differences[item.name] = difference
        has_zero_difference = any(difference == 0 for difference in differences.values())

        if has_zero_difference:
            # Set the document status to 'Closed'
            frappe.db.set_value('Delivery Note', doc_name, 'status', 'Closed')
        return differences
    except frappe.DoesNotExistError:
        frappe.msgprint(_("Delivery Note not found: {0}").format(doc_name))
    except Exception as e:
        frappe.msgprint(str(e))

def validate_item_quantity(item, delivery_note_doc):
    original_qty = abs(item.get('qty', 0))
    returned_qty = abs(item.get('returned_qty', 0))
    sales_invoice_return_qty = 0
    
    sales_invoice_name = frappe.get_value('Sales Invoice Item', {'delivery_note': delivery_note_doc.name}, 'parent')

    qty_in_invoice = 0

    if sales_invoice_name:
        sales_invoice_doc = frappe.get_doc('Sales Invoice', sales_invoice_name)
        for item in sales_invoice_doc.items:
            sales_invoice_return_qty = abs(item.get('qty', 0))

        original_sales_invoice_note = sales_invoice_doc.get('return_against')
        if original_sales_invoice_note:
            original_sales_invoice_doc = frappe.get_doc('Sales Invoice', original_sales_invoice_note)
            for invoice_item in original_sales_invoice_doc.items:
                qty_in_invoice = invoice_item.qty
        else:
            print("No linked Sales Invoice found for the given Delivery Note.")
            pass 
    else:
        pass

    difference = (original_qty - returned_qty) - qty_in_invoice

    item.difference = difference
    return difference
   
    