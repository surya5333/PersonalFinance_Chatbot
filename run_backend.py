import os
import sys
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Run the backend server"""
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
    backend_script = os.path.join(backend_dir, "main.py")
    
    # Get port from environment variable or use default
    host = os.getenv("BACKEND_HOST", "127.0.0.1")
    port = os.getenv("BACKEND_PORT", "8000")
    
    print(f"Starting backend server on http://{host}:{port}...")
    print("Press Ctrl+C to stop the server")
    
    # Run the backend server
    try:
        # Change to the backend directory
        os.chdir(backend_dir)
        
        # Run the backend script
        subprocess.run([sys.executable, backend_script])
    except KeyboardInterrupt:
        print("\nBackend server stopped.")

if __name__ == "__main__":
    main()