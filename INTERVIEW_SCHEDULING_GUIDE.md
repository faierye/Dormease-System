# Interview Scheduling System - Implementation Guide

## 🎯 What Was Built

A complete interview scheduling and application management system for the DormEase dormitory management application.

## 📋 Implementation Summary

### 1. **Database Changes** (`database_migration.sql`)
Run the SQL migration to add these fields to your `applications_tb` table:
- `interview_status` - 'pending' or 'scheduled'
- `application_status` - 'pending', 'approved', or 'rejected'
- `interview_date` - Date of the interview
- `interview_time` - Time of the interview

**To execute the migration:**
```sql
-- Open MySQL and run the commands from database_migration.sql
```

### 2. **Backend Routes** (`app.py`)

#### `/applications` (GET)
- Lists all applications with filters (applicant_type, sex)
- Returns applications.html with icon states based on interview_status

#### `/application/<int:app_id>` (GET)
- Shows detailed applicant page
- Displays:
  - Full applicant information
  - Student/Employee specific details
  - Uploaded document/picture
  - Interview schedule (if scheduled)
  - Approve/Reject buttons

#### `/schedule_interview` (POST)
- Accepts JSON: `{application_id, interview_date, interview_time}`
- Updates interview_status to 'scheduled'
- Returns success response

#### `/update_application_status` (POST)
- Accepts JSON: `{application_id, status}`
- Updates application_status to 'approved' or 'rejected'
- Returns success response

### 3. **Frontend Changes**

#### `applications.html`
**Dynamic Icon Logic:**
- Shows **clock icon** (fi-rr-clock) if `interview_status == 'pending'`
- Shows **eye icon** (fi-rr-eye) if `interview_status == 'scheduled'`

**Click Behavior:**
- Clock icon → Opens scheduling modal
- Eye icon → Redirects to `/application/<id>`

**Updated Jinja Template:**
```html
<i class="fi {% if application.interview_status == 'scheduled' %}
    fi-rr-eye
{% else %}
    fi-rr-clock
{% endif %} action-btn"
   data-id="{{ application.application_id }}"
   data-interview-status="{{ application.interview_status|default('pending') }}">
</i>
```

#### `application_detail.html` (NEW)
Detailed applicant view page showing:
- Full name, contact, address
- Student/Employee specific info (program, year, department, etc.)
- Application timeline
- Interview schedule (date & time)
- Uploaded document/picture with download option
- Approve/Reject action buttons

#### `detail.css` (NEW)
Comprehensive styling for the detail page including:
- Responsive 2-column layout (info + actions)
- Status badges with color coding
- File preview for documents/images
- Sticky action buttons
- Mobile-responsive design

### 4. **JavaScript Logic**

**applications.html:**
```javascript
// Click Clock Icon → Open Modal (to schedule)
// Click Eye Icon → Redirect to detail page

// Save Interview Schedule
// - Validates date and time inputs
- Sends POST to /schedule_interview
- Reloads page to update icon to eye

// Approve/Reject Application
// - Sends POST to /update_application_status
// - Shows confirmation dialog
// - Reloads page
```

## 🚀 How to Use

### Step 1: Execute Database Migration
```bash
# Open your MySQL client and run:
source database_migration.sql
```

Or manually run the SQL commands from `database_migration.sql`

### Step 2: Test the Application

1. **Start Flask:**
   ```bash
   python app.py
   ```

2. **Go to Applications Page:**
   - Navigate to `/applications`
   - You should see clock icons for pending interviews

3. **Schedule an Interview:**
   - Click the **clock icon** on any applicant row
   - Fill in date and time
   - Click "Save"
   - The page will reload and the icon changes to an eye

4. **View Applicant Details:**
   - Click the **eye icon** to view the full detail page
   - See all applicant information
   - View uploaded documents
   - Approve or Reject the application

## 📊 Status System

### Interview Status
- `pending` → Clock icon (can schedule)
- `scheduled` → Eye icon (can view details)

### Application Status
- `pending` → Pending badge
- `approved` → Green badge ✓
- `rejected` → Red badge ✗

## 🎨 UI/UX Features

✅ **Dynamic Icons:** Clock changes to eye after scheduling
✅ **Modal Interface:** Easy scheduling without leaving the page
✅ **Detail Page:** Comprehensive applicant information
✅ **Action Buttons:** One-click approve/reject
✅ **File Preview:** Display uploaded images and documents
✅ **Responsive Design:** Works on desktop and mobile
✅ **Confirmation Dialogs:** Prevent accidental approvals/rejections
✅ **Status Badges:** Color-coded status indicators

## 🔧 Troubleshooting

**Icons not updating?**
- Make sure database migration was run
- Check that interview_status field exists in applications_tb

**Modal not opening?**
- Ensure JavaScript is loaded correctly
- Check browser console for errors

**Eye icon not redirecting?**
- Verify application_id is correctly passed in data attribute
- Check that /application/<id> route is accessible

**Approve/Reject buttons not working?**
- Ensure /update_application_status route is accessible
- Check network tab in browser developer tools

## 📁 File Structure

```
Dormease/
├── app.py (Updated with new routes)
├── database_migration.sql (New)
├── templates/
│   ├── applications.html (Updated)
│   └── application_detail.html (New)
└── static/css/
    ├── applications.css (Updated)
    └── detail.css (New)
```

## 💡 Future Enhancements

- Add email notifications for interview schedules
- Export applicant data to PDF
- Interview notes/comments section
- Bulk actions (approve multiple at once)
- Advanced filtering and search
- Applicant status history/timeline
