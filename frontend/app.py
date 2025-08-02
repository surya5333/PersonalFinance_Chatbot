import streamlit as st
import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from components.chat_ui import render_chat_interface
from components.tax_graph import render_tax_comparison
from components.summary_tools import render_summary_tools
from components.voice_translator import VoiceTranslator
from components.summary_section import render_summary_section

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Personal Finance Chatbot",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_id" not in st.session_state:
    st.session_state.user_id = "user_" + os.urandom(4).hex()

if "profile" not in st.session_state:
    st.session_state.profile = None

if "voice_translator" not in st.session_state:
    st.session_state.voice_translator = VoiceTranslator()

# API endpoint
BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = os.getenv("BACKEND_PORT", "8000")
API_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}/api/v1"

# Custom CSS for glassmorphism effect with Unsplash background image
st.markdown("""
<style>
    .main {
        background-color: rgba(255, 255, 255, 0.1);
    }
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1951&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .glass-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 20px;
        margin-bottom: 20px;
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: rgba(0, 13, 255, 0.2);
        border: 1px solid rgba(0, 13, 255, 0.3);
        align-self: flex-end;
    }
    .bot-message {
        background-color: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        align-self: flex-start;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown("""
<div class="glass-container">
    <h1 style="color: white; text-align: center;">💰 Personal Finance Chatbot</h1>
    <p style="color: white; text-align: center;">Your AI-powered financial assistant</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for user profile
with st.sidebar:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("Your Financial Profile")
    
    # Profile form
    with st.form("profile_form"):
        name = st.text_input("Name", value=st.session_state.profile["name"] if st.session_state.profile else "")
        income = st.number_input("Monthly Income (₹)", min_value=0.0, value=st.session_state.profile["income"] if st.session_state.profile else 0.0)
        city_tier = st.selectbox("City Tier", [1, 2, 3], index=0 if not st.session_state.profile else st.session_state.profile["city_tier"]-1)
        
        st.subheader("Monthly Expenses")
        housing = st.number_input("Housing (₹)", min_value=0.0, value=st.session_state.profile["expenses"].get("Housing", 0.0) if st.session_state.profile else 0.0)
        food = st.number_input("Food (₹)", min_value=0.0, value=st.session_state.profile["expenses"].get("Food", 0.0) if st.session_state.profile else 0.0)
        transportation = st.number_input("Transportation (₹)", min_value=0.0, value=st.session_state.profile["expenses"].get("Transportation", 0.0) if st.session_state.profile else 0.0)
        utilities = st.number_input("Utilities (₹)", min_value=0.0, value=st.session_state.profile["expenses"].get("Utilities", 0.0) if st.session_state.profile else 0.0)
        entertainment = st.number_input("Entertainment (₹)", min_value=0.0, value=st.session_state.profile["expenses"].get("Entertainment", 0.0) if st.session_state.profile else 0.0)
        
        submit_button = st.form_submit_button("Update Profile")
        
        if submit_button:
            # Create profile object
            profile = {
                "user_id": st.session_state.user_id,
                "name": name,
                "income": income,
                "city_tier": city_tier,
                "expenses": {
                    "Housing": housing,
                    "Food": food,
                    "Transportation": transportation,
                    "Utilities": utilities,
                    "Entertainment": entertainment
                }
            }
            
            # Save profile to session state
            st.session_state.profile = profile
            
            # Send profile to backend
            try:
                response = requests.post(f"{API_URL}/profile", json=profile)
                if response.status_code == 200:
                    st.success("Profile updated successfully!")
                else:
                    st.error(f"Failed to update profile: {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Display financial summary if profile exists
    if st.session_state.profile:
        total_expenses = sum(st.session_state.profile["expenses"].values())
        savings = st.session_state.profile["income"] - total_expenses
        savings_rate = (savings / st.session_state.profile["income"]) * 100 if st.session_state.profile["income"] > 0 else 0
        
        st.markdown("### Financial Summary")
        st.markdown(f"**Monthly Income:** ₹{st.session_state.profile['income']:,.2f}")
        st.markdown(f"**Total Expenses:** ₹{total_expenses:,.2f}")
        st.markdown(f"**Monthly Savings:** ₹{savings:,.2f} ({savings_rate:.1f}%)")
        
        # Simple expense breakdown chart
        if total_expenses > 0:
            st.markdown("### Expense Breakdown")
            expenses_data = st.session_state.profile["expenses"]
            expenses_labels = list(expenses_data.keys())
            expenses_values = list(expenses_data.values())
            
            # Filter out zero values
            filtered_labels = [label for label, value in zip(expenses_labels, expenses_values) if value > 0]
            filtered_values = [value for value in expenses_values if value > 0]
            
            if filtered_values:
                st.bar_chart({label: [value] for label, value in zip(filtered_labels, filtered_values)})
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main content area with tabs
tab1, tab2, tab3, tab4 = st.tabs(["Chat", "Tax Calculator", "Financial Goals", "Summary"])

# Tab 1: Chat Interface
with tab1:
    render_chat_interface(API_URL)

# Tab 2: Tax Calculator
with tab2:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("Tax Calculator")
    
    with st.form("tax_calculator_form"):
        tax_income = st.number_input("Annual Income (₹)", min_value=0.0, value=st.session_state.profile["income"]*12 if st.session_state.profile else 0.0)
        tax_city_tier = st.selectbox("City Tier for HRA", [1, 2, 3], index=0 if not st.session_state.profile else st.session_state.profile["city_tier"]-1)
        tax_regime = st.radio("Tax Regime", ["New", "Old", "Compare"], index=0)
        
        calculate_button = st.form_submit_button("Calculate Tax")
        
        if calculate_button:
            try:
                response = requests.post(
                    f"{API_URL}/tax", 
                    json={
                        "user_id": st.session_state.user_id,
                        "income": tax_income,
                        "city_tier": tax_city_tier,
                        "regime": tax_regime.lower()
                    }
                )
                
                if response.status_code == 200:
                    tax_info = response.json()
                    
                    if tax_regime.lower() == "compare":
                        # Display tax comparison
                        st.markdown("### Tax Regime Comparison")
                        st.markdown(f"**Old Regime Tax:** ₹{tax_info['regime_comparison']['old_regime_tax']:,.2f}")
                        st.markdown(f"**New Regime Tax:** ₹{tax_info['regime_comparison']['new_regime_tax']:,.2f}")
                        st.markdown(f"**Savings with {tax_info['regime_comparison']['better_regime'].title()} Regime:** ₹{tax_info['regime_comparison']['savings']:,.2f}")
                        
                        # Create a section for tax visualizations
                        st.markdown("### Tax Visualizations")
                        
                        # Create tabs for different visualizations
                        viz_tab1, viz_tab2 = st.tabs(["Tax Comparison", "Tax Breakdown"])
                        
                        with viz_tab1:
                            # Render tax comparison graph
                            render_tax_comparison(tax_info['regime_comparison']['visualization_data'])
                        
                        with viz_tab2:
                            # Placeholder for tax breakdown visualization
                            st.info("Detailed tax breakdown visualization will be shown here.")
                            
                        # Add PDF download for tax summary
                        tax_summary = f"""# Tax Calculation Summary

## User Information
Annual Income: ₹{tax_income:,.2f}
City Tier: {tax_city_tier}

## Tax Regime Comparison
Old Regime Tax: ₹{tax_info['regime_comparison']['old_regime_tax']:,.2f}
New Regime Tax: ₹{tax_info['regime_comparison']['new_regime_tax']:,.2f}
Savings with {tax_info['regime_comparison']['better_regime'].title()} Regime: ₹{tax_info['regime_comparison']['savings']:,.2f}

## HRA Exemption
HRA Exemption Amount: ₹{tax_info['hra_exemption']['exemption_amount']:,.2f}
City Tier: {tax_info['hra_exemption']['city_tier']}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                        
                        from components.summary_tools import generate_pdf
                        pdf_bytes = generate_pdf(tax_summary)
                        st.download_button(
                            label="📄 Download Tax Summary as PDF",
                            data=pdf_bytes,
                            file_name=f"tax_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            help="Download tax summary as PDF"
                        )
                    else:
                        # Display tax calculation
                        st.markdown(f"### {tax_regime} Regime Tax Calculation")
                        st.markdown(f"**Total Tax:** ₹{tax_info['tax_amount']:,.2f}")
                    
                    # Display HRA exemption
                    st.markdown("### HRA Exemption")
                    st.markdown(f"**HRA Exemption Amount:** ₹{tax_info['hra_exemption']['exemption_amount']:,.2f}")
                    st.markdown(f"**City Tier:** {tax_info['hra_exemption']['city_tier']}")
                else:
                    st.error(f"Failed to calculate tax: {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3: Financial Goals
with tab3:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("Financial Goals")
    
    # Add new goal form
    with st.form("add_goal_form"):
        st.subheader("Add New Goal")
        goal_name = st.text_input("Goal Name")
        target_amount = st.number_input("Target Amount (₹)", min_value=0.0)
        current_amount = st.number_input("Current Amount (₹)", min_value=0.0)
        target_date = st.date_input("Target Date (Optional)")
        priority = st.slider("Priority", 1, 5, 3, help="1 = Highest Priority, 5 = Lowest Priority")
        
        add_goal_button = st.form_submit_button("Add Goal")
        
        if add_goal_button and goal_name and target_amount > 0:
            # Create goal object
            goal = {
                "user_id": st.session_state.user_id,
                "goal_name": goal_name,
                "target_amount": target_amount,
                "current_amount": current_amount,
                "target_date": target_date.isoformat() if target_date else None,
                "priority": priority
            }
            
            # Add goal to profile
            if not st.session_state.profile:
                st.session_state.profile = {
                    "user_id": st.session_state.user_id,
                    "name": "",
                    "income": 0.0,
                    "city_tier": 1,
                    "expenses": {},
                    "goals": []
                }
            
            if "goals" not in st.session_state.profile:
                st.session_state.profile["goals"] = []
            
            st.session_state.profile["goals"].append(goal)
            
            # Send goal to backend
            try:
                response = requests.post(f"{API_URL}/goal", json=goal)
                if response.status_code == 200:
                    st.success("Goal added successfully!")
                else:
                    st.error(f"Failed to add goal: {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Display existing goals
    if st.session_state.profile and "goals" in st.session_state.profile and st.session_state.profile["goals"]:
        st.subheader("Your Financial Goals")
        
        for i, goal in enumerate(st.session_state.profile["goals"]):
            progress = (goal["current_amount"] / goal["target_amount"]) * 100 if goal["target_amount"] > 0 else 0
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{goal['goal_name']}** (Priority: {goal['priority']})")
                st.progress(progress / 100)
                st.markdown(f"₹{goal['current_amount']:,.2f} of ₹{goal['target_amount']:,.2f} ({progress:.1f}%)")
                if goal.get("target_date"):
                    st.markdown(f"Target Date: {goal['target_date']}")
            
            with col2:
                if st.button("Update", key=f"update_goal_{i}"):
                    st.session_state.goal_to_update = i
                
                if st.button("Delete", key=f"delete_goal_{i}"):
                    st.session_state.profile["goals"].pop(i)
                    st.rerun()
        
        # Update goal form (shown when an update button is clicked)
        if "goal_to_update" in st.session_state:
            i = st.session_state.goal_to_update
            goal = st.session_state.profile["goals"][i]
            
            st.markdown("### Update Goal")
            with st.form(f"update_goal_form_{i}"):
                updated_current_amount = st.number_input("Current Amount (₹)", min_value=0.0, value=goal["current_amount"])
                updated_priority = st.slider("Priority", 1, 5, goal["priority"])
                
                update_button = st.form_submit_button("Save Changes")
                
                if update_button:
                    # Update goal in session state
                    st.session_state.profile["goals"][i]["current_amount"] = updated_current_amount
                    st.session_state.profile["goals"][i]["priority"] = updated_priority
                    
                    # Clear update state
                    del st.session_state.goal_to_update
                    st.rerun()
    else:
        st.info("You haven't set any financial goals yet. Add your first goal above!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 4: Summary
with tab4:
    # Render the summary section with visualizations
    render_summary_section(API_URL)

# Footer
st.markdown("""
<div class="glass-container" style="text-align: center; color: white;">
    <p>Personal Finance Chatbot | Powered by Google Gemini & IBM Granite</p>
</div>
""", unsafe_allow_html=True)