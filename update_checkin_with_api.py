import re

def update_checkin_with_api():
    """Update check-in HTML to use API instead of localStorage"""
    
    # Read the current checkin.html
    with open('/Users/nahomnigatu/Downloads/campusministrybadges/web/checkin.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # JavaScript code to replace localStorage with API calls
    api_js_code = '''
        // API Configuration
        const API_BASE_URL = 'http://localhost:5000/api';
        let checkedInParticipants = new Set();
        
        // Load checked-in participants from API
        async function loadCheckedInParticipants() {
            try {
                const response = await fetch(`${API_BASE_URL}/checkin/all`);
                if (response.ok) {
                    const data = await response.json();
                    checkedInParticipants = new Set(data.checked_in_participants.map(p => p.name));
                    console.log(`Loaded ${checkedInParticipants.size} checked-in participants from server`);
                    updateStats();
                } else {
                    console.error('Failed to load check-in data from server');
                    // Fallback to localStorage
                    loadFromLocalStorage();
                }
            } catch (error) {
                console.error('Error connecting to server:', error);
                // Fallback to localStorage
                loadFromLocalStorage();
            }
        }
        
        // Fallback to localStorage if server is unavailable
        function loadFromLocalStorage() {
            const saved = localStorage.getItem('checkedInParticipants');
            if (saved) {
                checkedInParticipants = new Set(JSON.parse(saved));
                console.log(`Loaded ${checkedInParticipants.size} checked-in participants from localStorage`);
                updateStats();
            }
        }
        
        // Save to both API and localStorage
        async function saveCheckinToAPI(participantName) {
            try {
                const response = await fetch(`${API_BASE_URL}/checkin`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ name: participantName })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    console.log(`Successfully checked in ${participantName} to server`);
                    
                    // Also save to localStorage as backup
                    localStorage.setItem('checkedInParticipants', JSON.stringify([...checkedInParticipants]));
                    
                    return true;
                } else {
                    console.error('Failed to save check-in to server');
                    // Still save to localStorage
                    localStorage.setItem('checkedInParticipants', JSON.stringify([...checkedInParticipants]));
                    return false;
                }
            } catch (error) {
                console.error('Error connecting to server:', error);
                // Still save to localStorage
                localStorage.setItem('checkedInParticipants', JSON.stringify([...checkedInParticipants]));
                return false;
            }
        }
        
        // Periodic sync with server (every 10 seconds)
        function startPeriodicSync() {
            setInterval(async () => {
                await loadCheckedInParticipants();
            }, 10000); // Sync every 10 seconds
        }
        
        // Updated confirmCheckIn function
        async function confirmCheckIn() {
            if (!selectedPerson) return;
            
            // Add to checked-in set
            checkedInParticipants.add(selectedPerson.name);
            
            // Save to API and localStorage
            await saveCheckinToAPI(selectedPerson.name);
            
            // Show success message
            document.getElementById('personInfo').style.display = 'none';
            document.getElementById('successMessage').style.display = 'block';
            
            // Update stats
            updateStats();
            
            // Clear form after 3 seconds
            setTimeout(() => {
                clearForm();
            }, 3000);
        }
        
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadParticipants();
            loadCheckedInParticipants(); // Load from API instead of localStorage
            startPeriodicSync(); // Start periodic sync
        });
    '''
    
    # Replace the old localStorage code with API code
    # First, find and replace the confirmCheckIn function
    old_confirm_checkin = r'function confirmCheckIn\(\) \{[^}]*\}[^}]*\}[^}]*\}'
    
    # Replace the DOMContentLoaded event listener
    old_dom_content = r'document\.addEventListener\(\'DOMContentLoaded\', function\(\) \{[^}]*\}\);'
    
    # Replace the localStorage loading code
    old_load_participants = r'// Load checked-in participants from localStorage[^}]*\}'
    
    # Remove old functions and add new API-based ones
    html_content = re.sub(r'let checkedInParticipants = new Set\(\);', '', html_content)
    html_content = re.sub(r'function loadParticipants\(\) \{', api_js_code + '\\n\\n        function loadParticipants() {', html_content)
    
    # Replace the confirmCheckIn function
    html_content = re.sub(
        r'function confirmCheckIn\(\) \{[^}]*checkedInParticipants\.add[^}]*localStorage\.setItem[^}]*updateStats\(\);[^}]*setTimeout[^}]*clearForm\(\);[^}]*\}, 3000\);[^}]*\}',
        '',
        html_content,
        flags=re.DOTALL
    )
    
    # Replace the DOMContentLoaded listener
    html_content = re.sub(
        r'// Load checked-in participants from localStorage[^}]*localStorage\.getItem[^}]*\}[^}]*updateStats\(\);[^}]*loadParticipants\(\);',
        '',
        html_content,
        flags=re.DOTALL
    )
    
    # Write the updated HTML
    with open('/Users/nahomnigatu/Downloads/campusministrybadges/web/checkin.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Updated check-in HTML with API integration")
    print("🔄 Check-in system now uses central server instead of localStorage")
    print("📱 Universal check-in across all devices")
    print("🔄 Automatic sync every 10 seconds")
    print("💾 Fallback to localStorage if server is unavailable")

if __name__ == "__main__":
    update_checkin_with_api()