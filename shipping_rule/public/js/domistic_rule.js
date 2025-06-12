// Copyright (c) 2025, Hamdy and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Domistic Rule", {
// 	refresh(frm) {

// 	},
// });

console.log("📦 Custom Sales Invoice JS from shipping_rule loaded");

frappe.ui.form.on("Sales Invoice", {
    refresh(frm) {
        if (frm.doc.custom_use_shipping_price_rule) {
            update_all_items(frm);
        }
    },

    custom_from_zone: update_all_items,
    custom_to_zone: update_all_items,
    custom_type_of_shipment: update_all_items,
    custom_use_shipping_price_rule: update_all_items
});

frappe.ui.form.on("Sales Invoice Item", {
    item_code(frm, cdt, cdn) {
        update_item_rate(frm, cdt, cdn, true);  // delay = true لتفادي تضارب مع كتابة Frappe التلقائية
    }
});

function update_all_items(frm) {
    (frm.doc.items || []).forEach(item => {
        update_item_rate(frm, item.doctype, item.name);
    });
}

function update_item_rate(frm, cdt, cdn, delay = false) {
    const row = locals[cdt][cdn];

    if (!frm.doc.custom_use_shipping_price_rule) return;

    if (!(frm.doc.custom_from_zone && frm.doc.custom_to_zone && frm.doc.custom_type_of_shipment && row.item_code)) {
        return;
    }

    const do_call = () => {
        frappe.call({
            method: "shipping_rule.shipping_rule.doctype.domistic_rule.domistic_rule.get_shipping_price",
            args: {
                item_code: row.item_code,
                from_zone: frm.doc.custom_from_zone,
                to_zone: frm.doc.custom_to_zone,
                type_of_shipment: frm.doc.custom_type_of_shipment,
                price_list: frm.doc.selling_price_list,
                posting_date: frm.doc.posting_date
            },
            callback(r) {
                console.log(" Response from domistic rule:", r.message);
                if (r.message) {
                    frappe.model.set_value(cdt, cdn, "rate", r.message.rate);
                }
            }
        });
    };

    if (delay) {
        setTimeout(do_call, 300);
    } else {
        do_call();
    }
}
