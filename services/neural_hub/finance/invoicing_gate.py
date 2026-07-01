import logging
import json
import subprocess
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)

class InvoicingGate:
    """
    Implements the boolean gating logic for invoice generation.
    Based on TPD's UK Stripe Setup requirements.
    """

    def __init__(self, status_provider):
        self.status_provider = status_provider

    def check_gates(self) -> Tuple[bool, List[str]]:
        """
        Evaluates all boolean gates required for invoicing.
        Returns:
            Tuple[bool, List[str]]: (Success Status, List of error messages for blocking gates)
        """
        status = self.status_provider.get_status()
        errors = []

        if not status.get("HAS_UK_ENTITY"):
            errors.append("UK Entity is not active or verified with Companies House.")
        
        if not status.get("BANK_LINKED"):
            errors.append("No business bank account (Wise/Revolut) is linked to Stripe.")

        if not status.get("STRIPE_VERIFIED"):
            errors.append("Stripe KYC/Identity verification is incomplete.")

        if not status.get("VAT_THRESHOLD_OK"):
            errors.append("Projected revenue exceeds £90k; UK VAT registration is required.")

        if not status.get("SARB_COMPLIANT"):
            errors.append("SARB Exchange Control Declaration must be confirmed by the founder.")

        success = len(errors) == 0
        return success, errors

    def can_generate_invoice(self) -> bool:
        """
        Helper function to check if invoice generation is enabled.
        """
        success, errors = self.check_gates()
        if not success:
            for error in errors:
                logger.warning(f"Invoicing Blocked: {error}")
        return success

class MockStatusProvider:
    def __init__(self, overrides: Optional[Dict] = None):
        self.status = {
            "HAS_UK_ENTITY": True,
            "BANK_LINKED": True,
            "STRIPE_VERIFIED": True,
            "VAT_THRESHOLD_OK": True,
            "SARB_COMPLIANT": True
        }
        if overrides:
            self.status.update(overrides)

    def get_status(self) -> Dict:
        return self.status

class DbStatusProvider:
    """
    Status provider that reads from the team-db config table.
    """
    def get_status(self) -> Dict:
        try:
            # Query team-db for finance-related config
            # We assume keys like 'finance_has_uk_entity', etc. exist or we default to False.
            query = "SELECT key, value FROM config WHERE key LIKE 'finance_%'"
            result = subprocess.check_output(["team-db", query], text=True)
            config_rows = json.loads(result)
            
            config = {row["key"]: row["value"] for row in config_rows}
            
            return {
                "HAS_UK_ENTITY": config.get("finance_has_uk_entity") == "true",
                "BANK_LINKED": config.get("finance_bank_linked") == "true",
                "STRIPE_VERIFIED": config.get("finance_stripe_verified") == "true",
                "VAT_THRESHOLD_OK": config.get("finance_vat_threshold_ok") == "true",
                "SARB_COMPLIANT": config.get("finance_sarb_compliant") == "true"
            }
        except Exception as e:
            logger.error(f"Failed to fetch status from team-db: {e}")
            return {
                "HAS_UK_ENTITY": False,
                "BANK_LINKED": False,
                "STRIPE_VERIFIED": False,
                "VAT_THRESHOLD_OK": False,
                "SARB_COMPLIANT": False
            }
