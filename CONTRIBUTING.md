# Contributing to FinAC

Thank you for your interest in contributing to FinAC! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with the following information:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment information (OS, browser, etc.)

### Suggesting Enhancements

We welcome suggestions for enhancements! Please create an issue with:

- A clear, descriptive title
- A detailed description of the proposed enhancement
- Any relevant examples or mockups

### Pull Requests

1. Fork the repository
2. Create a new branch from `main`
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Submit a pull request

#### Pull Request Guidelines

- Follow the existing code style
- Include tests for new functionality
- Update documentation as needed
- Keep pull requests focused on a single concern

## Development Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your API keys
6. Run the application: `python run.py`

## Project Structure

```
├── backend/            # FastAPI backend
│   ├── db/             # Database files
│   ├── routes/         # API routes
│   └── services/       # Service modules
├── frontend/           # Streamlit frontend
│   └── components/     # UI components
└── shared/             # Shared utilities
    └── prompts/        # AI prompt templates
```

## Testing

Before submitting a pull request, please run:

```
python check_dependencies.py  # Ensure all dependencies are installed
python test_api_keys.py       # Test API connectivity
```

## Documentation

Please update relevant documentation when making changes:

- README.md for general information
- SETUP.md for setup instructions
- Code comments for technical details

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.