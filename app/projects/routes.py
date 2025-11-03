from flask import render_template
from app.projects import bp

projects = [
    {
        "id": 1,
        "title": "Tephra Analysis",
        "owner": "Matthew Kenner",
        "status": "Ongoing",
        "type": "Tephra",
        "last_updated": "2025-09-20",
        "priority": "High",
        "collaborators": "Samantha Diaz, John Wright",
        "tags": ["Sample Prep", "Imaging"],
        "description": "Analysis of volcanic tephra deposits to understand eruption history."
    },
    {
        "id": 2,
        "title": "Sediment Study",
        "owner": "Ian Keitlan",
        "status": "Completed",
        "type": "Sedimentology",
        "last_updated": "2025-08-11",
        "priority": "Medium",
        "collaborators": "Carlos Cortes Garcia",
        "tags": ["Mineralogy"],
        "description": "Study of sediment layers to reconstruct paleoenvironmental conditions."
    },
    {
        "id": 3,
        "title": "Volcanic Glass Imaging",
        "owner": "Killian Bertsch",
        "status": "In Review",
        "type": "Imaging",
        "last_updated": "2025-09-01",
        "priority": "High",
        "collaborators": "Matthew Kenner",
        "tags": ["Microscopy", "Analysis"],
        "description": "High-resolution imaging of volcanic glass shards for structural analysis."
    },
    {
        "id": 4,
        "title": "Lake Sample Processing",
        "owner": "Carlos Cortes Garcia",
        "status": "Completed",
        "type": "Geochemistry",
        "last_updated": "2025-07-30",
        "priority": "Low",
        "collaborators": "Ian Keitlan, Samantha Diaz",
        "tags": ["Water Quality", "Lab Prep"],
        "description": "Processing and analysis of lake sediment samples."
    },
    {
        "id": 5,
        "title": "Pollen Fractionation",
        "owner": "Samantha Diaz",
        "status": "Ongoing",
        "type": "Palynology",
        "last_updated": "2025-09-25",
        "priority": "High",
        "collaborators": "Matthew Kenner",
        "tags": ["Pollen", "Fractionation"],
        "description": "Separation and analysis of pollen grains for ecological reconstruction."
    },
    {
        "id": 6,
        "title": "Thin Section Petrography",
        "owner": "John Wright",
        "status": "Ongoing",
        "type": "Petrology",
        "last_updated": "2025-09-22",
        "priority": "Medium",
        "collaborators": "Killian Bertsch",
        "tags": ["Microscopy", "Minerals"],
        "description": "Examination of thin rock sections under microscope."
    },
    {
        "id": 7,
        "title": "Geochemical Data Cleanup",
        "owner": "Carlos Cortes Garcia",
        "status": "In Review",
        "type": "Geochemistry",
        "last_updated": "2025-09-10",
        "priority": "High",
        "collaborators": "Samantha Diaz",
        "tags": ["Data Processing"],
        "description": "Post-processing of geochemical datasets for publication."
    },
    {
        "id": 8,
        "title": "Sieve Fraction Recording",
        "owner": "Matthew Kenner",
        "status": "Completed",
        "type": "Sedimentology",
        "last_updated": "2025-07-18",
        "priority": "Low",
        "collaborators": "Ian Keitlan",
        "tags": ["Sieving", "Curation"],
        "description": "Recording of sediment fractions separated by sieve sizes."
    },
    {
        "id": 9,
        "title": "Legacy Dataset Migration",
        "owner": "Samantha Diaz",
        "status": "Archived",
        "type": "Database",
        "last_updated": "2025-06-01",
        "priority": "Medium",
        "collaborators": "John Wright",
        "tags": ["Data Migration"],
        "description": "Migration of historical datasets into the new system."
    }
]

# We are going to have to change this to be the homepage (where the projects are now)
@bp.route('/')
def project_list():
    return render_template("projects/project_list.html", title="Projects", projects=projects)

@bp.route('/<int:project_id>')
def project_detail(project_id):
    project = next((p for p in projects if p["id"] == project_id), None)
    if not project:
        return "Project not found", 404
    return render_template("projects/project_detail.html", title=project["title"], project=project)


@bp.route('/new')
def project_create():
    funding_agencies = [
        "NSF",
        "USGS",
        "NASA",
        "NOAA",
        "Internal / Institutional",
    ]
    visibility_options = [
        {"value": "internal", "label": "Internal only"},
        {"value": "public", "label": "Public metadata (title + PI)"},
    ]
    return render_template(
        "projects/project_create.html",
        title="Create Project",
        funding_agencies=funding_agencies,
        visibility_options=visibility_options,
    )
