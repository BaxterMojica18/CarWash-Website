# User Profile Feature

## Overview
Added comprehensive user profile management with dropdown menu and edit functionality.

## Features Implemented

### 1. Profile Dropdown Menu
Located in top-right corner of dashboard header:
- **Profile Icon**: Circular photo (40x40px)
- **Click to Open**: Shows dropdown menu
- **Menu Items**:
  - Profile info (photo, name, role)
  - ✏️ Edit Profile
  - ⚙️ Settings
  - 🚪 Logout

### 2. Edit Profile Modal
Accessible from dropdown menu:
- **Name Field**: Edit user's display name
- **Role Field**: Edit user's role/title
- **Photo Upload**: Upload profile picture with preview
- **Save Button**: Saves changes to localStorage and database

### 3. Dashboard Filter Repositioned
- Moved below "Dashboard" title
- Above stats cards (Total Revenue, etc.)
- Label: "Filter by:"
- Options: Weekly, Bi-Weekly, Monthly, Quarterly, Semi-Annually, Annually

### 4. Database Schema
New `user_profiles` table:
```sql
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id),
    name VARCHAR,
    role VARCHAR,
    photo VARCHAR
);
```

## Migration Required

Run this command to create the user_profiles table:
```bash
python add_user_profiles.py
```

## API Endpoints

### Get User Profile
```
GET /api/settings/profile
```
Returns current user's profile information.

### Save User Profile
```
POST /api/settings/profile
Body: {
    "name": "John Doe",
    "role": "Administrator",
    "photo": "base64_encoded_image"
}
```
Saves or updates user profile.

## Frontend Implementation

### Profile Data Storage
- Stored in localStorage for quick access
- Synced with backend database
- Keys: `profileName`, `profileRole`, `profilePhoto`

### Profile Photo Handling
- Accepts image files (jpg, png, etc.)
- Converts to base64 for storage
- Displays in circular format
- Default: Blue background if no photo

### Menu Behavior
- Opens on profile icon click
- Closes when clicking outside
- Closes when selecting an option
- Smooth transitions

## Styling

### Profile Icon
- 40x40px circular image
- Cursor pointer on hover
- Default blue background (#667eea)

### Dropdown Menu
- White background
- Rounded corners (8px)
- Box shadow for depth
- Min width: 220px
- Positioned absolute (top-right)

### Menu Items
- Hover effect (light gray background)
- Icons for visual clarity
- Smooth transitions
- Proper spacing

## Files Modified

### Backend
- `app/database.py` - Added UserProfile model
- `app/schemas.py` - Added UserProfile schemas
- `app/crud.py` - Added profile CRUD functions
- `app/routers/settings.py` - Added profile endpoints
- `add_user_profiles.py` - Migration script

### Frontend
- `frontend/dashboard.html` - Added profile dropdown and edit modal
- `frontend/js/dashboard.js` - Added profile management functions
- `frontend/css/style.css` - Added profile dropdown styling

## Usage

### Viewing Profile
1. Click profile icon in top-right corner
2. View name and role in dropdown

### Editing Profile
1. Click profile icon
2. Select "✏️ Edit Profile"
3. Update name, role, or photo
4. Click "Save Profile"
5. Changes reflect immediately

### Changing Photo
1. Open Edit Profile
2. Click "Choose File" under Profile Photo
3. Select image file
4. Preview appears
5. Click Save to apply

## Default Values
- Name: "Demo User" or user's email
- Role: "Admin" or "Demo User"
- Photo: None (blue background)

## Future Enhancements
- Email change functionality
- Password change
- Two-factor authentication
- Profile visibility settings
- Custom role permissions
