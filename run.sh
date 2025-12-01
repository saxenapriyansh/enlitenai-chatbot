#!/bin/bash

# Medical Data Query System - Startup Script

echo "🏥 Starting Medical Data Query System..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  WARNING: .env file not found!"
    echo "Please create a .env file with your OpenAI API key:"
    echo "  OPENAI_API_KEY=your_key_here"
    echo ""
    echo "You can copy from env_template.txt:"
    echo "  cp env_template.txt .env"
    echo ""
    read -p "Press Enter to continue anyway or Ctrl+C to exit..."
fi

# Start Streamlit
echo ""
echo "🚀 Launching application..."
echo "📱 The app will open in your browser at http://localhost:8501"
echo ""
streamlit run app.py

