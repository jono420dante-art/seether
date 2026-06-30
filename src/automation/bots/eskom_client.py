import requests
import os
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class EskomClient:
    """
    Eskom Se Push Business API V2.0 Client.
    Handles real-time load-shedding status and schedule data.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ESKOM_API_KEY")
        self.base_url = "https://developer.sepush.co.za/business/2.0"
        self.mock_mode = self.api_key is None
        
        if self.mock_mode:
            logger.warning("ESKOM_API_KEY not found. Running in MOCK MODE.")

    def get_status(self) -> Dict:
        """
        Fetch the current load-shedding status (National/Regional).
        Returns the stage and source information.
        """
        if self.mock_mode:
            # High-fidelity mock for Stage 4 load-shedding (frequent in SA)
            return {
                "status": {
                    "capetown": {
                        "name": "Cape Town",
                        "next_stages": [{"stage": "4", "stage_start_timestamp": "2024-01-01T16:00:00+02:00"}],
                        "stage": "4"
                    },
                    "eskom": {
                        "name": "Eskom",
                        "next_stages": [{"stage": "4", "stage_start_timestamp": "2024-01-01T16:00:00+02:00"}],
                        "stage": "4"
                    }
                }
            }
        
        headers = {"token": self.api_key}
        try:
            response = requests.get(f"{self.base_url}/status", headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Eskom API Error: {e}")
            # Fallback to a safe 'Stage 2' if the API is down in production
            return {"status": {"eskom": {"stage": "2"}}}

    def get_area_status(self, area_id: str) -> int:
        """Helper to get current stage for a specific area, default to Eskom national."""
        data = self.get_status()
        status_map = data.get("status", {})
        
        # Check specific area or fall back to 'eskom' national
        area_data = status_map.get(area_id, status_map.get("eskom", {}))
        try:
            return int(area_data.get("stage", 0))
        except (ValueError, TypeError):
            return 0

if __name__ == "__main__":
    # Test Client
    client = EskomClient()
    print(f"Current Stage: {client.get_area_status('eskom')}")
