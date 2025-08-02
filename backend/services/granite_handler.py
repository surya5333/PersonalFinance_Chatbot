import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GraniteHandler:
    def __init__(self):
        # Initialize Hugging Face API
        self.api_key = os.getenv("HF_API_KEY")
        if not self.api_key:
            raise ValueError("HF_API_KEY environment variable not set")
        
        self.api_url = "https://api-inference.huggingface.co/models/ibm/granite-2.5b-instruct-v1"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
    
    async def generate_budget_summary(self, user_profile: Dict[str, Any]) -> str:
        """Generate a comprehensive budget summary using IBM Granite"""
        try:
            # Extract relevant information from user profile
            income = user_profile.get("income", 0)
            expenses = user_profile.get("expenses", {})
            goals = user_profile.get("goals", [])
            
            # Calculate total expenses
            total_expenses = sum(expenses.values())
            
            # Calculate savings
            savings = income - total_expenses
            savings_rate = (savings / income) * 100 if income > 0 else 0
            
            # Format expenses for the prompt
            expenses_text = "\n".join([f"- {category}: ₹{amount} ({(amount/income)*100:.1f}% of income)" 
                                    for category, amount in expenses.items()])
            
            # Format goals for the prompt
            goals_text = "No financial goals set."
            if goals:
                goals_text = "\n".join([f"- {goal['goal_name']}: ₹{goal['target_amount']} " + 
                                    f"(Currently at ₹{goal.get('current_amount', 0)}, " + 
                                    f"{(goal.get('current_amount', 0)/goal['target_amount'])*100:.1f}% complete)" 
                                    for goal in goals])
            
            # Create prompt for budget summary
            prompt = f"""
            <instruction>Generate a comprehensive budget summary based on the following financial information. 
            Include analysis of spending patterns, savings rate, progress towards goals, and actionable recommendations 
            for improving financial health.</instruction>
            
            Monthly Income: ₹{income}
            
            Monthly Expenses (Total: ₹{total_expenses}, {(total_expenses/income)*100:.1f}% of income):
            {expenses_text}
            
            Monthly Savings: ₹{savings} ({savings_rate:.1f}% of income)
            
            Financial Goals:
            {goals_text}
            
            <response>
            """
            
            # Make API request to Granite
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True
                }
            }
            
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            # Extract and return the generated text
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "").replace(prompt, "").strip()
            else:
                return "Unable to generate budget summary. Please try again later."
        
        except Exception as e:
            print(f"Error generating budget summary: {str(e)}")
            return f"I'm having trouble generating your budget summary. Please try again later. Error: {str(e)}"