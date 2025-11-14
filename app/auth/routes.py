from flask import render_template, redirect, url_for, session, flash, request

from app.auth import bp


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Mock login page for development - supports all 5 roles"""
    if request.method == 'POST':
        role = request.form.get('role')
        username = request.form.get('username', 'Test User')

        # Mock user data for each role
        user_data = {
            'Administrator': {
                'username': username or 'Admin User',
                'email': 'admin@university.edu',
                'role': 'Administrator',
                'can_create_projects': True,
                'can_edit_sample': True,
                'can_manage_analysis': True,
                'can_flag_samples': True,
                'can_create_subsample': True,
                'can_export_data': True
            },
            'Project_Owner': {
                'username': username or 'Project Owner',
                'email': 'owner@university.edu',
                'role': 'Project_Owner',
                'can_create_projects': True,
                'can_edit_sample': True,
                'can_manage_analysis': True,
                'can_flag_samples': True,
                'can_create_subsample': True,
                'can_export_data': True
            },
            'Collaborator': {
                'username': username or 'Collaborator',
                'email': 'collaborator@university.edu',
                'role': 'Collaborator',
                'can_create_projects': False,
                'can_edit_sample': True,
                'can_manage_analysis': True,
                'can_flag_samples': True,
                'can_create_subsample': True,
                'can_export_data': False
            },
            'View_Export': {
                'username': username or 'View Export User',
                'email': 'viewer@university.edu',
                'role': 'View_Export',
                'can_create_projects': False,
                'can_edit_sample': False,
                'can_manage_analysis': False,
                'can_flag_samples': False,
                'can_create_subsample': False,
                'can_export_data': True
            },
            'View_Only': {
                'username': username or 'View Only User',
                'email': 'readonly@university.edu',
                'role': 'View_Only',
                'can_create_projects': False,
                'can_edit_sample': False,
                'can_manage_analysis': False,
                'can_flag_samples': False,
                'can_create_subsample': False,
                'can_export_data': False
            }
        }

        if role in user_data:
            # Store user data in session
            session['user'] = user_data[role]
            session['is_authenticated'] = True
            flash(f'Logged in as {user_data[role]["username"]} ({role})', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid role selected', 'error')

    return render_template('auth/login.html', title='Login')


@bp.route('/logout')
def logout():
    """Clear session and log out"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))


@bp.route('/quick-login/<role>')
def quick_login(role):
    """Quick login for development - URL-based role selection"""
    user_data = {
        'Administrator': {
            'username': 'Admin User',
            'email': 'admin@kuehnlab.edu',
            'role': 'Administrator',
            'can_create_projects': True,
            'can_edit_sample': True,
            'can_manage_analysis': True,
            'can_flag_samples': True,
            'can_create_subsample': True,
            'can_export_data': True
        },
        'Project_Owner': {
            'username': 'Project Owner',
            'email': 'owner@kuehnlab.edu',
            'role': 'Project_Owner',
            'can_create_projects': True,
            'can_edit_sample': True,
            'can_manage_analysis': True,
            'can_flag_samples': True,
            'can_create_subsample': True,
            'can_export_data': True
        },
        'Collaborator': {
            'username': 'Collaborator',
            'email': 'collaborator@kuehnlab.edu',
            'role': 'Collaborator',
            'can_create_projects': False,
            'can_edit_sample': True,
            'can_manage_analysis': True,
            'can_flag_samples': True,
            'can_create_subsample': True,
            'can_export_data': False
        },
        'View_Export': {
            'username': 'View Export User',
            'email': 'viewer@kuehnlab.edu',
            'role': 'View_Export',
            'can_create_projects': False,
            'can_edit_sample': False,
            'can_manage_analysis': False,
            'can_flag_samples': False,
            'can_create_subsample': False,
            'can_export_data': True
        },
        'View_Only': {
            'username': 'View Only User',
            'email': 'readonly@kuehnlab.edu',
            'role': 'View_Only',
            'can_create_projects': False,
            'can_edit_sample': False,
            'can_manage_analysis': False,
            'can_flag_samples': False,
            'can_create_subsample': False,
            'can_export_data': False
        }
    }

    if role in user_data:
        session['user'] = user_data[role]
        session['is_authenticated'] = True
        flash(f'Quick login as {role}', 'success')
    else:
        flash('Invalid role', 'error')

    return redirect(url_for('main.index'))
