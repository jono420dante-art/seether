from services.neural_hub.finance.invoicing_gate import InvoicingGate, DbStatusProvider

class FinanceManager:
    """
    Higher-level manager for finance-related operations.
    Handles invoicing, payouts, and compliance checks.
    """
    def __init__(self):
        self.invoicing_gate = InvoicingGate(DbStatusProvider())

    def get_invoicing_status(self):
        """
        Returns the detailed invoicing status.
        """
        success, errors = self.invoicing_gate.check_gates()
        return {
            "can_generate_invoice": success,
            "blockers": errors,
            "status": self.invoicing_gate.status_provider.get_status()
        }

    def generate_invoice(self, data: dict):
        """
        Generates an invoice if the gates are cleared.
        """
        if not self.invoicing_gate.can_generate_invoice():
            raise Exception("Invoicing is currently blocked. Check compliance status.")
        
        # Logic for invoice generation would go here
        return {"status": "success", "invoice_id": "MOCK-INV-001"}
