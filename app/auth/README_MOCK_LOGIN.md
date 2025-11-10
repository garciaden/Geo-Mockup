# Mock Login System (Development Only)

**Status**: Development/Testing Only
**Security**: ⚠️ **Remove before production deployment**

## Overview

This mockup includes a simple session-based authentication system for testing different user roles and permissions without requiring a real authentication backend (SSO/OIDC).

## Quick Start

### Option 1: Login Page
1. Navigate to: `http://localhost:5000/auth/login`
2. Select a role from the dropdown
3. (Optional) Enter a custom username
4. Click "Login"

### Option 2: Quick Login URLs (Faster for Development)
Direct login links for each role:

- **Administrator**: `http://localhost:5000/auth/quick-login/Administrator`
- **Project Owner**: `http://localhost:5000/auth/quick-login/Project_Owner`
- **Collaborator**: `http://localhost:5000/auth/quick-login/Collaborator`
- **View & Export**: `http://localhost:5000/auth/quick-login/View_Export`
- **View Only**: `http://localhost:5000/auth/quick-login/View_Only`

### Logout
Click your username in the navigation bar → "Logout" or visit: `http://localhost:5000/auth/logout`

---

## Role Permissions Matrix

| Permission             | Administrator | Project Owner | Collaborator | View & Export | View Only |
|------------------------|:-------------:|:-------------:|:------------:|:-------------:|:---------:|
| **Create Projects**    | ✅            | ✅            | ❌           | ❌            | ❌        |
| **Edit Samples**       | ✅            | ✅            | ✅           | ❌            | ❌        |
| **Manage Analysis**    | ✅            | ✅            | ✅           | ❌            | ❌        |
| **Flag Samples**       | ✅            | ✅            | ✅           | ❌            | ❌        |
| **Create Sub-samples** | ✅            | ✅            | ✅           | ❌            | ❌        |
| **Export Data**        | ✅            | ✅            | ❌           | ✅            | ❌        |

---

## Role Descriptions

### Administrator (Full Access)
- **Use Case**: System administrators, lab managers
- **Permissions**: Complete access to all features
- **Restrictions**: None

### Project Owner (Manage Projects)
- **Use Case**: Principal investigators, project leads
- **Permissions**: Create/manage projects, full sample/analysis access
- **Restrictions**: None for owned projects

### Collaborator (Edit Samples & Data)
- **Use Case**: Lab technicians, research assistants
- **Permissions**: Edit samples, manage analyses, create sub-samples
- **Restrictions**: Cannot create projects or export data

### View & Export (Read + Export)
- **Use Case**: External researchers, data analysts
- **Permissions**: View all data, export datasets
- **Restrictions**: Cannot edit samples or analyses

### View Only (Read Only)
- **Use Case**: Students, observers, auditors
- **Permissions**: View data only
- **Restrictions**: No editing, no exporting

---

## Implementation Details

### Session Storage
User data is stored in Flask's session object:
```python
session['user'] = {
    'username': 'Admin User',
    'email': 'admin@concord.edu',
    'role': 'Administrator',
    'can_create_projects': True,
    'can_edit_sample': True,
    'can_manage_analysis': True,
    'can_flag_samples': True,
    'can_create_subsample': True,
    'can_export_data': True
}
session['is_authenticated'] = True
```

### Permission Checks in Templates
```jinja2
{% if session.get('is_authenticated') %}
  {% set user = session.get('user', {}) %}
  {% if user.get('can_create_projects') %}
    <a href="{{ url_for('projects.project_create') }}">Create Project</a>
  {% endif %}
{% endif %}
```

### Permission Checks in Routes
```python
from flask import session

user = session.get('user', {})
if not user.get('can_edit_sample'):
    abort(403)  # Forbidden
```

### Combined Permission Checks
Permissions combine user role + sample status:
```python
# User has permission AND sample is not archived
can_edit = user.get('can_edit_sample') and sample['status'] != 'archived'
```

---

## Testing Different Roles

### Test Scenario: Create Project
1. **As View Only**: Login → No "Add Project" button visible ✅
2. **As Collaborator**: Login → No "Add Project" button visible ✅
3. **As Project Owner**: Login → "Add Project" button visible ✅

### Test Scenario: Edit Sample
1. **As View Only**: Login → No edit buttons on sample page ✅
2. **As View & Export**: Login → No edit buttons, "Export Data" visible ✅
3. **As Collaborator**: Login → Edit buttons visible ✅

### Test Scenario: Export Data
1. **As View Only**: Login → No export button ✅
2. **As Collaborator**: Login → No export button ✅
3. **As View & Export**: Login → Export button visible ✅

---

## Files Modified

### Core Authentication
- `app/auth/routes.py` - Login/logout routes, session management
- `app/auth/templates/auth/login.html` - Login page with role selector

### Navigation
- `app/templates/components/_header.html` - User dropdown, login/logout buttons

### Permission Integration
- `app/main/templates/main/index.html` - "Add Project" button visibility
- `app/samples/routes.py` - Combined user + sample status permissions

---

## Migration to Production Authentication

When ready to implement real authentication (SSO/OIDC):

1. **Keep**: Session storage structure (compatible with Flask-Login)
2. **Replace**: Mock login routes with SSO callback handlers
3. **Add**: User database table for persistent user data
4. **Update**: Permission checks to query database
5. **Remove**: `/quick-login/<role>` routes (development only)

See `future_enhancements/sso_implementation_plan.md` for detailed migration guide.

---

## Security Warnings

⚠️ **This is NOT production-ready authentication:**
- No password verification
- No protection against session hijacking
- No user database (sessions clear on server restart)
- No HTTPS enforcement
- No rate limiting

⚠️ **Before production deployment:**
- Remove all quick-login routes
- Remove mock login form
- Implement SSO/OIDC (see `future_enhancements/`)
- Add session security (HTTPS-only cookies, CSRF protection)
- Implement proper authorization checks

---

## Troubleshooting

### "Add Project" button not appearing after login
- Check: `session.get('is_authenticated')` returns `True`
- Check: `session.get('user', {}).get('can_create_projects')` returns `True`
- Solution: Re-login with Administrator or Project_Owner role

### Permissions not working after server restart
- **Cause**: Flask sessions are stored in cookies (limited data)
- **Solution**: Re-login after server restart
- **Future**: Move to database-backed sessions

### Edit buttons not appearing on sample page
- Check: User has `can_edit_sample` permission
- Check: Sample status is not "archived"
- Solution: Login as Collaborator/Owner/Admin AND sample must be active

---

## Additional Resources

- **Flask Session Documentation**: https://flask.palletsprojects.com/en/3.0.x/api/#sessions
- **Role-Based Access Control**: `requirements.md` (Section 4.2)
- **Future SSO Implementation**: `future_enhancements/sso_implementation_plan.md`
