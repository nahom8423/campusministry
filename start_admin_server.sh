#!/bin/bash

echo "🚀 Starting Campus Ministry Admin Server..."
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Install required packages
echo "📦 Installing required packages..."
pip3 install -r requirements.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies. Please check your Python installation."
    exit 1
fi

echo ""
echo "🎯 Starting the admin server..."
echo "The admin panel will be available at: http://localhost:5000"
echo ""
echo "📋 Available Features:"
echo "   • Check-in/Check-out participants"
echo "   • Add new participants with automatic table/discussion assignments"
echo "   • Export data to CSV and Excel"
echo "   • Live participant statistics"
echo "   • Search and filter participants"
echo ""
echo "🔐 Default admin password: campus2024"
echo ""
echo "⚠️  To stop the server, press Ctrl+C"
echo "================================"
echo ""

# Start the server
python3 admin_server.py