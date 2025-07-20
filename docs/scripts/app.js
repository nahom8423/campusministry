import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getDatabase, ref, push, onChildAdded } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-database.js";
import { firebaseConfig } from "./env.js";

// Utility function to get today's date in consistent format
function getTodayPath() {
  return new Date().toISOString().slice(0,10);
}

// Function to get Saturday's date (July 19)
function getSaturdayPath() {
  return "2025-07-19";
}

// Function to get the date path for admin panel (defaults to Saturday until archived)
function getAdminDatePath() {
  // Check if Saturday data has been archived
  const saturdayArchived = localStorage.getItem('saturdayArchive');
  if (saturdayArchived) {
    return getTodayPath(); // Use today's date if Saturday is archived
  } else {
    return getSaturdayPath(); // Use Saturday's date if not archived yet
  }
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
    ts: Date.now(),
    status: 'checked-in'
  }).then(() => {
    console.log("Check-in saved successfully:", name);
  }).catch(error => {
    console.error("Error saving check-in:", error);
    throw error;
  });
}

function saveCheckout(name, campus) {
  if (!db || !checkinsRef) {
    console.error("Firebase not initialized properly");
    return Promise.reject("Firebase not initialized");
  }
  
  return push(checkinsRef(getAdminDatePath()), { 
    name, 
    campus, 
    ts: Date.now(),
    status: 'checked-out'
  }).then(() => {
    console.log("Check-out saved successfully:", name);
  }).catch(error => {
    console.error("Error saving check-out:", error);
    throw error;
  });
}

// ========== index.html code ==========
if (document.body.id === "checkinPage") {
  // Initialize checkin page functionality
  let participants = window.participants || [];
  let participantStatus = new Map(); // Track participant status (checked-in, checked-out)
  let selectedPerson = null;

  // Load participants from embedded data
  function loadParticipants() {
    // Participants data is embedded in the HTML
    updateStats();
  }

  function updateStats() {
    const total = participants.length;
    let checkedInCount = 0;
    
    for (const [name, status] of participantStatus) {
      if (status === 'checked-in') {
        checkedInCount++;
      }
    }
    
    document.getElementById('totalCount').textContent = total;
    document.getElementById('checkedInCount').textContent = checkedInCount;
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
    
    const currentStatus = participantStatus.get(person.name) || 'not-checked-in';
    const isCheckedIn = currentStatus === 'checked-in';
    const isCheckedOut = currentStatus === 'checked-out';
    
    let statusBadge, statusColor, buttonText, buttonDisabled;
    
    if (isCheckedIn) {
      statusBadge = '<span class="icon-check">✓</span> Already Checked In';
      statusColor = '#28a745';
      buttonText = '✓ Already Checked In';
      buttonDisabled = true;
    } else if (isCheckedOut) {
      statusBadge = '<span class="icon-pending">🚪</span> Checked Out - Can Check In Again';
      statusColor = '#ffc107';
      buttonText = '✓ Check Me In Again';
      buttonDisabled = false;
    } else {
      statusBadge = '<span class="icon-pending">○</span> Not Checked In';
      statusColor = '#ffc107';
      buttonText = '✓ Yes, Check Me In';
      buttonDisabled = false;
    }
    
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
    checkInBtn.disabled = buttonDisabled;
    checkInBtn.textContent = buttonText;
  }

  window.confirmCheckIn = async function() {
    if (!selectedPerson) return;
    
    try {
      participantStatus.set(selectedPerson.name, 'checked-in');
      
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
      
      // Remove from status if save failed
      participantStatus.delete(selectedPerson.name);
      
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
      const data = snap.val();
      const status = data.status || 'checked-in'; // Default to checked-in for backward compatibility
      
      participantStatus.set(data.name, status);
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
  
  // Make checkout function available globally
  window.saveCheckout = saveCheckout;
  
  if (db && checkinsRef) {    
    onChildAdded(checkinsRef(getAdminDatePath()), snap => {
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
