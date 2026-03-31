# from odoo import models, fields, api


# class prescription_scanner(models.Model):
#     _name = 'prescription_scanner.prescription_scanner'
#     _description = 'prescription_scanner.prescription_scanner'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

