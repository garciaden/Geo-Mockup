from flask import render_template, redirect, url_for, request
from datetime import datetime

from app.main import bp
from app.projects.routes import projects as project_catalog
from app.samples.routes import samples as sample_catalog, format_sample


def format_relative_time(date_string):
    """Convert date string to relative time (e.g., '2 days ago')"""
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        delta = datetime.now() - date_obj

        if delta.days == 0:
            return "today"
        elif delta.days == 1:
            return "1 day ago"
        elif delta.days < 7:
            return f"{delta.days} days ago"
        elif delta.days < 30:
            weeks = delta.days // 7
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"
        elif delta.days < 365:
            months = delta.days // 30
            return f"{months} month{'s' if months != 1 else ''} ago"
        else:
            years = delta.days // 365
            return f"{years} year{'s' if years != 1 else ''} ago"
    except:
        return date_string


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
    elif sort_by == 'last_updated':
        filtered_projects = sorted(filtered_projects, key=lambda x: x.get('last_updated', ''), reverse=reverse)
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

    # Format dates as relative time for display
    for project in paginated_projects:
        if 'last_updated' in project:
            project['last_updated_relative'] = format_relative_time(project['last_updated'])
        else:
            project['last_updated_relative'] = 'Unknown'

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


@bp.route('/admin/all-samples')
def all_samples():
    """Admin view: All samples across all projects"""
    # Mock data for all samples
    all_samples_data = [
        {
            'sample_id': 'JL20-01A-1',
            'lab_catalog': 'LAB-2025-001',
            'short_description': 'Mount St. Helens Tephra Layer A',
            'project_title': 'Mount St. Helens Eruption Analysis',
            'project_owner': 'Dr. Jessica Lane',
            'collection_date': '2025-09-15',
            'status': 'Active',
            'has_physical': False,
            'has_micro': False,
            'has_geochem': False,
        },
        {
            'sample_id': 'JL20-01A-2',
            'lab_catalog': 'LAB-2025-002',
            'short_description': 'Volcanic Ash Sample - Site B',
            'project_title': 'Mount St. Helens Eruption Analysis',
            'project_owner': 'Dr. Jessica Lane',
            'collection_date': '2025-08-02',
            'status': 'Active',
            'has_physical': True,
            'has_micro': True,
            'has_geochem': False,
        },
        {
            'sample_id': 'MC19-05B-1',
            'lab_catalog': 'LAB-2025-009',
            'short_description': 'Basalt Core - Mid-Ocean Ridge',
            'project_title': 'Mid-Atlantic Ridge Basalt Study',
            'project_owner': 'Dr. Maria Chen',
            'collection_date': '2025-07-12',
            'status': 'Active',
            'has_physical': True,
            'has_micro': False,
            'has_geochem': True,
        },
        {
            'sample_id': 'TR24-02C-3',
            'lab_catalog': 'LAB-2024-156',
            'short_description': 'Rhyolite Dome Fragment',
            'project_title': 'Cascadia Volcanic Arc Survey',
            'project_owner': 'Dr. Thomas Rodriguez',
            'collection_date': '2024-11-20',
            'status': 'Archived',
            'has_physical': True,
            'has_micro': True,
            'has_geochem': True,
        },
        {
            'sample_id': 'SD23-08A-5',
            'lab_catalog': 'LAB-2023-442',
            'short_description': 'Obsidian Flow Sample',
            'project_title': 'Holocene Volcanism Timeline',
            'project_owner': 'Dr. Sarah Davis',
            'collection_date': '2023-06-15',
            'status': 'Active',
            'has_physical': True,
            'has_micro': False,
            'has_geochem': True,
        },
    ]

    return render_template(
        "main/all_samples.html",
        title="All Samples",
        samples=all_samples_data
    )


@bp.route('/admin/all-geochemical')
def all_geochemical():
    """Admin view: All geochemical analyses across all projects"""
    geochem_data = [
        {
            'sample_id': 'MC19-05B-1',
            'lab_catalog': 'LAB-2025-009',
            'project_title': 'Mid-Atlantic Ridge Basalt Study',
            'analysis_type': 'ICP-MS',
            'run_date': '2025-10-15',
            'analyst': 'Dr. James Wilson',
            'elements_analyzed': 'REE, Trace Elements (45 elements)',
            'status': 'Complete',
            'qc_status': 'Passed'
        },
        {
            'sample_id': 'SD23-08A-5',
            'lab_catalog': 'LAB-2023-442',
            'project_title': 'Holocene Volcanism Timeline',
            'analysis_type': 'XRF (Whole Rock)',
            'run_date': '2023-08-20',
            'analyst': 'Lab Field Team',
            'elements_analyzed': 'Major Elements (10 elements)',
            'status': 'Complete',
            'qc_status': 'Passed'
        },
        {
            'sample_id': 'TR24-02C-3',
            'lab_catalog': 'LAB-2024-156',
            'project_title': 'Cascadia Volcanic Arc Survey',
            'analysis_type': 'LA-ICP-MS',
            'run_date': '2024-12-05',
            'analyst': 'Dr. Maria Chen',
            'elements_analyzed': 'In-situ trace elements',
            'status': 'Complete',
            'qc_status': 'Passed'
        },
        {
            'sample_id': 'JL20-01A-4',
            'lab_catalog': 'LAB-2025-004',
            'project_title': 'Mount St. Helens Eruption Analysis',
            'analysis_type': 'SIMS',
            'run_date': '2025-10-28',
            'analyst': 'Dr. Sarah Davis',
            'elements_analyzed': 'O, H isotopes',
            'status': 'In Progress',
            'qc_status': 'Pending'
        },
    ]

    return render_template(
        "main/all_geochemical.html",
        title="All Geochemical Analysis",
        analyses=geochem_data
    )


@bp.route('/admin/all-microanalysis')
def all_microanalysis():
    """Admin view: All microanalysis data across all projects"""
    micro_data = [
        {
            'sample_id': 'JL20-01A-2',
            'lab_catalog': 'LAB-2025-002',
            'project_title': 'Mount St. Helens Eruption Analysis',
            'analysis_type': 'EPMA/SEM',
            'run_date': '2025-09-10',
            'analyst': 'Dr. Thomas Rodriguez',
            'minerals_analyzed': 'Plagioclase, Pyroxene, Fe-Ti oxides',
            'points_analyzed': 127,
            'status': 'Complete',
            'qc_status': 'Passed'
        },
        {
            'sample_id': 'TR24-02C-3',
            'lab_catalog': 'LAB-2024-156',
            'project_title': 'Cascadia Volcanic Arc Survey',
            'analysis_type': 'EPMA/SEM',
            'run_date': '2024-12-01',
            'analyst': 'Dr. Jessica Lane',
            'minerals_analyzed': 'Quartz, K-feldspar, Biotite',
            'points_analyzed': 85,
            'status': 'Complete',
            'qc_status': 'Passed'
        },
        {
            'sample_id': 'JL20-01A-4',
            'lab_catalog': 'LAB-2025-004',
            'project_title': 'Mount St. Helens Eruption Analysis',
            'analysis_type': 'Micro-XRF',
            'run_date': '2025-09-25',
            'analyst': 'Lab Field Team',
            'minerals_analyzed': 'Zircon mapping',
            'points_analyzed': 450,
            'status': 'Complete',
            'qc_status': 'Passed'
        },
    ]

    return render_template(
        "main/all_microanalysis.html",
        title="All Microanalysis",
        analyses=micro_data
    )


@bp.route('/admin/all-physical')
def all_physical():
    """Admin view: All physical analysis data across all projects"""
    physical_data = [
        {
            'sample_id': 'JL20-01A-2',
            'lab_catalog': 'LAB-2025-002',
            'project_title': 'Mount St. Helens Eruption Analysis',
            'analysis_type': 'Sieve Analysis',
            'run_date': '2025-08-15',
            'analyst': 'Lab Field Team',
            'parameters': 'Grain size distribution (2mm - 63µm)',
            'total_mass': '245.8 g',
            'status': 'Complete',
        },
        {
            'sample_id': 'MC19-05B-1',
            'lab_catalog': 'LAB-2025-009',
            'project_title': 'Mid-Atlantic Ridge Basalt Study',
            'analysis_type': 'Density Separation',
            'run_date': '2025-07-28',
            'analyst': 'Dr. James Wilson',
            'parameters': 'Heavy liquid separation (2.85 g/cm³)',
            'total_mass': '156.2 g',
            'status': 'Complete',
        },
        {
            'sample_id': 'TR24-02C-3',
            'lab_catalog': 'LAB-2024-156',
            'project_title': 'Cascadia Volcanic Arc Survey',
            'analysis_type': 'Magnetic Separation',
            'run_date': '2024-11-30',
            'analyst': 'Lab Field Team',
            'parameters': 'Frantz separation (0.5A - 1.5A)',
            'total_mass': '89.5 g',
            'status': 'Complete',
        },
        {
            'sample_id': 'SD23-08A-5',
            'lab_catalog': 'LAB-2023-442',
            'project_title': 'Holocene Volcanism Timeline',
            'analysis_type': 'Loss on Ignition',
            'run_date': '2023-06-22',
            'analyst': 'Dr. Sarah Davis',
            'parameters': '550°C, 950°C',
            'total_mass': '10.2 g',
            'status': 'Complete',
        },
    ]

    return render_template(
        "main/all_physical.html",
        title="All Physical Analysis",
        analyses=physical_data
    )
