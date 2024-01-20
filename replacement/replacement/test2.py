import frappe

# frappe.init(site="husna.erpgulf.com")
# frappe.connect()

@frappe.whitelist(allow_guest=True)
def search_items_and_replacements(item_name):
   
    replacements_for_item = frappe.get_all('Replacement', filters={'replacement_item': item_name}, fields=['item'])
    items_replaced_by_item = frappe.get_all('Replacement', filters={'item': item_name}, fields=['replacement_item'])
 

    result_items = [item['item'] for item in replacements_for_item]
    result_replacements = [item['replacement_item'] for item in items_replaced_by_item]

    return {
        'items': list(result_items),
        'replacements': list(result_replacements)
    }

