from odoo import http
from odoo.http import request

class QRScannerController(http.Controller):
    @http.route('/qr/validate/', auth='public', website=True)
    def scan_page_validate(self, **kw):
        return request.render(
            'prescription_scanner.qr_scan_page_validate'
        )
        
    @http.route('/qr/dispense/', auth='public', website=True)
    def scan_page_dispense(self, **kw):
        return request.render(
            'prescription_scanner.qr_scan_page_sales_order'
        )
    
    @http.route("/qr/lookup", type="json", auth="public", csrf=False)
    def qr_lookup(self, token):
        prescription = request.env["prescription.customer.prescription"].sudo().search(
            [("qr_token","=",token)], limit=1)
        if not prescription:
            return {"error":"Not found"}
        return {"redirect_url": f"/prescription/{prescription.id}"}
    
    @http.route("/prescription/<int:prescription_id>", auth='public', website=True)
    def prescription_detail(self, prescription_id, **kw):
        def clean(value):
            """Convert False/None/'False' into empty string."""
            if value in (False, None, "False"):
                return ""
            return value
            
        prescription = request.env["prescription.customer.prescription"].sudo().browse(prescription_id)
        if not prescription.exists():
            return request.not_found()
        
        prescription_data = {
            "id": prescription.id,
            "name": clean(prescription.name),
            "customer": {
                "name": clean(prescription.customer.name),
            },
            "date": clean(prescription.date),
            "valid_until": clean(prescription.valid_until),
            "line_ids": [
                {
                    "id": l.id,
                    "product": {
                        "name": clean(l.product.name),
                    },
                    "quantity": l.quantity or 0,
                    "remarks": clean(l.remarks),
                }
                for l in prescription.line_ids
            ],
        }
        
        return request.render(
            'prescription_scanner.qr_scan_page_prescription',
            {"prescription": prescription_data}
        )
        
    @http.route("/qr/create_sales_order", type="json", auth="public", csrf=False)
    def qr_create_so(self, token):
        prescription = request.env["prescription.customer.prescription"].sudo().search(
            [("qr_token","=",token), ("status","=","confirm")], limit=1)
        if not prescription:
            return {"error":"Prescription not found"}

        sale_order = request.env["sale.order"].sudo().create({
            "partner_id": prescription.customer.id,
            "order_line": [
                (0,0,{"product_id": line.product.product_variant_id.id,"product_uom_qty":line.quantity})
                for line in prescription.line_ids
            ],
        })
        return {"redirect_url": f"/sale_order/{sale_order.id}"}
    
    @http.route("/sale_order/<int:sale_order_id>", auth='public', website=True)
    def sale_order_detail(self, sale_order_id, **kw):
        sale_order = request.env["sale.order"].sudo().browse(sale_order_id)
        if not sale_order.exists():
            return request.not_found()
        
        sale_order_reference = sale_order.name or f"SO{sale_order.id:05d}"
        return request.render(
            'prescription_scanner.qr_scan_page_dispense',
            {"reference": sale_order_reference}
        )
        