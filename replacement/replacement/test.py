import frappe
# frappe.init(site="husna.erpgulf.com")
# frappe.connect()

@frappe.whitelist(allow_guest=True)
def create_reverse_replacement_doc(item, replacement_item):
    try:

        replacement = frappe.get_doc("Replacement", {"item": item, "replacement_item": replacement_item})
        new_replacement = frappe.new_doc("Replacement")
        new_replacement.item = replacement_item
        new_replacement.replacement_item = item
        new_replacement.insert(ignore_permissions=True) 

    except Exception as e:
        frappe.msgprint(f"An error occurred: {e}")


