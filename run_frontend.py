import os
import sys
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Run the frontend server"""
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
    frontend_script = os.path.join(frontend_dir, "run.py")
    
    # Get port from environment variable or use default
    port = os.getenv("FRONTEND_PORT", "8501")
    
    print(f"Starting frontend server on http://localhost:{port}...")
    print("Press Ctrl+C to stop the server")
    
    # Run the frontend server
    try:
        # Change to the frontend directory
        os.chdir(frontend_dir)
        
        # Run the frontend script
        subprocess.run([sys.executable, frontend_script])
    except KeyboardInterrupt:
        print("\nFrontend server stopped.")

if __name__ == "__main__":
    main()