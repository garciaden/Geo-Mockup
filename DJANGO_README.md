# Django Migration - Quick Start

This folder contains everything you need to migrate the KuehnLab Flask application to Django.

## 📚 Documentation

- **[DJANGO_MIGRATION_GUIDE.md](./DJANGO_MIGRATION_GUIDE.md)** - Comprehensive migration guide with code examples
- **[TODO.md](./TODO.md)** - Complete roadmap and task list

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
django_setup.bat
```

**Linux/Mac:**
```bash
chmod +x django_setup.sh
./django_setup.sh
```

This will:
- Create virtual environment
- Install Django and all dependencies
- Create Django project structure
- Set up apps (core, accounts, projects, samples, analyses, people, data_management)
- Create `.env` file for configuration

### Option 2: Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install django==5.0.1 psycopg2-binary python-dotenv django-extensions djangorestframework

# Create Django project
mkdir django_app
cd django_app
django-admin startproject kuehnlab .

# Create apps
mkdir apps
python manage.py startapp core apps/core
python manage.py startapp accounts apps/accounts
python manage.py startapp projects apps/projects
python manage.py startapp samples apps/samples
python manage.py startapp analyses apps/analyses
python manage.py startapp people apps/people
python manage.py startapp data_management apps/data_management
```

## 📋 Post-Setup Steps

After running the setup script:

### 1. Configure Settings

Update `django_app/kuehnlab/settings.py`:
- Add installed apps (see DJANGO_MIGRATION_GUIDE.md)
- Configure database (PostgreSQL)
- Set up static files
- Configure authentication

### 2. Create Models

Copy model code from DJANGO_MIGRATION_GUIDE.md:
- `apps/accounts/models.py` - User model (16 fields)
- `apps/projects/models.py` - Project, ProjectCollaborator, ProjectTransfer
- `apps/samples/models.py` - Sample, SampleDisbursement
- Continue with remaining 13 models

### 3. Run Migrations

```bash
cd django_app
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

Enter:
- Username: admin
- Email: admin@kuehnlab.edu
- Password: (your secure password)

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/admin

## 🗂️ Project Structure

After setup, your structure will be:

```
CULS-Mockup/
├── app/                          # Original Flask app (keep for reference)
├── django_app/                   # New Django application
│   ├── manage.py
│   ├── .env
│   ├── requirements.txt
│   ├── kuehnlab/                # Project configuration
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/                    # Django applications
│   │   ├── core/
│   │   ├── accounts/
│   │   ├── projects/
│   │   ├── samples/
│   │   ├── analyses/
│   │   ├── people/
│   │   └── data_management/
│   ├── templates/               # Base templates
│   ├── static/                  # Static files (CSS, JS, images)
│   └── media/                   # User uploads
├── DJANGO_MIGRATION_GUIDE.md   # Detailed guide
├── DJANGO_README.md            # This file
├── django_setup.sh             # Linux/Mac setup
└── django_setup.bat            # Windows setup
```

## 📊 Migration Checklist

Track your progress:

### Phase 1: Foundation
- [ ] Run setup script
- [ ] Configure `settings.py`
- [ ] Create all 20 models
- [ ] Run migrations
- [ ] Test Django admin

### Phase 2: Authentication
- [ ] Custom User model
- [ ] Login/logout views
- [ ] Permission system
- [ ] Role-based access

### Phase 3: Core Views
- [ ] Homepage/dashboard
- [ ] Project list/detail
- [ ] Sample list/detail
- [ ] CRUD operations

### Phase 4: Templates
- [ ] Base template
- [ ] Navigation component
- [ ] Project templates
- [ ] Sample templates

### Phase 5: Advanced Features
- [ ] Analysis workflows (18 branches)
- [ ] File uploads
- [ ] Export functionality
- [ ] Search and filtering

### Phase 6: Testing & Deployment
- [ ] Unit tests
- [ ] Integration tests
- [ ] Deploy to Lightsail
- [ ] Configure Gunicorn + Nginx

## 🎯 Key Differences (Flask → Django)

| Feature | Flask | Django |
|---------|-------|--------|
| **Routing** | `@bp.route('/projects')` | `path('projects/', views.ProjectListView)` |
| **Templates** | `url_for('projects.list')` | `{% url 'projects:list' %}` |
| **Authentication** | `session.get('user')` | `request.user` (built-in) |
| **Database** | SQLAlchemy (manual setup) | Django ORM (automatic) |
| **Admin** | Custom implementation | Auto-generated admin |
| **Forms** | Flask-WTF | Django Forms |
| **API** | Manual routes | Django REST Framework |

## 💡 Tips

1. **Keep Flask app running** - Don't delete it until Django is fully working
2. **Use Django admin** - It's powerful for testing models immediately
3. **Follow the guide** - DJANGO_MIGRATION_GUIDE.md has all code examples
4. **Test incrementally** - Migrate one app at a time
5. **Use version control** - Commit after each major milestone

## 🐛 Troubleshooting

### Import errors
```bash
# Make sure you're in the django_app directory
cd django_app
python manage.py runserver
```

### Database errors
```bash
# Check PostgreSQL is running
# Verify .env database credentials
# Run migrations again
python manage.py migrate
```

### Static files not loading
```bash
# Collect static files
python manage.py collectstatic
```

### Models not showing in admin
```python
# Register models in apps/*/admin.py
from django.contrib import admin
from .models import Project

admin.site.register(Project)
```

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Tutorial](https://docs.djangoproject.com/en/5.0/intro/tutorial01/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)

## 🤝 Need Help?

1. Check **DJANGO_MIGRATION_GUIDE.md** for detailed examples
2. Review **TODO.md** for the complete roadmap
3. Django documentation: https://docs.djangoproject.com/
4. Django community: https://forum.djangoproject.com/

---

**Last Updated**: 2025-11-13
**Status**: Ready for migration
**Next Step**: Run `django_setup.bat` (Windows) or `django_setup.sh` (Linux/Mac)
