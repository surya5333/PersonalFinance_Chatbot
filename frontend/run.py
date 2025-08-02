import os
import streamlit.web.cli as stcli
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_streamlit():
    """Run the Streamlit app"""
    # Get port from environment variable or use default
    port = int(os.getenv("FRONTEND_PORT", 8501))
    
    # Set Streamlit configuration
    os.environ["STREAMLIT_SERVER_PORT"] = str(port)
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "app.py")
    
    # Run the Streamlit app
    sys.argv = ["streamlit", "run", app_path, "--server.port", str(port)]
    sys.exit(stcli.main())

if __name__ == "__main__":
    print("Starting Personal Finance Chatbot Frontend...")
    run_streamlit()