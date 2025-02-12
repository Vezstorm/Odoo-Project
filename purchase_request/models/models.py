
from odoo import fields, models, api, _


# Child Model
class ProductOrderMaster(models.Model):
    _name="order.line"
    _description="Product Order Line"

    order_line_id = fields.Many2one('purchase.request', string="Product Table", copy=False)
    product_name = fields.Many2one('product.template', string="Product Name")
    description = fields.Char(string="Description")
    unit_of_measure = fields.Many2one('uom.uom',string="Unit of Measure")
    quantity = fields.Integer(string="Quantity")
    approved_quantity = fields.Integer(string="Approved Quantity", required=True)
    status = fields.Selection(related='order_line_id.status')

    @api.onchange('product_name')
    def onchange_uom(self):
        for record in self:
            if record.product_name:
                record.unit_of_measure = record.product_name.uom_id
            else:
                record.unit_of_measure = None

# Parent Model
class PurchaseRequestMaster(models.Model):
    _name="purchase.request"
    _description="Purchase Request"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "sequence_id"

    employee_name = fields.Many2one('hr.employee',string="Employee Name")
    designation = fields.Many2one('hr.job',string="Designation")
    date_of_request = fields.Date(string="Date of Request")
    department = fields.Many2one('hr.department', string="Department")
    reference_number = fields.Char(string="Reference Number")
    remarks = fields.Char(string="Remarks")
    table_id = fields.One2many('order.line', 'order_line_id', string="Product Table")
    # This field is for sequencing
    sequence_id = fields.Char('Sequence', copy=False, default="New")

    status = fields.Selection([('draft', 'Draft'),('request', 'Request'), ('approve', 'Approve'), ('reset', 'Reset'), ('cancel', 'Cancel')
                               ], string="status", default="draft",
                              copy=False,tracking= True)
    # job_id = fields.Many2one(related="employee_name.job_id",string="Designation")
    # department_id = fields.Many2one(related="employee_name.department_id", string="Department")

    # You can use the related parameter instead of writing the api.onchange decorator so a field knows which data to get from the right model so it can auto-change

    def action_draft(self):
        self.status="draft"

    def action_request(self):
        self.status = "request"

    def action_approve(self):
        self.status = "approve"

    def action_reset(self):
        self.status="draft"

    def action_cancel(self):
        for record in self:
            if record.status == "approve":
                if record.employee_name and record.required == "True":
                    record.employee_name = False
                    record.designation = False
                    record.date_of_request = False
                    record.department = False
                    record.reference_number = False
                    record.remarks = False
            # Child Model Fields
            # Todo List: To be inherited (Work in Progress)
            # record.product_name = False
            # record.description = False
            # record.unit_of_measure = False
            # record.quantity= False
            # record.approved_quantity = False

    @api.onchange('employee_name')
    def onchange_employee_name(self):
        for record in self:
            if record.employee_name:
                record.designation = record.employee_name.job_id
                record.department = record.employee_name.department_id
            else:
                record.designation = False
                record.department = False

    # Function to create the sequence
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('sequence_id') or vals['sequence_id'] == _('New'):
                vals['sequence_id'] = self.env['ir.sequence'].next_by_code('purchase.request.sequence') or _('New')
        return super().create(vals_list)





