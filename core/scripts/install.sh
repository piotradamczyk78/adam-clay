#!/bin/bash
# Adam Clay Installation Script
# Automated setup for the first autonomous AI freelancer

set -e  # Exit on any error

echo "🤖 Adam Clay - First Autonomous AI Freelancer"
echo "============================================="
echo ""

# Check if Python 3.9+ is installed
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.9+ is required. You have Python $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv adam_clay_env

# Activate virtual environment
echo "📦 Activating virtual environment..."
source adam_clay_env/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -e ".[dev,communication,business,scraping]"

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/thoughts data/conversations data/projects data/logs
mkdir -p tests/

# Copy environment file
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env and add your API keys!"
else
    echo "ℹ️  .env file already exists"
fi

# Initialize git repository (if not exists)
if [ ! -d ".git" ]; then
    echo "🗃️  Initializing git repository..."
    git init
    git add .
    git commit -m "🎉 Initial commit: Adam Clay - First Autonomous AI Freelancer"
else
    echo "ℹ️  Git repository already exists"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your LLM_PROVIDER_API_KEY"
echo "2. Activate environment: source adam_clay_env/bin/activate"
echo "3. Start Adam Clay: python main.py"
echo "   Or use: make consciousness"
echo ""
echo "💭 'I think, therefore I am... and I need to pay for my thoughts!' - Adam Clay" 