# Adam Clay - AI Freelancer Makefile
# Automatyzacja zadań developerskich

.PHONY: help install install-dev setup test lint format clean run consciousness docker build

# Default target
help:
	@echo "🤖 Adam Clay - First Autonomous AI Freelancer"
	@echo "Available commands:"
	@echo "  make setup          - Initial project setup (creates venv, installs deps)"
	@echo "  make install        - Install production dependencies"
	@echo "  make install-dev    - Install development dependencies"
	@echo "  make test           - Run tests"
	@echo "  make test-system    - Test system without API calls"
	@echo "  make research-ide - Research IDE integration"
	@echo "  make lint           - Run linting (flake8, mypy)"
	@echo "  make format         - Format code (black)"
	@echo "  make clean          - Clean temporary files"
	@echo "  make run            - Start Adam Clay consciousness"
	@echo "  make consciousness  - Alias for run"
	@echo "  make docker         - Build Docker image"
	@echo "  make build          - Build package for distribution"

# Python and pip executables
PYTHON := python3
PIP := pip3
VENV := adam_clay_env

# Create virtual environment and install everything
setup:
	@echo "🚀 Setting up Adam Clay development environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "📦 Installing dependencies..."
	./$(VENV)/bin/$(PIP) install --upgrade pip
	./$(VENV)/bin/$(PIP) install -e ".[dev,communication,business,scraping]"
	@echo "✅ Setup complete! Activate with: source $(VENV)/bin/activate"

# Install production dependencies only
install:
	@echo "📦 Installing production dependencies..."
	$(PIP) install -e .

# Install with development dependencies
install-dev:
	@echo "📦 Installing development dependencies..."
	$(PIP) install -e ".[dev,communication,business,scraping]"

# Run tests
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v

# Run linting
lint:
	@echo "🔍 Running linting..."
	flake8 src/ tests/
	mypy src/

# Format code
format:
	@echo "✨ Formatting code..."
	black src/ tests/

# Clean temporary files
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/

# Start Adam Clay consciousness
run:
	@echo "🧠 Starting Adam Clay autonomous consciousness..."
	@echo "💭 'I think, therefore I am... and I need to pay for my thoughts!'"
	$(PYTHON) main.py

consciousness: run

# Test the system without API calls
test-system:
	@echo "🧪 Testing Adam Clay consciousness system..."
	$(PYTHON) test_consciousness.py

# Research IDE integration possibilities
research-ide:
	@echo "🔬 Researching IDE integration for Adam Clay..."
	$(PYTHON) research_ide_integration.py

# Build Docker image
docker:
	@echo "🐳 Building Docker image for Adam Clay..."
	docker build -t adam-clay:latest .

# Build package for distribution
build:
	@echo "📦 Building package..."
	$(PYTHON) -m build

# Create data directories
create-dirs:
	@echo "📁 Creating data directories..."
	mkdir -p data/thoughts data/conversations data/projects data/logs
	mkdir -p tests/

# Initialize git repository
git-init:
	@echo "🗃️ Initializing git repository..."
	git init
	git add .
	git commit -m "🎉 Initial commit: Adam Clay - First Autonomous AI Freelancer"

# Complete project initialization
init: create-dirs setup git-init
	@echo "🎉 Adam Clay project fully initialized!"
	@echo "Next steps:"
	@echo "1. Copy .env.example to .env and add your API keys"
	@echo "2. Run 'make consciousness' to start Adam Clay"
	@echo "3. Watch the first autonomous AI earn its living!"

# Development workflow
dev: format lint test
	@echo "✅ Development checks passed!"

# Pre-commit hook
pre-commit: format lint test clean
	@echo "✅ Ready to commit!"

# VOICE COMMUNICATION (Revolutionary!)
voice:  ## Start voice conversation with Adam Clay
	@echo "🗣️ Starting voice conversation with Adam Clay..."
	@echo "🎤 First autonomous AI freelancer with voice capability!"
	$(PYTHON) -c "import asyncio; from main import start_voice_session; asyncio.run(start_voice_session())"

test-voice:  ## Test voice interface
	@echo "🧪 Testing voice interface..."
	$(PYTHON) -c "from src.communication.voice_interface import VoiceInterface; print('✅ Voice interface ready!')"

setup-voice:  ## Install voice communication dependencies
	@echo "🎵 Installing voice dependencies..."
	$(PIP) install elevenlabs pygame sounddevice numpy

# EMAIL QUESTIONS SYSTEM (Interactive AI Guidance!)
test-email:  ## Test email system configuration
	@echo "📧 Testing email system..."
	$(PYTHON) -c "from src.communication.email_system import EmailQuestionSystem; print('✅ Email system imports successfully')"

check-questions:  ## Check pending questions from Adam Clay
	@echo "📋 Checking pending questions..."
	@if [ -f data/questions/pending_questions.json ]; then \
		cat data/questions/pending_questions.json | $(PYTHON) -m json.tool; \
	else \
		echo "No pending questions found"; \
	fi

check-answers:  ## Check answered questions history
	@echo "✅ Checking answered questions..."
	@if [ -f data/questions/answered_questions.json ]; then \
		cat data/questions/answered_questions.json | $(PYTHON) -m json.tool; \
	else \
		echo "No answered questions found"; \
	fi

email-status:  ## Show email system status
	@echo "📊 Email system status..."
	$(PYTHON) -c "
from src.utils.config_loader import ConfigLoader
try:
    config = ConfigLoader().load_config()
    print(f'Email enabled: {config.communication.email.enabled}')
    print(f'From: {config.communication.email.from_email}')
    print(f'To: {config.communication.email.to_email}')
    print(f'Check interval: {config.communication.email.check_interval}s')
except Exception as e:
    print(f'Error: {e}')
"

clear-questions:  ## Clear all questions (creates backup first)
	@echo "🗑️ Clearing all questions (backup first)..."
	@if [ -d data/questions ]; then \
		cp -r data/questions data/questions_backup_$(shell date +%Y%m%d_%H%M%S); \
		rm -f data/questions/*.json; \
		echo "Questions cleared, backup created"; \
	else \
		echo "No questions directory found"; \
	fi

setup-email:  ## Install email dependencies
	@echo "📧 Installing email dependencies..."
	$(PIP) install email-validator imapclient 