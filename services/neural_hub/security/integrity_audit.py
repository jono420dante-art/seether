import hmac
import hashlib
import json
import datetime
import os

class IntegrityAuditor:
    """
    DIETER Zero-Trust Integrity Auditor.
    Implements HMAC-signed append-only logging to protect against procurement fraud
    and ensure data sovereignty as per Eskom L-001 requirements.
    """
    def __init__(self, secret_key: str = None):
        # In production, this key is sourced from a secure HSM or environment variable
        self.secret_key = (secret_key or os.getenv("SECRET_KEY", "default_tpd_secret")).encode()

    def sign_log(self, event_data: dict) -> str:
        """Signs an audit log entry using HMAC-SHA256."""
        # Ensure consistent serialization for deterministic signing
        message = json.dumps(event_data, sort_keys=True).encode()
        signature = hmac.new(self.secret_key, message, hashlib.sha256).hexdigest()
        return signature

    def create_audit_entry(self, agent_id: str, action: str, details: dict):
        """Creates a signed audit log entry."""
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "agent_id": agent_id,
            "action": action,
            "details": details
        }
        # Add the HMAC signature
        entry["signature"] = self.sign_log(entry)
        return entry

    def verify_entry(self, entry: dict) -> bool:
        """Verifies the signature of an audit log entry."""
        entry_copy = entry.copy()
        signature = entry_copy.pop("signature", None)
        if not signature:
            return False
        
        expected_signature = self.sign_log(entry_copy)
        return hmac.compare_digest(signature, expected_signature)

    def write_to_log(self, entry: dict, log_path: str = "/var/log/seether_audit.jsonl"):
        """Appends the signed entry to a JSONL log file."""
        try:
            with open(log_path, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            # Fallback to standard logging if file write fails
            print(f"Audit log write failure: {e}")
