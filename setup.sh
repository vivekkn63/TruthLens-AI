#!/bin/bash
# Setup script for TruthLens AI on macOS/Linux

echo "🚀 TruthLens AI Setup Script"
echo "=============================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create .env file
echo ""
echo "⚙️  Setting up configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your API keys:"
    echo "   - OPENAI_API_KEY: Get from https://platform.openai.com/api-keys"
    echo "   - TAVILY_API_KEY: Get from https://tavily.com"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Edit .env and add your API keys"
echo "   2. Run: python main.py"
echo ""
