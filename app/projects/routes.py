from flask import render_template, session
from app.projects import bp


def user_has_project_access(project):
    """Check if current user has access to this project"""
    # Public projects are accessible to everyone
    if not project.get('is_private'):
        return True

    # Check if user is logged in
    if not session.get('is_authenticated'):
        return False

    user = session.get('user', {})
    username = user.get('username', '')

    # Administrators have access to everything
    if user.get('role') == 'Administrator':
        return True

    # Check if user is the project owner
    if project.get('owner') == username:
        return True

    # Check if user is a collaborator
    collaborators = project.get('collaborators', '')
    if collaborators and username in collaborators:
        return True

    return False

projects = [
    {
        "id": 1,
        "title": "Tephra Analysis",
        "slug": "tephra-analysis",
        "owner": "Matthew Kenner",
        "status": "Ongoing",
        "type": "Tephra",
        "is_private": False,
        "last_updated": "2025-09-20",
        "priority": "High",
        "collaborators": "Samantha Diaz, John Wright",
        "tags": ["Sample Prep", "Imaging"],
        "description": "Analysis of volcanic tephra deposits to understand eruption history."
    },
    {
        "id": 2,
        "title": "Sediment Study",
        "slug": "sediment-study",
        "owner": "Ian Keitlan",
        "status": "Completed",
        "type": "Sedimentology",
        "is_private": True,
        "last_updated": "2025-08-11",
        "priority": "Medium",
        "collaborators": "Carlos Cortes Garcia",
        "tags": ["Mineralogy"],
        "description": "Study of sediment layers to reconstruct paleoenvironmental conditions."
    },
    {
        "id": 3,
        "title": "Volcanic Glass Imaging",
        "slug": "volcanic-glass-imaging",
        "owner": "Killian Bertsch",
        "status": "In Review",
        "type": "Imaging",
        "is_private": False,
        "last_updated": "2025-09-01",
        "priority": "High",
        "collaborators": "Matthew Kenner",
        "tags": ["Microscopy", "Analysis"],
        "description": "High-resolution imaging of volcanic glass shards for structural analysis."
    },
    {
        "id": 4,
        "title": "Lake Sample Processing",
        "slug": "lake-sample-processing",
        "owner": "Carlos Cortes Garcia",
        "status": "Completed",
        "type": "Geochemistry",
        "is_private": True,
        "last_updated": "2025-07-30",
        "priority": "Low",
        "collaborators": "Ian Keitlan, Samantha Diaz",
        "tags": ["Water Quality", "Lab Prep"],
        "description": "Processing and analysis of lake sediment samples."
    },
    {
        "id": 5,
        "title": "Pollen Fractionation",
        "slug": "pollen-fractionation",
        "owner": "Samantha Diaz",
        "status": "Ongoing",
        "type": "Palynology",
        "is_private": False,
        "last_updated": "2025-09-25",
        "priority": "High",
        "collaborators": "Matthew Kenner",
        "tags": ["Pollen", "Fractionation"],
        "description": "Separation and analysis of pollen grains for ecological reconstruction."
    },
    {
        "id": 6,
        "title": "Thin Section Petrography",
        "slug": "thin-section-petrography",
        "owner": "John Wright",
        "status": "Ongoing",
        "type": "Petrology",
        "is_private": False,
        "last_updated": "2025-09-22",
        "priority": "Medium",
        "collaborators": "Killian Bertsch",
        "tags": ["Microscopy", "Minerals"],
        "description": "Examination of thin rock sections under microscope."
    },
    {
        "id": 7,
        "title": "Geochemical Data Cleanup",
        "slug": "geochemical-data-cleanup",
        "owner": "Carlos Cortes Garcia",
        "status": "In Review",
        "type": "Geochemistry",
        "is_private": True,
        "last_updated": "2025-09-10",
        "priority": "High",
        "collaborators": "Samantha Diaz",
        "tags": ["Data Processing"],
        "description": "Post-processing of geochemical datasets for publication."
    },
    {
        "id": 8,
        "title": "Sieve Fraction Recording",
        "slug": "sieve-fraction-recording",
        "owner": "Matthew Kenner",
        "status": "Completed",
        "type": "Sedimentology",
        "is_private": False,
        "last_updated": "2025-07-18",
        "priority": "Low",
        "collaborators": "Ian Keitlan",
        "tags": ["Sieving", "Curation"],
        "description": "Recording of sediment fractions separated by sieve sizes."
    },
    {
        "id": 9,
        "title": "Legacy Dataset Migration",
        "slug": "legacy-dataset-migration",
        "owner": "Samantha Diaz",
        "status": "Archived",
        "type": "Database",
        "is_private": False,
        "last_updated": "2025-06-01",
        "priority": "Medium",
        "collaborators": "John Wright",
        "tags": ["Data Migration"],
        "description": "Migration of historical datasets into the new system."
    },
    {
        "id": 10,
        "title": "Carbonate Analysis Project",
        "slug": "carbonate-analysis-project",
        "owner": "Ian Keitlan",
        "status": "Ongoing",
        "type": "Geochemistry",
        "is_private": True,
        "last_updated": "2025-10-05",
        "priority": "High",
        "collaborators": "Matthew Kenner",
        "tags": ["Carbonates", "XRD"],
        "description": "Comprehensive analysis of carbonate mineral composition in marine samples."
    },
    {
        "id": 11,
        "title": "Microplastic Detection Study",
        "slug": "microplastic-detection-study",
        "owner": "Samantha Diaz",
        "status": "Ongoing",
        "type": "Environmental",
        "is_private": False,
        "last_updated": "2025-10-12",
        "priority": "High",
        "collaborators": "Killian Bertsch, Carlos Cortes Garcia",
        "tags": ["Pollution", "FTIR"],
        "description": "Identification and quantification of microplastics in aquatic sediments."
    },
    {
        "id": 12,
        "title": "Isotope Ratio Analysis",
        "slug": "isotope-ratio-analysis",
        "owner": "John Wright",
        "status": "In Review",
        "type": "Geochemistry",
        "is_private": True,
        "last_updated": "2025-09-28",
        "priority": "Medium",
        "collaborators": "Ian Keitlan",
        "tags": ["Isotopes", "Mass Spec"],
        "description": "Stable isotope analysis for paleoclimate reconstruction."
    },
    {
        "id": 13,
        "title": "Clay Mineralogy Survey",
        "slug": "clay-mineralogy-survey",
        "owner": "Carlos Cortes Garcia",
        "status": "Ongoing",
        "type": "Mineralogy",
        "is_private": False,
        "last_updated": "2025-10-08",
        "priority": "Medium",
        "collaborators": "Samantha Diaz",
        "tags": ["Clay", "XRD", "SEM"],
        "description": "Characterization of clay mineral assemblages in soil profiles."
    },
    {
        "id": 14,
        "title": "Diatom Assemblage Analysis",
        "slug": "diatom-assemblage-analysis",
        "owner": "Matthew Kenner",
        "status": "Completed",
        "type": "Paleoecology",
        "is_private": False,
        "last_updated": "2025-08-22",
        "priority": "Low",
        "collaborators": "John Wright",
        "tags": ["Diatoms", "Microscopy"],
        "description": "Study of diatom species composition in lake sediment cores."
    },
    {
        "id": 15,
        "title": "Grain Size Distribution",
        "slug": "grain-size-distribution",
        "owner": "Killian Bertsch",
        "status": "Ongoing",
        "type": "Sedimentology",
        "is_private": True,
        "last_updated": "2025-10-15",
        "priority": "High",
        "collaborators": "Matthew Kenner, Ian Keitlan",
        "tags": ["Particle Size", "Sieving"],
        "description": "Particle size analysis of coastal sediment deposits."
    },
    {
        "id": 16,
        "title": "Charcoal Fragment Study",
        "slug": "charcoal-fragment-study",
        "owner": "Samantha Diaz",
        "status": "In Review",
        "type": "Paleoecology",
        "is_private": False,
        "last_updated": "2025-09-18",
        "priority": "Medium",
        "collaborators": "Carlos Cortes Garcia",
        "tags": ["Fire History", "Charcoal"],
        "description": "Analysis of charcoal fragments for fire history reconstruction."
    },
    {
        "id": 17,
        "title": "Heavy Mineral Separation",
        "slug": "heavy-mineral-separation",
        "owner": "Ian Keitlan",
        "status": "Ongoing",
        "type": "Mineralogy",
        "is_private": False,
        "last_updated": "2025-10-10",
        "priority": "Medium",
        "collaborators": "John Wright",
        "tags": ["Minerals", "Density"],
        "description": "Extraction and identification of heavy mineral assemblages."
    },
    {
        "id": 18,
        "title": "Organic Carbon Content",
        "slug": "organic-carbon-content",
        "owner": "John Wright",
        "status": "Completed",
        "type": "Geochemistry",
        "is_private": True,
        "last_updated": "2025-07-25",
        "priority": "Low",
        "collaborators": "Samantha Diaz",
        "tags": ["TOC", "Elemental"],
        "description": "Total organic carbon analysis in sediment samples."
    },
    {
        "id": 19,
        "title": "Magnetic Susceptibility",
        "slug": "magnetic-susceptibility",
        "owner": "Carlos Cortes Garcia",
        "status": "Ongoing",
        "type": "Geophysics",
        "is_private": False,
        "last_updated": "2025-10-06",
        "priority": "High",
        "collaborators": "Killian Bertsch",
        "tags": ["Magnetism", "Core Scanning"],
        "description": "Magnetic susceptibility measurements for sediment correlation."
    },
    {
        "id": 20,
        "title": "Phytoplankton Pigments",
        "slug": "phytoplankton-pigments",
        "owner": "Matthew Kenner",
        "status": "In Review",
        "type": "Biogeochemistry",
        "is_private": True,
        "last_updated": "2025-09-30",
        "priority": "High",
        "collaborators": "Samantha Diaz, Ian Keitlan",
        "tags": ["HPLC", "Pigments"],
        "description": "Extraction and analysis of phytoplankton pigments from lake sediments."
    },
    {
        "id": 21,
        "title": "Radiocarbon Dating",
        "slug": "radiocarbon-dating",
        "owner": "Killian Bertsch",
        "status": "Ongoing",
        "type": "Geochronology",
        "is_private": False,
        "last_updated": "2025-10-14",
        "priority": "High",
        "collaborators": "John Wright",
        "tags": ["C14", "Dating"],
        "description": "Radiocarbon dating of organic materials for age-depth modeling."
    },
    {
        "id": 22,
        "title": "Mercury Concentration Study",
        "slug": "mercury-concentration-study",
        "owner": "Samantha Diaz",
        "status": "Completed",
        "type": "Environmental",
        "is_private": True,
        "last_updated": "2025-08-05",
        "priority": "Medium",
        "collaborators": "Carlos Cortes Garcia",
        "tags": ["Heavy Metals", "ICP-MS"],
        "description": "Quantification of mercury levels in contaminated sediments."
    },
    {
        "id": 23,
        "title": "Biogenic Silica Analysis",
        "slug": "biogenic-silica-analysis",
        "owner": "Ian Keitlan",
        "status": "Ongoing",
        "type": "Biogeochemistry",
        "is_private": False,
        "last_updated": "2025-10-11",
        "priority": "Medium",
        "collaborators": "Matthew Kenner",
        "tags": ["BSi", "Productivity"],
        "description": "Measurement of biogenic silica for paleoproductivity reconstruction."
    },
    {
        "id": 24,
        "title": "X-Ray Fluorescence Scanning",
        "slug": "x-ray-fluorescence-scanning",
        "owner": "John Wright",
        "status": "In Review",
        "type": "Geochemistry",
        "is_private": False,
        "last_updated": "2025-09-26",
        "priority": "High",
        "collaborators": "Killian Bertsch",
        "tags": ["XRF", "Core Scanning"],
        "description": "High-resolution XRF core scanning for elemental profiles."
    },
    {
        "id": 25,
        "title": "Ostracod Assemblage Research",
        "slug": "ostracod-assemblage-research",
        "owner": "Carlos Cortes Garcia",
        "status": "Archived",
        "type": "Paleoecology",
        "is_private": True,
        "last_updated": "2025-05-15",
        "priority": "Low",
        "collaborators": "Samantha Diaz",
        "tags": ["Ostracods", "Ecology"],
        "description": "Study of ostracod species for paleoenvironmental interpretation."
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

    has_access = user_has_project_access(project)
    return render_template("projects/project_detail.html",
                         title=project["title"],
                         project=project,
                         has_access=has_access)

@bp.route('/<slug>')
def project_detail_by_slug(slug):
    project = next((p for p in projects if p["slug"] == slug), None)
    if not project:
        return "Project not found", 404

    has_access = user_has_project_access(project)
    return render_template("projects/project_detail.html",
                         title=project["title"],
                         project=project,
                         has_access=has_access)


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
