import asyncio
from typing import Dict, Optional

class TrendDetector:
    """YouTube trend-spike detection for high-ticket intervention"""
    
    def __init__(self):
        # Trigger Alpha velocity logic thresholds
        self.monitoring_threshold = 500      # views/hour = monitoring
        self.active_threshold = 2000         # views/hour = active intervention
        self.high_ticket_threshold = 5000    # views/hour = high-ticket
        
        # 24hr specific threshold (from Lead's instructions)
        self.daily_spike_threshold = 5000    # 5k views/24hr
        
        self.engagement_spike = 0.25         # 25% engagement spike
        self.velocity_spike = 0.50           # 50% velocity spike
        self.negative_sentiment_alert = 0.15 # Alert if negative sentiment > 15%
        
    def calculate_trend_velocity(
        self, 
        current_views: int, 
        previous_views: int
    ) -> float:
        """Calculate view velocity spike"""
        if previous_views == 0:
            return float(current_views)
        
        velocity = (current_views - previous_views) / previous_views
        return velocity
    
    def get_intervention_level(
        self, 
        views_per_hour: int, 
        engagement_rate: float
    ) -> str:
        """
        Determine when trend-spike transitions from 'monitoring' to 'active high-ticket intervention'
        """
        if views_per_hour < self.monitoring_threshold:
            return "MONITORING"
        elif views_per_hour < self.active_threshold:
            return "ACTIVE_INTERVENTION"
        elif views_per_hour < self.high_ticket_threshold:
            return "HIGH_TICKET_INTERVENTION"
        else:
            return "CRISIS_OROPPORTUNITY"
    
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
        
        # Avoid division by zero
        if previous_engagement == 0:
            engagement_spike = float(current_engagement)
        else:
            engagement_spike = (current_engagement - previous_engagement) / previous_engagement
        
        views_per_hour = current_views
        
        # Combine hourly and daily logic
        intervention_level = self.get_intervention_level(
            views_per_hour, 
            current_engagement
        )
        
        # Lead's 5k/24h override
        if views_24h >= self.daily_spike_threshold and intervention_level == "MONITORING":
            intervention_level = "ACTIVE_INTERVENTION"

        sentiment_alert = negative_sentiment_score > self.negative_sentiment_alert
        
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
            "ACTIVE_INTERVENTION": "Deploy content optimization, boost engagement",
            "HIGH_TICKET_INTERVENTION": "Activate high-ticket sales funnel, direct outreach",
            "CRISIS_OROPPORTUNITY": "Emergency response or capitalize on viral moment"
        }
        return actions[level]
