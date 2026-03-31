/** @odoo-module **/

import { Component, onMounted, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class DispenseThankYou extends Component {
    setup() {
        onMounted(() => {
            this.startRedirectCountdown();
        });

        onWillUnmount(() => {
            if (this.redirectTimer) {
                clearTimeout(this.redirectTimer);
            }
        });
    }

    startRedirectCountdown() {
        this.redirectTimer = setTimeout(() => {
            window.location.href = "/qr/dispense";
        }, 10000); // 10 seconds
    }
}

DispenseThankYou.template = "prescription_scanner.DispenseThankYou";

registry.category("public_components").add(
    "prescription_scanner.DispenseThankYou",
    DispenseThankYou
);