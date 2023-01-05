import os

from utils.invoice import Invoice
from models.debt import Debts

class TestInvoice():
    def test_generate_invoice(self) -> None:
        if os.path.exists("boleto.pdf"):
            os.remove("boleto.pdf")

        invoice = Invoice(12345, '10/10/2020', 500)

        invoice.generate_pdf()

        assert os.path.exists("boleto.pdf")
        os.remove("boleto.pdf")