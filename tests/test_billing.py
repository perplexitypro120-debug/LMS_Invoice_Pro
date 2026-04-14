import unittest
from decimal import Decimal
from src.billing import Billing, Invoice, InvoiceItem, InvoiceStatus

class TestBilling(unittest.TestCase):
    def setUp(self):
        self.billing = Billing()

    def test_create_invoice(self):
        invoice = self.billing.create_invoice("INV-001")
        self.assertEqual(invoice.invoice_id, "INV-001")
        self.assertEqual(invoice.status, InvoiceStatus.PENDING)
        self.assertEqual(len(invoice.items), 0)

    def test_create_duplicate_invoice(self):
        self.billing.create_invoice("INV-001")
        with self.assertRaises(ValueError):
            self.billing.create_invoice("INV-001")

    def test_add_item_to_invoice(self):
        self.billing.create_invoice("INV-001")
        self.billing.add_item_to_invoice("INV-001", "Course Fee", 100.0)
        invoice = self.billing.invoices["INV-001"]
        self.assertEqual(len(invoice.items), 1)
        self.assertEqual(invoice.items[0].description, "Course Fee")
        self.assertEqual(invoice.items[0].amount, Decimal("100.0"))

    def test_calculate_invoice_total(self):
        self.billing.create_invoice("INV-001")
        self.billing.add_item_to_invoice("INV-001", "Course Fee", 100.0)
        self.billing.add_item_to_invoice("INV-001", "Book Fee", 20.0)
        total = self.billing.calculate_invoice_total("INV-001")
        self.assertEqual(total, Decimal("120.0"))
        self.assertEqual(self.billing.invoices["INV-001"].total_amount, Decimal("120.0"))

    def test_process_payment(self):
        self.billing.create_invoice("INV-001")
        self.billing.process_payment("INV-001")
        self.assertEqual(self.billing.invoices["INV-001"].status, InvoiceStatus.PAID)

    def test_nonexistent_invoice(self):
        with self.assertRaises(ValueError):
            self.billing.add_item_to_invoice("INV-999", "Item", 10.0)
        with self.assertRaises(ValueError):
            self.billing.calculate_invoice_total("INV-999")
        with self.assertRaises(ValueError):
            self.billing.process_payment("INV-999")

if __name__ == "__main__":
    unittest.main()
