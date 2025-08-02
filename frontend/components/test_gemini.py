import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test the Gemini API integration"""
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("Test Gemini API Integration")
    
    # Get API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.error("GEMINI_API_KEY environment variable not set. Please check your .env file.")
        return
    
    # Display masked API key
    masked_key = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
    st.info(f"Using Gemini API Key: {masked_key}")
    
    # Test prompt input
    test_prompt = st.text_area(
        "Enter a test prompt for Gemini",
        "What are some tips for creating an emergency fund?",
        height=100
    )
    
    if st.button("Test Gemini API"):
        with st.spinner("Generating response from Gemini..."):
            try:
                # Configure Gemini API
                genai.configure(api_key=api_key)
                
                # Create Gemini model
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Generate response
                response = model.generate_content(test_prompt)
                
                # Display response
                st.subheader("Gemini Response:")
                st.markdown(response.text)
                st.success("Gemini API test successful!")
            except Exception as e:
                st.error(f"Error testing Gemini API: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)