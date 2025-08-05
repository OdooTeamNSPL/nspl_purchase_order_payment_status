from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    payment_status = fields.Selection([
        ('no_invoice', 'No Invoice'),
        ('not_paid', 'Not Paid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Fully Paid'),
        ('overdue', 'Overdue'),
    ], string="Payment Status", compute="_compute_payment_status", store=True)

    amount_due = fields.Monetary(
        string="Amount Due",
        compute="_compute_payment_status",
        store=True,
        currency_field='currency_id',
        help='Total amount due for this purchase order based on related vendor bills.'
    )

    @api.depends('invoice_ids.state', 'invoice_ids.payment_ids.amount', 'invoice_ids.amount_total', 'invoice_ids.invoice_date_due')
    @api.depends('invoice_ids.state', 'invoice_ids.amount_total', 'invoice_ids.amount_residual',
                 'invoice_ids.invoice_date_due')
    def _compute_payment_status(self):
        for order in self:
            invoices = order.invoice_ids.filtered(
                lambda inv: inv.move_type == 'in_invoice' and inv.state == 'posted'
            )

            if not invoices:
                order.payment_status = 'no_invoice'
                order.amount_due = order.amount_total
                continue

            total_amount = sum(inv.amount_total for inv in invoices)
            total_residual = sum(inv.amount_residual for inv in invoices)

            currency = order.currency_id or order.company_id.currency_id
            total_residual = currency.round(total_residual)
            order.amount_due = total_residual

            today = fields.Date.today()
            overdue_invoices = invoices.filtered(
                lambda inv: inv.invoice_date_due and inv.invoice_date_due < today and not currency.is_zero(
                    inv.amount_residual)
            )

            if overdue_invoices:
                order.payment_status = 'overdue'
            elif currency.is_zero(total_residual):
                order.payment_status = 'paid'
            elif 0 < total_residual < total_amount:
                order.payment_status = 'partial'
            else:
                order.payment_status = 'not_paid'

