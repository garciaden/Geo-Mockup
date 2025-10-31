from flask import render_template, redirect, url_for, request

from app.main import bp
from app.projects.routes import projects as project_catalog
from app.samples.routes import samples as sample_catalog, format_sample


@bp.route('/')
def index():
    # Get search query from request
    search_query = request.args.get('search', '').strip().lower()

    # Get sort parameters
    sort_by = request.args.get('sort_by', 'title')  # Default sort by title
    sort_order = request.args.get('sort_order', 'asc')  # Default ascending

    # Get pagination parameter (projects per page)
    try:
        per_page = int(request.args.get('per_page', 10))
        # Limit to reasonable values
        if per_page not in [5, 10, 15, 20, 25, 50]:
            per_page = 10
    except ValueError:
        per_page = 10

    # Get page number
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    # Filter projects based on search query
    filtered_projects = project_catalog
    if search_query:
        filtered_projects = [
            project for project in project_catalog
            if search_query in project.get("title", "").lower() or
               search_query in project.get("owner", "").lower()
        ]

    # Sort projects
    reverse = (sort_order == 'desc')
    if sort_by == 'owner':
        filtered_projects = sorted(filtered_projects, key=lambda x: x.get('owner', '').lower(), reverse=reverse)
    else:  # Default to title
        filtered_projects = sorted(filtered_projects, key=lambda x: x.get('title', '').lower(), reverse=reverse)

    # Calculate pagination
    total_projects = len(filtered_projects)
    total_pages = (total_projects + per_page - 1) // per_page  # Ceiling division

    # Ensure page is within bounds
    if page > total_pages and total_pages > 0:
        page = total_pages

    # Get projects for current page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_projects = filtered_projects[start_idx:end_idx]

    # Pagination info
    pagination = {
        'page': page,
        'per_page': per_page,
        'total_projects': total_projects,
        'total_pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_page': page - 1 if page > 1 else None,
        'next_page': page + 1 if page < total_pages else None,
    }

    # Sort info
    sort_info = {
        'sort_by': sort_by,
        'sort_order': sort_order,
    }

    return render_template(
        "main/index.html",
        title="Home",
        projects=paginated_projects,
        pagination=pagination,
        search_query=search_query,
        sort_info=sort_info
    )


@bp.route('/login')
def fake_login():
    return redirect(url_for('auth.login'))
