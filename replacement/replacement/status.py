import frappe
# frappe.init(site="husna.erpgulf.com")
# frappe.connect()
import sys
from frappe import _

def validate_status_quantity(doc, method):
    try:
        for item in doc.items:
            validate_status(item, doc)
    except Exception as e:
        frappe.msgprint(str(e))


def validate_status(item, delivery_note_doc):
    original_qty = abs(item.get('qty', 0))
    returned_qty = abs(item.get('returned_qty', 0))

    # frappe.msgprint(f"Original Qty: {original_qty}, Returned Qty: {returned_qty}")

    sales_invoice_name = frappe.get_value('Sales Invoice Item', {'delivery_note': delivery_note_doc.name}, 'parent')

    if sales_invoice_name:
        sales_invoice_doc = frappe.get_doc('Sales Invoice', sales_invoice_name)
        original_sales_invoice_note = sales_invoice_doc.get('return_against')

        if original_sales_invoice_note:
            original_sales_invoice_doc = frappe.get_doc('Sales Invoice', original_sales_invoice_note)
            # frappe.msgprint(f"Original sales invoice doc is: {original_sales_invoice_doc}")
            for invoice_item in original_sales_invoice_doc.items:
                qty_in_invoice = invoice_item.qty
                # print(f"Quantity in Sales Invoice for item {invoice_item.item_code}: {qty_in_invoice}")
        else:
            frappe.msgprint("No linked Delivery Note found in Sales Invoice.")
    else:
        frappe.msgprint("No linked Sales Invoice found for the given Delivery Note.")

    difference = (original_qty - returned_qty) - qty_in_invoice
    item.difference = difference

    if difference == 0:
        delivery_note_doc.db_set('status', 'Closed', commit=True, update_modified=True)