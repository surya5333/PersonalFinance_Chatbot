# Personal Finance Chatbot - Setup Guide

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd finac
```

### 2. Create and Activate a Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up API Keys

Create a `.env` file in the root directory with the following content:

```
# API Keys
GEMINI_API_KEY=your_gemini_api_key
HF_API_KEY=your_huggingface_api_key

# Backend Configuration
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000

# Frontend Configuration
FRONTEND_PORT=8501
```

Replace `your_gemini_api_key` and `your_huggingface_api_key` with your actual API keys.

- Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Get a Hugging Face API key from [Hugging Face](https://huggingface.co/settings/tokens)

### 5. Run the Application

**Option 1: Run both servers with a single command**

```bash
python run.py
```

**Option 2: Run servers separately**

In one terminal, start the backend:
```bash
cd backend
python main.py
```

In another terminal, start the frontend:
```bash
cd frontend
python run.py
```

### 6. Access the Application

- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Troubleshooting

### PyAudio Installation Issues

If you encounter issues installing PyAudio:

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-pyaudio
```

### API Key Issues

If you encounter errors related to API keys:

1. Verify that your `.env` file is in the correct location (root directory)
2. Check that your API keys are valid and have the necessary permissions
3. Restart the application after updating the `.env` file

### Port Conflicts

If you encounter port conflicts:

1. Edit the `.env` file to change the port numbers
2. Restart the application

## Additional Configuration

### Customizing Prompts

You can customize the AI prompts by editing the files in the `shared/prompts/` directory.

### Changing UI Theme

The UI uses a glassmorphism design with a blue gradient background. You can customize the appearance by editing the CSS in `frontend/app.py`.