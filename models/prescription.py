from odoo import models, fields, api, _
import uuid

class CustomerPrescription(models.Model):
    _name = "prescription.customer.prescription"
    _description = "Customer Prescriptions"
    
    name = fields.Char(
        string="Reference Number",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    date = fields.Date(
        string="Date Prescribed"
    )
    customer = fields.Many2one(
        string="Customer",
        comodel_name="res.partner",
        ondelete="cascade",
    )
    valid_until=fields.Date(
        string="Valid Until"
    )
    qr_token=fields.Char(
        string="QR Token",
        index=True,
        readonly=True,
        copy=False
    )
    status=fields.Selection(
        string="Status",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Confirmed"),
            ("cancel", "Cancelled")
        ],
        default="draft"
    )
    confirmed_by = fields.Many2one(
        string="Confirmed By",
        comodel_name="res.users",
        ondelete="cascade",
    )
    active = fields.Boolean(
        string="Active",
        default=True
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        ondelete="cascade",
        default=lambda self: self.env.company.id
    )
    line_ids = fields.One2many(
        string="Prescription Line IDs",
        inverse_name="prescription_id",
        comodel_name="prescription.customer.prescription.lines"
    )
    
    _sql_constraints = [
        ('qr_token_unique', 'unique(qr_token)', 'QR Token must be unique!'),
    ]
    
    # GENERATE REFERENCE NUMBER
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'prescription.customer.prescription'
                ) or _('New')
        return super().create(vals_list)
    
    # GENERATE QR TOKEN CODE
    def _generate_qr_token(self):
        return f"RX-{uuid.uuid4().hex}"
    
    def generate_qr_token_on_confirm(self):
        for record in self:
            if record.status == 'draft' and not record.qr_token:
                record.qr_token = self._generate_qr_token()
                record.status = 'confirm'
                record.confirmed_by = self.env.user.id
    
    def reset_to_draft(self):
        for record in self:
            record.status = 'draft'
            record.qr_token = False
            record.confirmed_by = False
            
    # @api.model
    # def create(self, vals):
    #     if not vals.get("qr_token"):
    #         vals["qr_token"] = self._generate_qr_token()
    #     return super().create(vals)


class CustomerPrescriptionLine(models.Model):
    _name="prescription.customer.prescription.lines"
    _description = "Customer Prescription Lines"
    
    prescription_id = fields.Many2one(
        string="Prescription",
        comodel_name="prescription.customer.prescription",
        ondelete="cascade",
    )
    product = fields.Many2one(
        string="Product",
        domain="[('sale_ok', '=', True)]",
        comodel_name="product.template",
        ondelete="cascade",
    )
    quantity = fields.Integer(
        string="Quantity"
    )
    remarks = fields.Char(
        string="Doctor's Remarks"
    )
    