# Campus Ministry Admin Panel - Enhanced Features

## 🚀 New Features Added

### 1. **Add New Participants**
- **Live Form**: Add participants directly from the admin panel
- **Auto-Assignment**: Automatically assigns table and discussion groups
- **Smart Balancing**: Distributes participants evenly across tables/discussions
- **Real-time Updates**: New participants appear immediately in the table
- **Excel Integration**: Updates both CSV and Excel files simultaneously

### 2. **Enhanced Export Features**
- **Excel Export**: Export complete participant data to Excel format
- **CSV Export**: Export checked-in participants or all data
- **Timestamped Files**: All exports include date/time stamps
- **Formatted Data**: Excel exports match the original Excel structure

### 3. **Live Data Management**
- **API Integration**: Backend API handles all data operations
- **Real-time Updates**: Data refreshes automatically every 30 seconds
- **Persistent Storage**: Check-in data stored locally with backup
- **Error Handling**: Graceful fallback when server is unavailable

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip3 package manager

### Quick Start
1. **Start the Admin Server**:
   ```bash
   ./start_admin_server.sh
   ```

2. **Access the Admin Panel**:
   - Open your browser to: `http://localhost:5000`
   - Login with password: `campus2024`

### Manual Setup
If you prefer to set up manually:

1. **Install Dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Start the Server**:
   ```bash
   python3 admin_server.py
   ```

## 📋 How to Use

### Adding New Participants
1. **Navigate to "Add New Participant" section**
2. **Fill in required fields**:
   - Full Name (required)
   - Campus Ministry (dropdown selection)
   - Dorm/Room (required)
   - Role (Participant/Coordinator/Staff)
3. **Click "Add Participant"**
4. **System automatically assigns**:
   - Table assignment (balanced distribution)
   - Discussion group (balanced distribution)
   - Slide/slot for badge generation

### Exporting Data
- **Export Checked In**: Download CSV of only checked-in participants
- **Export All Data**: Download CSV of all participants with check-in status
- **Export Excel**: Download Excel file with all current participant data

### Managing Participants
- **Search**: Use the search box to find participants by name, campus, dorm, or table
- **Filter**: Filter by check-in status or campus ministry
- **Sort**: Click column headers to sort data
- **Check In/Out**: Use action buttons to manage attendance
- **View Details**: Click "Details" to see full participant information

## 🔧 Technical Details

### API Endpoints
- `GET /api/participants` - Get all participants
- `POST /api/participants` - Add new participant
- `GET /api/export/excel` - Export to Excel
- `GET /api/stats` - Get participant statistics

### File Updates
When adding new participants, the system updates:
- `/input_data/badge_assignments.csv` - Main participant database
- `/input_data/BADGE (CLEAN FILE).xlsx` - Excel source file

### Assignment Logic
- **Tables**: Automatically assigns to table with fewest participants (Tables 1-35)
- **Discussions**: Assigns to discussion group with fewest participants (DE 1-35, DA 1-9)
- **Slides**: Creates new badge slides as needed (4 participants per slide)

## 🔐 Security

### Authentication
- Password-protected admin panel
- Default password: `campus2024`
- Session-based authentication

### Data Security
- Local file storage only
- No external data transmission
- Check-in data stored in browser localStorage

## 🎯 Advanced Features

### Auto-Refresh
- Panel refreshes every 30 seconds
- Live updates of participant status
- Maintains local check-in state

### Responsive Design
- Mobile-friendly interface
- Professional styling with MK branding
- Accessible on tablets and phones

### Error Handling
- Graceful degradation when server is unavailable
- Fallback to static data if API fails
- Clear error messages for user actions

## 📊 Statistics Dashboard

The admin panel provides real-time statistics:
- Total participants count
- Check-in status breakdown
- Campus ministry distribution
- Table/discussion usage statistics

## 🔄 Integration with Existing System

### Badge Generation
- New participants automatically included in badge generation
- Preserves existing slide/slot assignments
- Maintains proper formatting and layout

### Check-in System
- New participants appear in check-in interface
- Maintains all existing functionality
- Seamless integration with current workflow

## 🆘 Troubleshooting

### Common Issues

1. **Server won't start**:
   - Check Python installation: `python3 --version`
   - Install dependencies: `pip3 install -r requirements.txt`
   - Check port availability: `lsof -i :5000`

2. **Can't add participants**:
   - Ensure server is running
   - Check browser console for errors
   - Verify all required fields are filled

3. **Excel export fails**:
   - Ensure admin server is running
   - Check file permissions in output folder
   - Verify Excel files are not open in another program

### Support
For additional support or questions about the new features, check:
- Server logs in terminal
- Browser developer console
- File system permissions

## 📈 Future Enhancements

Potential future improvements:
- Bulk participant import
- Advanced filtering options
- Email notifications
- Custom table/discussion assignments
- Integration with external databases

---

**Note**: This enhanced admin panel maintains full backward compatibility with the existing system while adding powerful new participant management capabilities.