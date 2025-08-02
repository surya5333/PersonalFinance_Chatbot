from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from services.gemini_handler import GeminiHandler
from services.granite_handler import GraniteHandler
from services.tax_utils import calculate_tax, compare_tax_regimes, calculate_hra_exemption
import json
import os
from datetime import datetime

router = APIRouter(tags=["chatbot"])

# Initialize AI handlers
gemini_handler = GeminiHandler()
granite_handler = GraniteHandler()

# Models
class UserProfile(BaseModel):
    user_id: str
    name: str
    income: float
    city_tier: int = Field(..., description="City tier (1, 2, or 3)")
    expenses: Dict[str, float] = {}
    goals: List[Dict[str, Any]] = []

class ChatMessage(BaseModel):
    user_id: str
    message: str
    voice_input: bool = False
    chat_history: Optional[List[Dict[str, str]]] = None

class ChatResponse(BaseModel):
    response: str
    audio_available: bool = False
    summary_available: bool = False
    tax_info: Optional[Dict[str, Any]] = None
    visualization_data: Optional[Dict[str, Any]] = None

class ExpenseEntry(BaseModel):
    user_id: str
    category: str
    amount: float
    description: Optional[str] = None
    date: str = Field(default_factory=lambda: datetime.now().isoformat())

class FinancialGoal(BaseModel):
    user_id: str
    goal_name: str
    target_amount: float
    current_amount: float = 0
    target_date: Optional[str] = None
    priority: int = 1  # 1 (highest) to 5 (lowest)

class TaxCalculationRequest(BaseModel):
    user_id: str
    income: float
    city_tier: int
    regime: str = "new"  # "old" or "new"

# Helper function to load/save chat history
def get_chat_history(user_id: str) -> List[Dict[str, str]]:
    try:
        with open("db/memory.json", "r") as f:
            data = json.load(f)
            return data.get(user_id, [])
    except (FileNotFoundError, json.JSONDecodeError):
        # Create directory if it doesn't exist
        os.makedirs("db", exist_ok=True)
        return []

def save_chat_history(user_id: str, history: List[Dict[str, str]]):
    try:
        with open("db/memory.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    
    data[user_id] = history
    
    with open("db/memory.json", "w") as f:
        json.dump(data, f, indent=2)

# Endpoints
@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    # Get chat history from request if provided, otherwise load from file
    history = message.chat_history if message.chat_history else get_chat_history(message.user_id)
    
    # Get user profile if available
    user_profile = None
    try:
        user_profile = await get_profile(message.user_id)
    except:
        # Profile not found, continue without it
        pass
    
    # Process message with Gemini
    response = await gemini_handler.generate_response(message.message, history, user_profile)
    
    # Update chat history
    history.append({"role": "user", "content": message.message})
    history.append({"role": "assistant", "content": response})
    save_chat_history(message.user_id, history)
    
    # Determine if this is a request that needs summary
    summary_available = "summary" in message.message.lower() or "budget" in message.message.lower()
    
    # Determine if this is a tax-related query
    tax_info = None
    if any(keyword in message.message.lower() for keyword in ["tax", "hra", "exemption", "regime"]):
        # This is a placeholder. In a real implementation, we would extract relevant
        # information from the message and calculate tax information.
        tax_info = {
            "message": "Tax information is available. Use the /tax endpoint for detailed calculations."
        }
    
    return ChatResponse(
        response=response,
        audio_available=True,  # We'll always make audio available
        summary_available=summary_available,
        tax_info=tax_info
    )

@router.post("/profile", response_model=UserProfile)
async def create_or_update_profile(profile: UserProfile):
    # Define the profiles directory
    PROFILES_DIR = "db/profiles"
    os.makedirs(PROFILES_DIR, exist_ok=True)
    
    # Save profile to file
    profile_path = os.path.join(PROFILES_DIR, f"{profile.user_id}.json")
    try:
        with open(profile_path, 'w') as f:
            json.dump(profile.dict(), f, indent=2)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving profile: {str(e)}")

@router.get("/profile/{user_id}", response_model=UserProfile)
async def get_profile(user_id: str):
    # Define the profiles directory
    PROFILES_DIR = "db/profiles"
    os.makedirs(PROFILES_DIR, exist_ok=True)
    
    # Check if profile exists
    profile_path = os.path.join(PROFILES_DIR, f"{user_id}.json")
    if not os.path.exists(profile_path):
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Load profile from file
    try:
        with open(profile_path, 'r') as f:
            profile_data = json.load(f)
            return UserProfile(**profile_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading profile: {str(e)}")

@router.post("/expense", response_model=ExpenseEntry)
async def add_expense(expense: ExpenseEntry):
    # In a real implementation, this would save to a database
    return expense

@router.post("/goal", response_model=FinancialGoal)
async def add_goal(goal: FinancialGoal):
    # In a real implementation, this would save to a database
    return goal

@router.post("/summary")
async def generate_summary(user_id: str = Body(..., embed=True)):
    # Get user profile (placeholder)
    profile = await get_profile(user_id)
    
    # Generate summary with Granite
    summary = await granite_handler.generate_budget_summary(profile)
    
    return {"summary": summary}

@router.post("/tax", response_model=Dict[str, Any])
async def calculate_tax_info(request: TaxCalculationRequest):
    # Calculate tax based on income and regime
    tax_amount = calculate_tax(request.income, request.regime)
    
    # If comparing regimes is requested
    comparison = None
    if request.regime == "compare":
        comparison = compare_tax_regimes(request.income)
    
    # Calculate HRA exemption if applicable
    hra_exemption = calculate_hra_exemption(request.income * 0.4, request.city_tier)  # Assuming HRA is 40% of income
    
    return {
        "tax_amount": tax_amount,
        "regime": request.regime,
        "hra_exemption": hra_exemption,
        "regime_comparison": comparison
    }