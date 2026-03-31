# AI Generated tests for prescription_scanner module. 
# These tests cover the QR code scanning flow, sales order creation, 
# and page rendering for prescriptions and sales orders. 
# The tests use Odoo's HttpCase for integration testing of public routes and 
# JSON endpoints.

# File: prescription_scanner/tests/test_qr_controller.py
from odoo.tests.common import HttpCase
import json
import logging

_logger = logging.getLogger(__name__)

class TestQRScannerController(HttpCase):
    """Integration tests for QR scanner public routes"""

    def setUp(self):
        super().setUp()
        # Create a test partner
        self.partner = self.env['res.partner'].sudo().create({
            'name': 'Test Customer',
        })
        # Create a test prescription
        self.prescription = self.env['prescription.customer.prescription'].sudo().create({
            'customer': self.partner.id,
            'status': 'confirm',  # Ready for sales order test
        })
        # Generate QR token
        self.prescription.generate_qr_token_on_confirm()
        _logger.info(f"Test prescription QR token: {self.prescription.qr_token}")

    def test_scan_page_validate_render(self):
        """Test the /qr/validate page renders successfully"""
        response = self.url_open("/qr/validate/")
        self.assertIn(b"qr-fullscreen", response.read())

    def test_scan_page_dispense_render(self):
        """Test the /qr/dispense page renders successfully"""
        response = self.url_open("/qr/dispense/")
        self.assertIn(b"PrescriptionInterface", response.read())

    def test_qr_lookup_success(self):
        """Test JSON route /qr/lookup returns correct redirect"""
        response = self.url_open(
            "/qr/lookup",
            method='POST',
            data=json.dumps({'token': self.prescription.qr_token}),
            headers=[('Content-Type', 'application/json')]
        )
        result = json.loads(response.read())
        self.assertIn(f"/prescription/{self.prescription.id}", result.get("redirect_url"))

    def test_qr_lookup_fail(self):
        """Test lookup with invalid token returns error"""
        response = self.url_open(
            "/qr/lookup",
            method='POST',
            data=json.dumps({'token': 'INVALID'}),
            headers=[('Content-Type', 'application/json')]
        )
        result = json.loads(response.read())
        self.assertEqual(result.get("error"), "Not found")

    def test_qr_create_sales_order(self):
        """Test sales order creation via QR"""
        response = self.url_open(
            "/qr/create_sales_order",
            method='POST',
            data=json.dumps({'token': self.prescription.qr_token}),
            headers=[('Content-Type', 'application/json')]
        )
        result = json.loads(response.read())
        self.assertIn("/sale_order/", result.get("redirect_url"))
        sale_order_id = int(result["redirect_url"].split("/")[-1])
        sale_order = self.env['sale.order'].sudo().browse(sale_order_id)
        self.assertEqual(sale_order.partner_id.id, self.partner.id)
        _logger.info(f"Created Sale Order: {sale_order.name}")

    def test_prescription_detail_render(self):
        """Test prescription detail page renders"""
        response = self.url_open(f"/prescription/{self.prescription.id}")
        content = response.read()
        self.assertIn(self.prescription.name.encode(), content)
        self.assertIn(self.partner.name.encode(), content)

    def test_sale_order_detail_render(self):
        """Test sale order detail page render"""
        # Create sale order for testing
        sale_order = self.env['sale.order'].sudo().create({
            'partner_id': self.partner.id
        })
        response = self.url_open(f"/sale_order/{sale_order.id}")
        self.assertIn(sale_order.name.encode(), response.read())