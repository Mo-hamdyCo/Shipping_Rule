# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DomisticRule(Document):
    pass

@frappe.whitelist()
def get_shipping_price(item_code, from_zone, to_zone, type_of_shipment, price_list, posting_date):
    # Step 1: جيب كل Domistic Rules اللي فيها الصنف المطلوب
    domistic_rules = frappe.get_all(
        "Domistic Rule",
        filters={"item": item_code},
        fields=["name", "shippment_price_list"]
    )

    if not domistic_rules:
        frappe.throw(f"❌ مفيش Domistic Rule مرتبط بالصنف: {item_code}")

    # Step 2: فلترة بناء على الشروط + الشيبمنت برايس ليست
    for rule in domistic_rules:
        if rule.shippment_price_list != price_list:
            continue  # Ignore rules with different price list

        result = frappe.get_all(
            "ship price",
            filters={
                "parent": rule.name,
                "from_zone": from_zone,
                "to_zone": to_zone,
                "type_of_ship": type_of_shipment
            },
            fields=["ship_rate"]
        )

        if result:
            return {
                "rate": result[0].ship_rate,
                "rule_name": rule.name,
                "price_list": rule.shippment_price_list
            }

    # Step 3: fallback error
    frappe.throw(
        f"❌ مفيش سعر شحن متاح للصنف {item_code} من {from_zone} إلى {to_zone} عن طريق {type_of_shipment} باستخدام Price List: {price_list}"
    )

