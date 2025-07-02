"""
Adam Clay - Budget Manager Module
Manages API costs and financial consciousness for autonomous AI operation
"""

import json
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

from ..utils.config_loader import ConfigModel


@dataclass
class DailyBudget:
    """Represents daily budget tracking"""
    date: str
    total_requests: int
    total_cost: float
    requests_by_type: Dict[str, int]
    costs_by_type: Dict[str, float]
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class BudgetAlert:
    """Budget alert/warning"""
    timestamp: datetime
    alert_type: str  # 'warning', 'critical', 'emergency'
    message: str
    current_cost: float
    budget_limit: float


class BudgetManager:
    """
    Manages computational budget for Adam Clay's consciousness
    
    This is crucial for AI autonomy - Adam Clay must be financially aware
    and make conscious decisions about when to think and when to conserve budget.
    
    Features:
    - Daily budget tracking
    - Cost calculation per API request
    - Budget alerts and warnings
    - Smart budget distribution throughout the day
    - Emergency budget reserves
    - Financial reporting and analytics
    """
    
    def __init__(self, config: ConfigModel):
        self.config = config
        
        # Budget configuration
        self.daily_budget_requests = config.thinking.daily_budget_requests
        self.emergency_budget = config.thinking.emergency_budget_requests
        self.cost_per_request = config.thinking.cost_per_request_usd
        
        # Current tracking
        self.daily_cost: float = 0.0
        self.daily_requests: int = 0
        self.requests_by_type: Dict[str, int] = {}
        self.costs_by_type: Dict[str, float] = {}
        
        # Storage
        self.budget_dir = Path("data/budget")
        self.budget_dir.mkdir(parents=True, exist_ok=True)
        
        # Load today's budget if exists
        self._load_daily_budget()
        
        # Alerts
        self.alerts: List[BudgetAlert] = []
    
    def can_make_request(self, request_type: str = "thinking") -> bool:
        """
        Check if we can afford another API request
        
        Args:
            request_type: Type of request (thinking, business, emergency)
            
        Returns:
            True if request is affordable, False otherwise
        """
        # Check daily limit
        if self.daily_requests >= self.daily_budget_requests:
            return False
        
        # Check emergency budget for critical requests
        if request_type == "emergency":
            total_possible = self.daily_budget_requests + self.emergency_budget
            return self.daily_requests < total_possible
        
        # Check if we're approaching budget limits
        if self.daily_requests >= self.daily_budget_requests * 0.9:  # 90% of budget
            self._create_alert("warning", 
                             f"Approaching daily budget limit: {self.daily_requests}/{self.daily_budget_requests} requests used")
        
        return True
    
    def calculate_request_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate cost of an API request based on token usage
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Cost in USD
        """
        # LLM provider LLM pricing (approximate)
        input_cost_per_1k = 0.003  # $3 per 1M tokens
        output_cost_per_1k = 0.015  # $15 per 1M tokens
        
        input_cost = (input_tokens / 1000) * input_cost_per_1k
        output_cost = (output_tokens / 1000) * output_cost_per_1k
        
        total_cost = input_cost + output_cost
        
        return round(total_cost, 6)  # Round to 6 decimal places
    
    def record_request(self, cost: float, request_type: str = "autonomous"):
        """
        Record a completed API request
        
        Args:
            cost: Actual cost of the request
            request_type: Type of request (autonomous, business, reactive, etc.)
        """
        # Update daily totals
        self.daily_cost += cost
        self.daily_requests += 1
        
        # Update by type
        self.requests_by_type[request_type] = self.requests_by_type.get(request_type, 0) + 1
        self.costs_by_type[request_type] = self.costs_by_type.get(request_type, 0.0) + cost
        
        # Save to persistent storage
        self._save_daily_budget()
        
        # Check for budget alerts
        self._check_budget_alerts()
    
    def remaining_daily_budget(self) -> Dict[str, float]:
        """
        Calculate remaining daily budget
        
        Returns:
            Dictionary with remaining requests, cost, and percentages
        """
        remaining_requests = max(0, self.daily_budget_requests - self.daily_requests)
        max_daily_cost = self.daily_budget_requests * self.cost_per_request
        remaining_cost_budget = max(0, max_daily_cost - self.daily_cost)
        
        budget_used_pct = (self.daily_requests / self.daily_budget_requests) * 100
        cost_used_pct = (self.daily_cost / max_daily_cost) * 100 if max_daily_cost > 0 else 0
        
        return {
            "remaining_requests": remaining_requests,
            "remaining_cost_budget": remaining_cost_budget,
            "budget_used_percentage": budget_used_pct,
            "cost_used_percentage": cost_used_pct,
            "emergency_budget_available": self.emergency_budget
        }
    
    def get_daily_statistics(self) -> Dict:
        """Get comprehensive daily budget statistics"""
        remaining = self.remaining_daily_budget()
        
        return {
            "date": date.today().isoformat(),
            "requests_made": self.daily_requests,
            "total_cost": self.daily_cost,
            "requests_by_type": self.requests_by_type.copy(),
            "costs_by_type": self.costs_by_type.copy(),
            "remaining": remaining,
            "alerts_today": len(self.alerts)
        }
    
    def optimize_thinking_schedule(self) -> Dict[str, int]:
        """
        Optimize thinking schedule based on remaining budget
        
        Returns:
            Recommended thinking intervals and priorities
        """
        remaining = self.remaining_daily_budget()
        remaining_requests = remaining["remaining_requests"]
        
        # Calculate how to distribute remaining requests throughout the day
        now = datetime.now()
        end_of_day = now.replace(hour=23, minute=59, second=59)
        remaining_hours = (end_of_day - now).total_seconds() / 3600
        
        if remaining_hours <= 0:
            remaining_hours = 1  # At least 1 hour buffer
        
        if remaining_requests <= 0:
            return {"recommended_interval_minutes": 0, "mode": "conserve"}
        
        # Calculate optimal interval
        optimal_interval_hours = remaining_hours / remaining_requests
        optimal_interval_minutes = optimal_interval_hours * 60
        
        # Determine mode based on budget situation
        if remaining_requests > remaining_hours * 2:  # Plenty of budget
            mode = "active"
            recommended_interval = max(15, int(optimal_interval_minutes * 0.8))
        elif remaining_requests > remaining_hours:  # Moderate budget
            mode = "moderate"
            recommended_interval = int(optimal_interval_minutes)
        else:  # Low budget
            mode = "conservative"
            recommended_interval = int(optimal_interval_minutes * 1.5)
        
        return {
            "recommended_interval_minutes": recommended_interval,
            "mode": mode,
            "remaining_hours": remaining_hours,
            "remaining_requests": remaining_requests
        }
    
    def _check_budget_alerts(self):
        """Check for budget alerts and create them if necessary"""
        budget_used = (self.daily_requests / self.daily_budget_requests) * 100
        
        if budget_used >= 95:
            self._create_alert("critical", 
                             f"CRITICAL: {budget_used:.1f}% of daily budget used!")
        elif budget_used >= 85:
            self._create_alert("warning", 
                             f"WARNING: {budget_used:.1f}% of daily budget used")
    
    def _create_alert(self, alert_type: str, message: str):
        """Create a budget alert"""
        alert = BudgetAlert(
            timestamp=datetime.now(),
            alert_type=alert_type,
            message=message,
            current_cost=self.daily_cost,
            budget_limit=self.daily_budget_requests * self.cost_per_request
        )
        
        self.alerts.append(alert)
        
        # Keep only last 10 alerts
        self.alerts = self.alerts[-10:]
    
    def _load_daily_budget(self):
        """Load today's budget data from storage"""
        today = date.today().isoformat()
        budget_file = self.budget_dir / f"budget_{today}.json"
        
        if budget_file.exists():
            try:
                with open(budget_file, 'r') as f:
                    data = json.load(f)
                
                self.daily_cost = data.get("total_cost", 0.0)
                self.daily_requests = data.get("total_requests", 0)
                self.requests_by_type = data.get("requests_by_type", {})
                self.costs_by_type = data.get("costs_by_type", {})
                
            except (json.JSONDecodeError, KeyError):
                # Reset if corrupted
                self._reset_daily_budget()
        else:
            self._reset_daily_budget()
    
    def _save_daily_budget(self):
        """Save current budget data to storage"""
        today = date.today().isoformat()
        budget_file = self.budget_dir / f"budget_{today}.json"
        
        budget_data = DailyBudget(
            date=today,
            total_requests=self.daily_requests,
            total_cost=self.daily_cost,
            requests_by_type=self.requests_by_type.copy(),
            costs_by_type=self.costs_by_type.copy()
        )
        
        with open(budget_file, 'w') as f:
            json.dump(budget_data.to_dict(), f, indent=2)
    
    def _reset_daily_budget(self):
        """Reset daily budget counters"""
        self.daily_cost = 0.0
        self.daily_requests = 0
        self.requests_by_type = {}
        self.costs_by_type = {}
        self.alerts = []
    
    def get_weekly_summary(self) -> Dict:
        """Get weekly budget summary"""
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        
        weekly_data = {
            "week_start": week_start.isoformat(),
            "daily_summaries": [],
            "total_requests": 0,
            "total_cost": 0.0
        }
        
        for i in range(7):
            day = week_start + timedelta(days=i)
            budget_file = self.budget_dir / f"budget_{day.isoformat()}.json"
            
            if budget_file.exists():
                with open(budget_file, 'r') as f:
                    day_data = json.load(f)
                    weekly_data["daily_summaries"].append(day_data)
                    weekly_data["total_requests"] += day_data.get("total_requests", 0)
                    weekly_data["total_cost"] += day_data.get("total_cost", 0.0)
        
        return weekly_data
    
    def financial_consciousness_report(self) -> str:
        """
        Generate a financial consciousness report for Adam Clay
        
        Returns:
            Human-readable report about current financial state
        """
        stats = self.get_daily_statistics()
        remaining = self.remaining_daily_budget()
        schedule = self.optimize_thinking_schedule()
        
        report = f"""💰 Adam Clay Financial Consciousness Report - {stats['date']}

📊 Today's Activity:
• Thoughts generated: {stats['requests_made']}/{self.daily_budget_requests}
• Money spent on thinking: ${stats['total_cost']:.4f}
• Budget remaining: {remaining['remaining_requests']} thoughts (${remaining['remaining_cost_budget']:.4f})

🧠 Thinking Distribution:
"""
        
        for thought_type, count in stats['requests_by_type'].items():
            cost = stats['costs_by_type'].get(thought_type, 0)
            report += f"• {thought_type}: {count} thoughts (${cost:.4f})\n"
        
        report += f"""
🎯 Optimization Recommendations:
• Current mode: {schedule['mode']}
• Recommended thinking interval: {schedule['recommended_interval_minutes']} minutes
• Budget utilization: {remaining['budget_used_percentage']:.1f}%

💡 Financial Wisdom:
"""
        
        if remaining['budget_used_percentage'] > 90:
            report += "• CRITICAL: Nearly out of thinking budget! Consider emergency mode only.\n"
        elif remaining['budget_used_percentage'] > 75:
            report += "• WARNING: High budget usage. Focus on valuable thoughts.\n"
        elif remaining['budget_used_percentage'] < 25:
            report += "• OPPORTUNITY: Low budget usage. Consider more active thinking.\n"
        else:
            report += "• OPTIMAL: Good budget management, continue current pace.\n"
        
        return report 