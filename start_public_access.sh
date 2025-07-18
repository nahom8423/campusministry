#!/bin/bash

# Campus Ministry Check-In System - Public Access Setup
# This script makes your check-in system accessible from ANY WiFi/cellular connection

echo "🎉 Setting up UNIVERSAL ACCESS for Campus Ministry Check-In System"
echo "=================================================="

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok is not installed. Please install it first:"
    echo "   brew install ngrok/ngrok/ngrok"
    exit 1
fi

# Check if admin_server.py is running
if ! pgrep -f "admin_server.py" > /dev/null; then
    echo "🚀 Starting admin server..."
    python3 admin_server.py &
    SERVER_PID=$!
    sleep 3
    echo "   Admin server started (PID: $SERVER_PID)"
else
    echo "✅ Admin server is already running"
fi

# Start ngrok tunnel
echo "🌐 Creating public tunnel..."
ngrok http 5001 &
NGROK_PID=$!

# Wait for ngrok to establish connection
sleep 5

# Get the public URL
PUBLIC_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for tunnel in data['tunnels']:
        if tunnel['proto'] == 'https':
            print(tunnel['public_url'])
            break
except:
    print('Error getting URL')
")

if [ "$PUBLIC_URL" = "Error getting URL" ] || [ -z "$PUBLIC_URL" ]; then
    echo "❌ Failed to get public URL. Please check ngrok setup."
    exit 1
fi

echo ""
echo "🎉 SUCCESS! Your check-in system is now PUBLICLY accessible!"
echo "=================================================="
echo ""
echo "📱 ATTENDEE CHECK-IN:"
echo "   URL: $PUBLIC_URL"
echo "   QR Code: Create QR code with this URL"
echo ""
echo "🔧 ADMIN PANEL:"
echo "   URL: $PUBLIC_URL/docs/admin.html"
echo "   Password: campus2024"
echo ""
echo "✅ HOW ATTENDEES USE IT:"
echo "   1. Scan QR code with phone camera (any phone, any carrier)"
echo "   2. Opens check-in page in their browser"
echo "   3. Search their name and tap to check in"
echo "   4. Works with their own cellular data or any WiFi!"
echo ""
echo "📊 REAL-TIME FEATURES:"
echo "   ✅ Check-ins sync across ALL devices instantly"
echo "   ✅ No app downloads required"
echo "   ✅ Works on ANY smartphone"
echo "   ✅ Live attendance count"
echo ""
echo "🔒 SECURITY:"
echo "   - All connections are HTTPS encrypted"
echo "   - Admin panel requires password"
echo "   - Session expires automatically"
echo ""
echo "To stop the service:"
echo "   1. Press Ctrl+C in this terminal"
echo "   2. Or run: pkill -f ngrok && pkill -f admin_server.py"
echo ""
echo "Keep this terminal open during your event!"
echo "=================================================="

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🔄 Stopping services..."
    pkill -f ngrok
    pkill -f admin_server.py
    echo "✅ Services stopped"
    exit 0
}

# Trap Ctrl+C and cleanup
trap cleanup INT

# Keep the script running
echo "Press Ctrl+C to stop..."
while true; do
    sleep 1
done
