import frappe
# frappe.init(site="husna.erpgulf.com")
# frappe.connect()


def create_payment_entry():
    try:
            amount=1000
            payment_entry = frappe.get_doc({
                "doctype": "Payment Entry",
                "payment_type": "Receive",
                "company": "Husna (Demo)",
                "party_type": "Customer", 
                "party": "Grant Plastics Ltd.",  
                "party_name": "Grant Plastics Ltd.",  
                "paid_amount": amount,
                "received_amount" : amount,
                "mode_of_payment": "Cash",
                "target_exchange_rate" : 1,
                "paid_to": "1110 - Cash - MD",
                "paid_to_account_currency": "SAR",
                "reference_no" : "",
                "reference_date" : "2024-01-02"
            })
            payment_entry.insert()
            frappe.msgprint(f"Payment Entry created successfully with ID: {payment_entry.name}")

    except Exception as e:
            frappe.msgprint(f"An error occurred: {e}")
