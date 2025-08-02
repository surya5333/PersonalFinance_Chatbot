import os
import sys
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test the Google Gemini API"""
    print("\n=== Testing Google Gemini API ===")
    
    # Get API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ GEMINI_API_KEY environment variable not set. Please check your .env file.")
        return False
    
    # Mask API key for display
    masked_key = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
    print(f"Using Gemini API Key: {masked_key}")
    
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Create Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate a simple response
        response = model.generate_content("Hello, what can you help me with regarding personal finance?")
        
        # Check if response is valid
        if response and response.text:
            print("✅ Gemini API test successful!")
            print(f"Response preview: {response.text[:100]}...")
            return True
        else:
            print("❌ Gemini API returned an empty response.")
            return False
    
    except Exception as e:
        print(f"❌ Error testing Gemini API: {str(e)}")
        return False

def test_huggingface_api():
    """Test the Hugging Face API"""
    print("\n=== Testing Hugging Face API ===")
    
    # Get API key from environment variable
    api_key = os.getenv("HF_API_KEY")
    
    if not api_key:
        print("❌ HF_API_KEY environment variable not set. Please check your .env file.")
        return False
    
    # Mask API key for display
    masked_key = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
    print(f"Using Hugging Face API Key: {masked_key}")
    
    try:
        # Set up API request
        api_url = "https://api-inference.huggingface.co/models/ibm/granite-2.5b-instruct-v1"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        # Create a simple payload
        payload = {
            "inputs": "<instruction>Generate a short tip about saving money.</instruction>\n\n<response>",
            "parameters": {
                "max_new_tokens": 100,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True
            }
        }
        
        # Make API request
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        # Check if response is valid
        result = response.json()
        if result and isinstance(result, list) and len(result) > 0:
            generated_text = result[0].get("generated_text", "")
            if generated_text:
                print("✅ Hugging Face API test successful!")
                print(f"Response preview: {generated_text[:100]}...")
                return True
        
        print("❌ Hugging Face API returned an invalid response.")
        print(f"Response: {result}")
        return False
    
    except Exception as e:
        print(f"❌ Error testing Hugging Face API: {str(e)}")
        return False

def main():
    """Main function to test API keys"""
    print("=== Personal Finance Chatbot API Key Test ===")
    print("This script will test your API keys to ensure they are working correctly.")
    
    # Test Gemini API
    gemini_success = test_gemini_api()
    
    # Test Hugging Face API
    hf_success = test_huggingface_api()
    
    # Print summary
    print("\n=== Test Summary ===")
    print(f"Google Gemini API: {'✅ Working' if gemini_success else '❌ Not Working'}")
    print(f"Hugging Face API: {'✅ Working' if hf_success else '❌ Not Working'}")
    
    if gemini_success and hf_success:
        print("\n✅ All API keys are working correctly! You're ready to run the application.")
        return 0
    else:
        print("\n❌ Some API keys are not working. Please check your .env file and API key validity.")
        return 1

if __name__ == "__main__":
    sys.exit(main())