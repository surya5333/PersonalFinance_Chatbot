import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

def format_currency(amount: float) -> str:
    """Format a number as Indian currency (₹)"""
    return f"₹{amount:,.2f}"

def calculate_savings_rate(income: float, expenses: Dict[str, float]) -> float:
    """Calculate savings rate as a percentage"""
    if income <= 0:
        return 0.0
    
    total_expenses = sum(expenses.values())
    savings = income - total_expenses
    savings_rate = (savings / income) * 100
    
    return savings_rate

def calculate_goal_progress(current_amount: float, target_amount: float) -> float:
    """Calculate progress towards a financial goal as a percentage"""
    if target_amount <= 0:
        return 0.0
    
    progress = (current_amount / target_amount) * 100
    return min(progress, 100.0)  # Cap at 100%

def get_city_tier_name(tier: int) -> str:
    """Get the name for a city tier"""
    tier_names = {
        1: "Metro/Tier 1",
        2: "Tier 2",
        3: "Tier 3"
    }
    
    return tier_names.get(tier, "Unknown")

def get_expense_category_emoji(category: str) -> str:
    """Get an emoji for an expense category"""
    category_emojis = {
        "Housing": "🏠",
        "Food": "🍔",
        "Transportation": "🚗",
        "Utilities": "💡",
        "Entertainment": "🎬",
        "Shopping": "🛍️",
        "Healthcare": "⚕️",
        "Education": "📚",
        "Travel": "✈️",
        "Savings": "💰",
        "Investments": "📈",
        "Debt": "💳",
        "Insurance": "🔒",
        "Taxes": "📝",
        "Gifts": "🎁",
        "Miscellaneous": "🔄"
    }
    
    return category_emojis.get(category, "💼")

def load_json_file(file_path: str, default_value: Any = None) -> Any:
    """Load data from a JSON file"""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default_value

def save_json_file(file_path: str, data: Any) -> bool:
    """Save data to a JSON file"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving JSON file: {str(e)}")
        return False

def get_date_difference_text(date_str: str) -> str:
    """Get a human-readable text for the difference between a date and today"""
    try:
        target_date = datetime.fromisoformat(date_str)
        today = datetime.now()
        
        diff = target_date - today
        
        if diff.days < 0:
            return "Past due"
        elif diff.days == 0:
            return "Today"
        elif diff.days == 1:
            return "Tomorrow"
        elif diff.days < 7:
            return f"{diff.days} days left"
        elif diff.days < 30:
            weeks = diff.days // 7
            return f"{weeks} {'week' if weeks == 1 else 'weeks'} left"
        elif diff.days < 365:
            months = diff.days // 30
            return f"{months} {'month' if months == 1 else 'months'} left"
        else:
            years = diff.days // 365
            return f"{years} {'year' if years == 1 else 'years'} left"
    except (ValueError, TypeError):
        return "No date specified"