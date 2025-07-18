// Alternative Firebase configurations to try if the main one fails

export const firebaseConfig = {
  apiKey: "AIzaSyAk7BBzX1FejPjW-d6QVz1G9T2E001RWeQ",
  authDomain: "campusministry-d8400.firebaseapp.com",
  databaseURL: "https://campusministry-d8400-default-rtdb.firebaseio.com/",
  projectId: "campusministry-d8400",
  storageBucket: "campusministry-d8400.appspot.com",
  messagingSenderId: "647659158955",
  appId: "1:647659158955:web:0dad448d9ad7ad7f6926ee"
};

// Alternative configurations to try if the main one fails
export const alternativeConfigs = [
  {
    ...firebaseConfig,
    databaseURL: "https://campusministry-d8400-default-rtdb.us-central1.firebasedatabase.app/"
  },
  {
    ...firebaseConfig,
    databaseURL: "https://campusministry-d8400-default-rtdb.europe-west1.firebasedatabase.app/"
  },
  {
    ...firebaseConfig,
    databaseURL: "https://campusministry-d8400-default-rtdb.asia-southeast1.firebasedatabase.app/"
  }
];

// Function to test database connectivity
export async function testDatabaseURL(config) {
  try {
    const response = await fetch(config.databaseURL + "/.json");
    return response.ok;
  } catch (error) {
    return false;
  }
}

// Function to find working configuration
export async function findWorkingConfig() {
  // Try main config first
  if (await testDatabaseURL(firebaseConfig)) {
    console.log("Main Firebase config is working");
    return firebaseConfig;
  }
  
  // Try alternatives
  for (const config of alternativeConfigs) {
    console.log("Trying alternative config:", config.databaseURL);
    if (await testDatabaseURL(config)) {
      console.log("Found working config:", config.databaseURL);
      return config;
    }
  }
  
  console.error("No working Firebase configuration found");
  return null;
}
