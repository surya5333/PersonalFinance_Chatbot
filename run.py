import os
import subprocess
import sys
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_backend():
    """Run the backend server"""
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
    backend_script = os.path.join(backend_dir, "main.py")
    
    print("Starting backend server...")
    
    # Run the backend server
    if os.name == "nt":  # Windows
        return subprocess.Popen([sys.executable, backend_script], cwd=backend_dir)
    else:  # Unix/Linux/Mac
        return subprocess.Popen([sys.executable, backend_script], cwd=backend_dir)

def run_frontend():
    """Run the frontend server"""
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
    frontend_script = os.path.join(frontend_dir, "run.py")
    
    print("Starting frontend server...")
    
    # Run the frontend server
    if os.name == "nt":  # Windows
        return subprocess.Popen([sys.executable, frontend_script], cwd=frontend_dir)
    else:  # Unix/Linux/Mac
        return subprocess.Popen([sys.executable, frontend_script], cwd=frontend_dir)

def main():
    """Main function to run both servers"""
    # Start the backend server
    backend_process = run_backend()
    
    # Wait for the backend to start
    print("Waiting for backend server to start...")
    time.sleep(5)
    
    # Start the frontend server
    frontend_process = run_frontend()
    
    # Get port information from environment variables
    backend_port = os.getenv("BACKEND_PORT", "8000")
    frontend_port = os.getenv("FRONTEND_PORT", "8501")
    
    # Print URLs
    print(f"\nBackend API running at: http://localhost:{backend_port}")
    print(f"Frontend running at: http://localhost:{frontend_port}")
    print("\nPress Ctrl+C to stop both servers\n")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping servers...")
        
        # Terminate processes
        backend_process.terminate()
        frontend_process.terminate()
        
        print("Servers stopped.")

if __name__ == "__main__":
    main()