/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class PrescriptionInterface extends Component {
    setup() {
        this.prescription = this.props.data;
    }

    goToValidate(ev) {
        if (ev) {
            ev.preventDefault();
        }
        window.location.href = "/qr/validate";
    }
}

PrescriptionInterface.template = "prescription_scanner.PrescriptionInterface";

registry.category("public_components").add(
    "prescription_scanner.PrescriptionInterface",
    PrescriptionInterface
);