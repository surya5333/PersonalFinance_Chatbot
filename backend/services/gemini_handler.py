import os
import google.generativeai as genai
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiHandler:
    def __init__(self):
        # Initialize Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Define system prompt
        self.system_prompt = """
        You are a personal finance assistant chatbot. Your goal is to provide helpful, 
        accurate, and personalized financial guidance. You can help with budgeting, 
        expense tracking, financial goal setting, investment advice, and tax information.
        
        When providing advice:
        1. Be specific and actionable
        2. Consider the user's financial situation
        3. Explain financial concepts in simple terms
        4. Provide balanced perspectives on investment options
        5. Clarify that you're providing general guidance, not professional financial advice
        
        For tax-related questions, focus on Indian tax system including:
        - Income tax slabs for old and new regimes
        - HRA exemptions based on city tier
        - Standard deductions and exemptions
        - Tax-saving investment options under Section 80C
        
        Always maintain a helpful, encouraging tone while being realistic about financial situations.
        """
    
    async def generate_response(self, user_message: str, chat_history: List[Dict[str, str]] = None, user_profile: Dict = None) -> str:
        """Generate a response using Gemini model with user profile context"""
        try:
            # Format chat history for Gemini
            formatted_history = []
            
            if chat_history:
                for message in chat_history:
                    role = "user" if message["role"] == "user" else "model"
                    formatted_history.append({"role": role, "parts": [message["content"]]})
            
            # Add system prompt if this is a new conversation
            if not formatted_history:
                formatted_history.append({"role": "model", "parts": [self.system_prompt]})
            
            # Add user profile context if available
            profile_context = ""
            if user_profile:
                # Calculate total expenses and savings
                total_expenses = sum(user_profile.expenses.values())
                savings = user_profile.income - total_expenses
                savings_rate = (savings / user_profile.income) * 100 if user_profile.income > 0 else 0
                
                profile_context = f"""
                User Profile Information:
                Name: {user_profile.name}
                Monthly Income: ₹{user_profile.income:,.2f}
                City Tier: {user_profile.city_tier}
                
                Monthly Expenses:
                {', '.join([f'{category}: ₹{amount}' for category, amount in user_profile.expenses.items() if amount > 0])}
                
                Total Expenses: ₹{total_expenses:,.2f}
                Monthly Savings: ₹{savings:,.2f} ({savings_rate:.1f}%)
                
                Based on this profile, provide personalized advice that addresses their specific financial situation.
                """
                
                # Add profile context as a system message
                formatted_history.append({"role": "model", "parts": [profile_context]})
            
            # Add current user message
            formatted_history.append({"role": "user", "parts": [user_message]})
            
            # Generate response
            chat = self.model.start_chat(history=formatted_history)
            response = chat.send_message(user_message)
            
            return response.text
        
        except Exception as e:
            print(f"Error generating response from Gemini: {str(e)}")
            return f"I'm having trouble processing your request. Please try again later. Error: {str(e)}"
    
    async def generate_spending_insights(self, expenses: Dict[str, float], income: float) -> str:
        """Generate insights about spending patterns"""
        try:
            # Create prompt for spending insights
            prompt = f"""
            Based on the following financial information, provide insights and recommendations:
            
            Monthly Income: ₹{income}
            
            Monthly Expenses:
            {', '.join([f'{category}: ₹{amount}' for category, amount in expenses.items()])}
            
            Please analyze:
            1. Spending patterns and potential areas to reduce expenses
            2. Savings rate and recommendations to improve it
            3. Budget allocation suggestions based on the 50/30/20 rule
            4. Any potential financial risks or imbalances
            """
            
            # Generate insights
            response = self.model.generate_content(prompt)
            
            return response.text
        
        except Exception as e:
            print(f"Error generating spending insights: {str(e)}")
            return f"I'm having trouble analyzing your expenses. Please try again later. Error: {str(e)}"
    
    async def generate_investment_advice(self, risk_tolerance: str, goals: List[Dict[str, Any]], 
                                        time_horizon: str, current_investments: Dict[str, float] = None) -> str:
        """Generate personalized investment advice"""
        try:
            # Format current investments if provided
            investments_text = "No current investments provided."
            if current_investments:
                investments_text = ", ".join([f"{inv_type}: ₹{amount}" for inv_type, amount in current_investments.items()])
            
            # Format goals
            goals_text = "\n".join([f"- {goal['goal_name']}: ₹{goal['target_amount']} by {goal.get('target_date', 'No date specified')}" 
                                for goal in goals])
            
            # Create prompt for investment advice
            prompt = f"""
            Based on the following investor profile, provide personalized investment advice:
            
            Risk Tolerance: {risk_tolerance}
            Time Horizon: {time_horizon}
            
            Financial Goals:
            {goals_text}
            
            Current Investments:
            {investments_text}
            
            Please provide:
            1. Asset allocation recommendations based on risk tolerance and time horizon
            2. Specific investment vehicles suitable for the goals (mutual funds, stocks, bonds, etc.)
            3. Considerations for tax-efficient investing
            4. Suggestions for regular review and rebalancing
            
            Note: Frame this as general guidance, not professional financial advice.
            """
            
            # Generate advice
            response = self.model.generate_content(prompt)
            
            return response.text
        
        except Exception as e:
            print(f"Error generating investment advice: {str(e)}")
            return f"I'm having trouble generating investment advice. Please try again later. Error: {str(e)}"