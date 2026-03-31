import { Component, onMounted } from "@odoo/owl";
import { QRScanner } from "./qr_scanner";
import { jsonrpc } from "@web/core/network/rpc_service";

export class PrescriptionScanPage extends Component {
    setup() {
        onMounted(() => {
            this.scanner = new QRScanner();
            this.scanner.on("qr-scanned", async ({ value }) => {
                await this.handleScannedValue(value);
            });
        });
    }

    async handleScannedValue(qrToken) {
        if (this.mode === "lookup") {
            const result = await jsonrpc("/qr/lookup", { token: qrToken });
            if (result.error) {
                alert(result.error);
            } else {
                window.location.href = result.redirect_url;
            }
        } else if (this.mode === "sales_order") {
            const result = await jsonrpc("/qr/create_sales_order", { token: qrToken });
            if (result.error) {
                alert(result.error);
            } else {
                window.location.href = result.redirect_url;
            }
        }
    }
}

