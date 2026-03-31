/** @odoo-module **/

import { Component, onMounted, onWillUnmount } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";

export class QRScanner extends Component {

    setup() {
        this.qr = null;

        onMounted(() => {
            this.startScanner();
        });

        onWillUnmount(() => {
            if (this.qr) {
                this.qr.stop().catch(() => {});
            }
        });
    }

    startScanner() {
        const self = this;

        this.qr = new Html5Qrcode("qr-reader");

        this.qr.start(
            { facingMode: "environment" },
            {fps: 10,qrbox: 250,},
            (decodedText) => {
                self.onScan(decodedText);
            }
        );
    }

    onScan(value) {
        // alert("QR Scanned: " + value);
        this.qr.stop();
        this.handleScannedValue(value);
    }

    async handleScannedValue(qrToken) {
        if (this.props.mode === "lookup") {
            alert("Looking up prescription for token: " + qrToken);
            const result = await rpc("/qr/lookup", { token: qrToken });
            if (result.error) {
                alert(result.error);
            } else {
                window.location.href = result.redirect_url;
            }
        } else if (this.props.mode === "sales_order") {
            alert("Creating sales order for token: " + qrToken);
            const result = await rpc("/qr/create_sales_order", { token: qrToken });
            if (result.error) {
                alert(result.error);
            } else {
                window.location.href = result.redirect_url;
            }
        } else {
            alert("Scanned QR Token: " + qrToken);
        }
    }
};

QRScanner.props = {mode: {type: String, default: "lookup"}};
QRScanner.template = "prescription_scanner.QRScanner";

registry.category("public_components").add(
    "prescription_scanner.QRScanner",
    QRScanner
);