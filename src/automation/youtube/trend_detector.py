import asyncio
from typing import Dict, Optional

class TrendDetector:
    """YouTube trend-spike detection for high-ticket intervention"""
    
    def __init__(self):
        # Trigger Alpha Velocity-Acceleration (VA) thresholds
        self.monitoring_vph = 500
        self.monitoring_velocity = 0.10
        self.active_vph = 500
        self.active_velocity = 0.20
        self.high_ticket_vph = 2000
        self.high_ticket_velocity = 0.50
        self.crisis_vph = 5000
        self.crisis_velocity = 1.00
        
        # Lead's 5k/24h trigger & Sentiment alerts
        self.daily_spike_threshold = 5000
        self.negative_sentiment_alert = 0.15

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
        elif views_per_hour >= self.active_vph and velocity >= self.active_velocity:
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
        negative_sentiment_score: float = 0.0,
        views_24h: int = 0
    ) -> Dict:
        """Detect trend-spike and recommend intervention"""
        velocity = self.calculate_trend_velocity(current_views, previous_views)
        views_per_hour = current_views  # Assuming current_views is hourly for this logic
        
        intervention_level = self.get_intervention_level(
            views_per_hour,
            velocity
        )
        
        # Lead's 5k/24h override
        if views_24h >= self.daily_spike_threshold and intervention_level == "MONITORING":
            intervention_level = "ACTIVE_INTERVENTION"

        sentiment_alert = negative_sentiment_score > self.negative_sentiment_alert
        
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
            "sentiment_alert": sentiment_alert,
            "recommend_action": self.get_action_recommendation(intervention_level, sentiment_alert)
        }
        return result

    def get_action_recommendation(self, level: str, sentiment_alert: bool = False) -> str:
        """Get specific action for each intervention level"""
        if sentiment_alert:
            return "NEGATIVE SENTIMENT DETECTED: Deploy reputation management and audit comments."

        actions = {
            "MONITORING": "Continue monitoring, no action needed",
            "ACTIVE_INTERVENTION": "Deploy content optimization, boost MOFU offers",
            "HIGH_TICKET_INTERVENTION": "Activate high-ticket sales funnel, direct outbound",
            "CRISIS_OROPPORTUNITY": "Immediate Lead/CEO intervention, viral tender capture"
        }
        return actions.get(level, "No action defined")
