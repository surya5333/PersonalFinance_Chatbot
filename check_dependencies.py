import importlib.util
import sys
import subprocess
import pkg_resources

def check_package(package_name):
    """Check if a package is installed"""
    try:
        pkg_resources.get_distribution(package_name)
        return True
    except pkg_resources.DistributionNotFound:
        return False

def main():
    """Check if all required dependencies are installed"""
    print("=== Checking Dependencies ===")
    
    # List of required packages
    required_packages = [
        # Backend
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "pydantic",
        "google-generativeai",
        "huggingface-hub",
        "requests",
        "python-multipart",
        
        # Frontend
        "streamlit",
        "matplotlib",
        "seaborn",
        "reportlab",
        
        # Voice capabilities
        "SpeechRecognition",
        "gTTS",
        "PyAudio",
        
        # Data handling
        "pandas",
        "numpy"
    ]
    
    # Check each package
    missing_packages = []
    for package in required_packages:
        if check_package(package):
            print(f"✅ {package} is installed")
        else:
            print(f"❌ {package} is NOT installed")
            missing_packages.append(package)
    
    # Summary
    print("\n=== Summary ===")
    if missing_packages:
        print(f"❌ {len(missing_packages)} package(s) are missing:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nTo install missing packages, run:")
        print(f"pip install {' '.join(missing_packages)}")
        return 1
    else:
        print("✅ All required packages are installed!")
        return 0

if __name__ == "__main__":
    sys.exit(main())