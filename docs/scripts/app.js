import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getDatabase, ref, push, onChildAdded } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-database.js";
import { firebaseConfig } from "./env.js";

const app = initializeApp(firebaseConfig);
const db = getDatabase(app);
const todayPath = new Date().toISOString().slice(0,10);          // 2025-07-18
const checkinsRef = path => ref(db, `checkins/${path}`);

function saveCheckin(name, campus) {
  push(checkinsRef(todayPath), { name, campus, ts: Date.now() });
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
    
    checkedInParticipants.add(selectedPerson.name);
    
    // Save to Firebase
    saveCheckin(selectedPerson.name, selectedPerson.campus);
    
    // Show success message
    document.getElementById('personInfo').style.display = 'none';
    document.getElementById('successMessage').style.display = 'block';
    
    updateStats();
    
    setTimeout(() => {
      clearForm();
    }, 3000);
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
  onChildAdded(checkinsRef(todayPath), snap => {
    const { name } = snap.val();
    checkedInParticipants.add(name);
    updateStats();
  });

  // Initialize
  loadParticipants();
}

// ========== admin.html code ==========
if (document.body.id === "adminPage") {
  onChildAdded(checkinsRef(todayPath), snap => {
    const checkinData = snap.val();
    
    // Call the global function defined in admin.html
    if (window.addCheckinToTable) {
      window.addCheckinToTable(checkinData);
    }
  });
}
