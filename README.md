

# Personal Finance Chatbot (FinAC)

## Overview
This project is an intelligent conversational AI chatbot that provides personalized financial guidance using Google Gemini Flash for insights and IBM Granite for budget summaries. It features a FastAPI backend and a Streamlit frontend with a modern glassmorphism UI design, specifically tailored for Indian users' financial needs.

## Key Features

### 1. Personalized Financial Guidance
- **User Profile Management**: Create and manage financial profiles with income, expenses, city, and financial goals
- **Expense Tracking**: Track expenses across multiple categories (Housing, Food, Transportation, etc.)
- **Financial Goal Setting**: Set and track multiple financial goals

### 2. AI-Powered Insights
- **Google Gemini Integration**: Uses Gemini 1.5 Flash model for generating spending insights
- **Budget Summaries**: Generates comprehensive budget summaries using IBM Granite 2.5B
- **Investment Advice**: Provides personalized investment recommendations based on risk tolerance and goals

### 3. Tax Information
- **City-Based Tax Calculation**: Tax calculations based on city tier classification (Tier 1, 2, or 3)
- **Tax Regime Comparison**: Compares old vs. new tax regimes with visual graphs
- **HRA Exemption Calculator**: Calculates HRA exemptions based on city tier

### 4. Voice Capabilities
- **Speech Recognition**: Convert voice input to text for chatbot queries
- **Text-to-Speech**: Convert chatbot responses to voice output
- **Audio Downloads**: Download audio versions of financial summaries

### 5. Export & Sharing
- **PDF Generation**: Export financial summaries as PDF documents
- **Text Copying**: One-click copy functionality for summaries
- **Data Visualization**: Visual representation of tax information and expenses

## Technologies Used
- **Backend**: FastAPI, Python 3.10+
- **Frontend**: Streamlit with glassmorphism UI
- **AI Models**: Google Gemini 1.5 Flash, IBM Granite 2.5B
- **Voice**: SpeechRecognition, gTTS (Google Text-to-Speech)
- **Data Visualization**: Matplotlib, Seaborn
- **Document Generation**: ReportLab for PDF generation

## Getting Started

For detailed setup instructions, please refer to the [SETUP.md](SETUP.md) file.

### Quick Start

#### Using Scripts

**Windows:**
```
start_app.bat
```

**Linux/Mac:**
```
./start_app.sh
```

#### Manual Setup

1. Clone the repository
2. Set up a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Configure API keys in `.env` file
5. Run the application: `python run.py`

#### Docker

```
docker-compose up
```

## Development

### Running Components Separately

**Backend only:**
```
python run_backend.py
```

**Frontend only:**
```
python run_frontend.py
```

### Testing API Keys

```
python test_api_keys.py
```

### Checking Dependencies

```
python check_dependencies.py
```

## API Key Configuration
The project uses the following API keys (stored in the `.env` file):
```
GEMINI_API_KEY=your_gemini_api_key
HF_API_KEY=your_huggingface_api_key
```

## License

This project is licensed under the MIT License.

