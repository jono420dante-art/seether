import unittest
from src.finance.invoicing_gate import InvoicingGate, MockStatusProvider

class TestInvoicingGate(unittest.TestCase):
    def test_all_gates_pass(self):
        provider = MockStatusProvider() # All True by default
        gate = InvoicingGate(provider)
        success, errors = gate.check_gates()
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
        self.assertTrue(gate.can_generate_invoice())

    def test_single_gate_fails(self):
        provider = MockStatusProvider({"HAS_UK_ENTITY": False})
        gate = InvoicingGate(provider)
        success, errors = gate.check_gates()
        self.assertFalse(success)
        self.assertIn("UK Entity is not active", errors[0])
        self.assertFalse(gate.can_generate_invoice())

    def test_multiple_gates_fail(self):
        provider = MockStatusProvider({
            "HAS_UK_ENTITY": False,
            "STRIPE_VERIFIED": False
        })
        gate = InvoicingGate(provider)
        success, errors = gate.check_gates()
        self.assertFalse(success)
        self.assertEqual(len(errors), 2)
        self.assertFalse(gate.can_generate_invoice())

    def test_vat_threshold_fail(self):
        provider = MockStatusProvider({"VAT_THRESHOLD_OK": False})
        gate = InvoicingGate(provider)
        success, errors = gate.check_gates()
        self.assertFalse(success)
        self.assertIn("VAT registration is required", errors[0])

if __name__ == "__main__":
    unittest.main()
