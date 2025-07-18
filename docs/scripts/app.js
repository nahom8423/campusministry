import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getDatabase, ref, push, onChildAdded } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-database.js";
import { firebaseConfig } from "./env.js";

// Utility function to get today's date in consistent format
function getTodayPath() {
  return new Date().toISOString().slice(0,10);
}

// Initialize Firebase
let app, db, checkinsRef;

try {
  app = initializeApp(firebaseConfig);
  console.log("Firebase app initialized successfully");
  
  // Try to initialize database with better error handling
  try {
    db = getDatabase(app);
    console.log("Firebase database initialized successfully");
    checkinsRef = path => ref(db, `checkins/${path || getTodayPath()}`);
    console.log("Firebase initialized successfully for date:", getTodayPath());
  } catch (dbError) {
    console.error("Firebase Database initialization error:", dbError);
    console.error("Make sure Firebase Realtime Database is enabled in your Firebase console");
    
    // Show user-friendly error
    if (typeof window !== 'undefined' && window.showAdminError) {
      window.showAdminError("Database connection failed. Please check Firebase configuration.");
    }
  }
} catch (error) {
  console.error("Firebase app initialization error:", error);
}

function saveCheckin(name, campus) {
  if (!db || !checkinsRef) {
    console.error("Firebase not initialized properly");
    return Promise.reject("Firebase not initialized");
  }
  
  return push(checkinsRef(getTodayPath()), { 
    name, 
    campus, 
    ts: Date.now() 
  }).then(() => {
    console.log("Check-in saved successfully:", name);
  }).catch(error => {
    console.error("Error saving check-in:", error);
    throw error;
  });
}

// ========== index.html code ==========
if (document.body.id === "checkinPage") {
  // Initialize checkin page functionality
  let participants = window.participants || [];
  let checkedInParticipants = new Set();
  let selectedPerson = null;

  // Load participants from embedded data
  function loadParticipants() {
    // Participants data is embedded in the HTML
    updateStats();
  }

  function updateStats() {
    document.getElementById('totalCount').textContent = participants.length;
    document.getElementById('checkedInCount').textContent = checkedInParticipants.size;
  }

  function filterParticipants(searchText) {
    if (!searchText || searchText.length < 2) {
      return [];
    }
    
    const text = searchText.toLowerCase();
    return participants.filter(person => 
      person.name.toLowerCase().includes(text)
    ).slice(0, 10);
  }

  function showSuggestions(matches) {
    const suggestionsDiv = document.getElementById('suggestions');
    
    if (matches.length === 0) {
      suggestionsDiv.style.display = 'none';
      return;
    }
    
    suggestionsDiv.innerHTML = matches.map(person => `
      <div class="suggestion-item" onclick="selectPerson('${person.name}')">
        <strong>${person.name}</strong><br>
        <small>${person.campus} • ${person.dorm}</small>
      </div>
    `).join('');
    
    suggestionsDiv.style.display = 'block';
  }

  window.selectPerson = function(name) {
    selectedPerson = participants.find(p => p.name === name);
    document.getElementById('nameSearch').value = name;
    document.getElementById('suggestions').style.display = 'none';
    showPersonInfo(selectedPerson);
  }

  function showPersonInfo(person) {
    const personInfo = document.getElementById('personInfo');
    const personDetails = document.getElementById('personDetails');
    
    const isCheckedIn = checkedInParticipants.has(person.name);
    const statusBadge = isCheckedIn ? '<span class="icon-check">✓</span> Already Checked In' : '<span class="icon-pending">○</span> Not Checked In';
    const statusColor = isCheckedIn ? '#28a745' : '#ffc107';
    
    personDetails.innerHTML = `
      <p><strong>Name:</strong> ${person.name}</p>
      <p><strong>Campus Ministry:</strong> ${person.campus}</p>
      <p><strong>Dorm:</strong> ${person.dorm}</p>
      <p><strong>Table Assignment:</strong> ${person.table}</p>
      <p><strong>Discussion Group:</strong> ${person.discussion}</p>
      <p style="color: ${statusColor}; font-weight: bold;"><strong>Status:</strong> ${statusBadge}</p>
    `;
    
    personInfo.style.display = 'block';
    
    const checkInBtn = personInfo.querySelector('button');
    checkInBtn.disabled = isCheckedIn;
    checkInBtn.textContent = isCheckedIn ? '✓ Already Checked In' : '✓ Yes, Check Me In';
  }

  window.confirmCheckIn = async function() {
    if (!selectedPerson) return;
    
    try {
      checkedInParticipants.add(selectedPerson.name);
      
      // Save to Firebase
      await saveCheckin(selectedPerson.name, selectedPerson.campus);
      
      // Show success message
      document.getElementById('personInfo').style.display = 'none';
      document.getElementById('successMessage').style.display = 'block';
      
      updateStats();
      
      setTimeout(() => {
        clearForm();
      }, 3000);
    } catch (error) {
      console.error("Error during check-in:", error);
      
      // Remove from checked in set if save failed
      checkedInParticipants.delete(selectedPerson.name);
      
      // Show error message
      document.getElementById('errorMessage').style.display = 'block';
      
      setTimeout(() => {
        document.getElementById('errorMessage').style.display = 'none';
      }, 5000);
    }
  }

  window.clearSelection = function() {
    document.getElementById('personInfo').style.display = 'none';
    selectedPerson = null;
  }

  window.clearForm = function() {
    document.getElementById('nameSearch').value = '';
    document.getElementById('suggestions').style.display = 'none';
    document.getElementById('personInfo').style.display = 'none';
    document.getElementById('successMessage').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';
    selectedPerson = null;
  }

  // Event listeners
  document.getElementById('nameSearch').addEventListener('input', function(e) {
    const searchText = e.target.value;
    const matches = filterParticipants(searchText);
    showSuggestions(matches);
    
    if (!searchText) {
      clearSelection();
    }
  });

  document.addEventListener('click', function(e) {
    if (!e.target.closest('.search-container')) {
      document.getElementById('suggestions').style.display = 'none';
    }
  });

  // Load existing check-ins
  if (db && checkinsRef) {
    onChildAdded(checkinsRef(getTodayPath()), snap => {
      const { name } = snap.val();
      checkedInParticipants.add(name);
      updateStats();
    }, error => {
      console.error("Error loading check-ins:", error);
    });
  }

  // Initialize
  loadParticipants();
}

// ========== admin.html code ==========
if (document.body.id === "adminPage") {
  let isInitialLoad = true;
  let initialCheckinsCount = 0;
  
  if (db && checkinsRef) {    
    onChildAdded(checkinsRef(getTodayPath()), snap => {
      const checkinData = snap.val();
      
      if (isInitialLoad) {
        // Count existing check-ins during initial load
        initialCheckinsCount++;
      }
      
      // Call the global function defined in admin.html
      if (window.addCheckinToTable) {
        window.addCheckinToTable(checkinData, isInitialLoad);
      }
    }, error => {
      console.error("Error loading admin check-ins:", error);
      if (window.showAdminError) {
        window.showAdminError("Failed to load check-ins: " + error.message);
      }
    });
    
    // After a short delay, mark initial load as complete and update stats
    setTimeout(() => {
      isInitialLoad = false;
      if (window.initializeAdminStats) {
        window.initializeAdminStats(initialCheckinsCount);
      }
    }, 1000);
  } else {
    console.error("Firebase not initialized for admin panel");
    if (window.showAdminError) {
      window.showAdminError("Firebase connection failed");
    }
  }
}
