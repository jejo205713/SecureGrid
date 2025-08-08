#!/bin/bash

echo "🔧 Starting SecureGrid Installation..."

# Check for python3
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 is not installed. Please install Python3 and rerun this script."
    exit 1
fi

# Check for pip
if ! command -v pip3 &> /dev/null
then
    echo "❌ pip3 is not installed. Please install pip3 and rerun this script."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "✅ Installation complete!"

echo ""
echo "💡 To activate your virtual environment, run:"
echo "    source venv/bin/activate"
echo ""
echo "▶️ To start SecureGrid, run:"
echo "    python main.py"
echo ""
echo "▶️ To run the demo simulation, run:"
echo "    python demo_simulation.py"
