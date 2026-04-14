from decimal import Decimal
from enum import Enum

class InvoiceStatus(Enum):
    PENDING = "PENDING"
    PAID = "PAID"

class InvoiceItem:
    def __init__(self, description, amount):
        self.description = description
        self.amount = Decimal(str(amount))

class Invoice:
    def __init__(self, invoice_id):
        self.invoice_id = invoice_id
        self.items = []
        self.total_amount = Decimal("0.00")
        self.status = InvoiceStatus.PENDING

    def add_item(self, item):
        self.items.append(item)
        self.calculate_total()

    def calculate_total(self):
        self.total_amount = sum((item.amount for item in self.items), Decimal("0.00"))
        return self.total_amount

class Billing:
    def __init__(self):
        self.invoices = {}

    def create_invoice(self, invoice_id):
        if invoice_id in self.invoices:
            raise ValueError(f"Invoice with ID {invoice_id} already exists.")
        invoice = Invoice(invoice_id)
        self.invoices[invoice_id] = invoice
        return invoice

    def add_item_to_invoice(self, invoice_id, description, amount):
        if invoice_id not in self.invoices:
            raise ValueError(f"Invoice with ID {invoice_id} not found.")
        item = InvoiceItem(description, amount)
        self.invoices[invoice_id].add_item(item)

    def calculate_invoice_total(self, invoice_id):
        if invoice_id not in self.invoices:
            raise ValueError(f"Invoice with ID {invoice_id} not found.")
        return self.invoices[invoice_id].calculate_total()

    def process_payment(self, invoice_id):
        if invoice_id not in self.invoices:
            raise ValueError(f"Invoice with ID {invoice_id} not found.")
        self.invoices[invoice_id].status = InvoiceStatus.PAID
