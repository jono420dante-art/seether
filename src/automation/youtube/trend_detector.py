import asyncio
import json
import os
from typing import Dict, Optional

class TrendDetector:
    """YouTube trend-spike detection for high-ticket intervention"""
    
    def __init__(self, config_path: str = "/home/team/shared/src/automation/youtube/youtube_engine_config.json"):
        self.config_path = config_path
        # Lead's specific thresholds from my previous implementation
        self.daily_spike_threshold = 5000
        self.negative_sentiment_alert = 0.15
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                config = json.load(f)
            thresholds = config.get("thresholds", {})
            
            # Level 1: Monitoring
            self.monitoring_vph = thresholds.get("monitoring", {}).get("vph", 500)
            self.monitoring_velocity = thresholds.get("monitoring", {}).get("velocity", 0.10)
            
            # Level 2: Active Intervention
            self.active_vph = thresholds.get("active_intervention", {}).get("vph", 500)
            self.active_velocity = thresholds.get("active_intervention", {}).get("velocity", 0.20)
            
            # Level 3: High-Ticket Burst
            self.high_ticket_vph = thresholds.get("high_ticket_burst", {}).get("vph", 2000)
            self.high_ticket_velocity = thresholds.get("high_ticket_burst", {}).get("velocity", 0.50)
            
            # Level 4: Crisis/CEO Intervention
            self.crisis_vph = thresholds.get("crisis_ceo_intervention", {}).get("vph", 5000)
            self.crisis_velocity = thresholds.get("crisis_ceo_intervention", {}).get("velocity", 1.00)
            
            # Store actions
            self.actions = {
                "MONITORING": thresholds.get("monitoring", {}).get("action", "Continue monitoring"),
                "ACTIVE_INTERVENTION": thresholds.get("active_intervention", {}).get("action", "Deploy MOFU offers"),
                "HIGH_TICKET_INTERVENTION": thresholds.get("high_ticket_burst", {}).get("action", "Activate high-ticket funnel"),
                "CRISIS_OROPPORTUNITY": thresholds.get("crisis_ceo_intervention", {}).get("action", "CEO Intervention")
            }
        else:
            # Fallback to defaults
            self.monitoring_vph = 500
            self.monitoring_velocity = 0.10
            self.active_vph = 500
            self.active_velocity = 0.20
            self.high_ticket_vph = 2000
            self.high_ticket_velocity = 0.50
            self.crisis_vph = 5000
            self.crisis_velocity = 1.00
            self.actions = {
                "MONITORING": "Continue monitoring, no action needed",
                "ACTIVE_INTERVENTION": "Deploy content optimization, boost MOFU offers",
                "HIGH_TICKET_INTERVENTION": "Activate high-ticket sales funnel, direct outbound",
                "CRISIS_OROPPORTUNITY": "Immediate Lead/CEO intervention, viral tender capture"
            }

    def calculate_trend_velocity(
        self,
        current_views: int,
        previous_views: int
    ) -> float:
        """Calculate view velocity spike (acceleration)"""
        if previous_views == 0:
            return float(current_views)
        velocity = (current_views - previous_views) / previous_views
        return velocity

    def get_intervention_level(
        self,
        views_per_hour: int,
        velocity: float
    ) -> str:
        """
        Determine intervention level using Velocity-Acceleration (VA) logic.
        """
        if views_per_hour >= self.crisis_vph and velocity >= self.crisis_velocity:
            return "CRISIS_OROPPORTUNITY"
        elif views_per_hour >= self.high_ticket_vph and velocity >= self.high_ticket_velocity:
            return "HIGH_TICKET_INTERVENTION"
        elif (views_per_hour >= self.active_vph and velocity >= self.active_velocity):
            return "ACTIVE_INTERVENTION"
        else:
            return "MONITORING"

    async def detect_spike(
        self,
        video_id: str,
        current_views: int,
        previous_views: int,
        current_engagement: float,
        previous_engagement: float,
        views_24h: int = 0,
        negative_sentiment_score: float = 0.0
    ) -> Dict:
        """Detect trend-spike and recommend intervention"""
        velocity = self.calculate_trend_velocity(current_views, previous_views)
        
        # Velocity-Acceleration (VA) logic uses current_views as hourly proxy
        views_per_hour = current_views
        intervention_level = self.get_intervention_level(
            views_per_hour,
            velocity
        )
        
        # Additional Daily Burst Logic (Lead's Requirement)
        if views_24h >= self.daily_spike_threshold:
            if intervention_level == "MONITORING":
                intervention_level = "ACTIVE_INTERVENTION"
        
        # Sentiment-based Reputation Alert
        reputation_alert = False
        if negative_sentiment_score >= self.negative_sentiment_alert:
            reputation_alert = True
            
        engagement_spike = 0.0
        if previous_engagement > 0:
            engagement_spike = (current_engagement - previous_engagement) / previous_engagement
            
        result = {
            "video_id": video_id,
            "views_per_hour": views_per_hour,
            "views_24h": views_24h,
            "velocity_spike": velocity,
            "engagement_spike": engagement_spike,
            "intervention_level": intervention_level,
            "reputation_alert": reputation_alert,
            "recommend_action": self.get_action_recommendation(intervention_level, reputation_alert)
        }
        return result

    def get_action_recommendation(self, level: str, reputation_alert: bool = False) -> str:
        """Get specific action for each intervention level"""
        recommendation = self.actions.get(level, "No action defined")
        if reputation_alert:
            recommendation = f"ALERT: High Negative Sentiment. {recommendation} + Deploy Reputation Management."
            
        return recommendation
