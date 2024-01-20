import frappe
# frappe.init(site="husna.erpgulf.com")
# frappe.connect()
import sys
from frappe import _
import frappe
import sys
from frappe import _
# from frappe.model.mapper import get_mapped_doc
# from erpnext.controllers.sales_and_purchase_return import make_return_doc


@frappe.whitelist(allow_guest=True)
def validate_returned_quantity(doc_name):
    try:
        doc = frappe.get_doc('Delivery Note', doc_name)
        for item in doc.items: 
            validate_item_quantity(item, doc)
    except Exception as e:
        frappe.msgprint(str(e))

def validate_item_quantity(item, delivery_note_doc):
    original_qty = abs(item.get('qty', 0))
    returned_qty = abs(item.get('returned_qty', 0))
    sales_invoice_return_qty = 0
    
    sales_invoice_name = frappe.get_value('Sales Invoice Item', {'delivery_note': delivery_note_doc.name}, 'parent')

    qty_in_invoice = 0 # Initialize qty_in_invoice here

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
    
    if difference == 0:
        delivery_note_doc.db_set('status', 'Closed', commit=True, update_modified=True)
        frappe.throw(_("Sales Return cannot be created for already completed delivery note {0} .").format(delivery_note_doc.name))
        return
    else:
     
        pass
