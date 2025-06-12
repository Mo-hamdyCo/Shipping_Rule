# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DomisticRule(Document):
    pass

@frappe.whitelist()
def get_shipping_price(item_code, from_zone, to_zone, type_of_shipment, price_list, posting_date):
    result = frappe.get_all(
        "ship price",
        filters={
            "from_zone": from_zone,
            "to_zone": to_zone,
            "type_of_ship": type_of_shipment
        },
        fields=["ship_rate", "parent"]
    )

    if not result:
        frappe.throw("مفيش سعر لصنف.")

    parent_name = result[0].parent

    if not frappe.db.exists("Domistic Rule", parent_name):
        frappe.throw(f"Domistic Rule {parent_name} not found.")

    domistic_rule = frappe.get_doc("Domistic Rule", parent_name)

    return {
        "rate": result[0].ship_rate,
        "rule_name": parent_name,
        "price_list": domistic_rule.shippment_price_list  # تأكد من وجود هذا الحقل
    }
