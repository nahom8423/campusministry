# 🔧 Firebase Realtime Database Setup Guide

## ⚠️ Database Configuration Issue

If you're seeing this error:
```
Firebase error. Please ensure that you have the URL of your Firebase Realtime Database instance configured correctly.
```

This means the Firebase Realtime Database hasn't been created yet for your project.

## 🚀 Step-by-Step Setup

### 1. Go to Firebase Console
Visit: https://console.firebase.google.com/

### 2. Select Your Project
- Click on **campusministry-d8400** project

### 3. Create Realtime Database
1. In the left sidebar, click **"Realtime Database"**
2. Click **"Create Database"** button
3. Choose your database location:
   - **Recommended**: `us-central1` (Iowa)
   - Or choose the region closest to your users
4. Set security rules:
   - For testing: Choose **"Start in test mode"**
   - For production: Choose **"Start in locked mode"** and update rules later

### 4. Configure Security Rules (Important!)
Once created, go to the **"Rules"** tab and set:

```json
{
  "rules": {
    "checkins": {
      ".read": true,
      ".write": true
    }
  }
}
```

### 5. Update Database URL (if needed)
After creating the database, Firebase will show you the database URL. It should look like:
- `https://campusministry-d8400-default-rtdb.firebaseio.com/`
- OR `https://campusministry-d8400-default-rtdb.us-central1.firebasedatabase.app/`

If it's different, update the `docs/scripts/env.js` file.

## 🧪 Testing the Setup

1. Open the test page: http://localhost:8081/test-firebase.html
2. Click **"Check Database URL"** to verify connectivity
3. Click **"Test Firebase Connection"** to test read operations
4. Click **"Add Test Check-in"** to test write operations

## 🎯 Expected Results

After setup, you should see:
- ✅ Database URL is reachable
- ✅ Connection successful
- ✅ Test check-in added successfully

## 🔒 Security Considerations

### For Development/Testing:
```json
{
  "rules": {
    "checkins": {
      ".read": true,
      ".write": true
    }
  }
}
```

### For Production (more secure):
```json
{
  "rules": {
    "checkins": {
      ".read": true,
      ".write": "auth != null || root.child('admin_key').val() == 'your-secret-key'"
    }
  }
}
```

## 🌍 Database Regions

Common Firebase Realtime Database regions:
- **us-central1**: United States (Iowa)
- **europe-west1**: Europe (Belgium)  
- **asia-southeast1**: Asia (Singapore)

Choose the region closest to your users for best performance.

## ❓ Troubleshooting

### Error: "Database instance not found"
- Make sure you created the database in Firebase Console
- Check that the database URL in `env.js` matches what's shown in Console

### Error: "Permission denied"
- Check your security rules
- Make sure they allow read/write to the `checkins` path

### Error: "Network request failed"
- Check your internet connection
- Make sure the Firebase project is active
- Verify the project ID and database URL are correct

## 📞 Need Help?

If you're still having issues:
1. Check the browser console for detailed error messages
2. Verify your Firebase project settings
3. Try the test page to isolate the issue
4. Make sure all files are served over HTTP (not file://)

---
**Last Updated**: July 18, 2025
