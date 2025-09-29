from datetime import date

from flask import render_template, abort

from app.samples import bp
from app.projects.routes import projects as project_catalog


samples = [
    {
        "id": 1,
        "sample_code": "CULS-2025-001",
        "nickname": "Glass shard concentrate",
        "collected_on": date(2025, 9, 15),
        "collected_by": ["Samantha Diaz", "Carlos Cortes Garcia"],
        "site": {
            "project": 1,
            "site_name": "Red Hills Stratigraphic Section",
            "station": "RHS-03",
            "stratum": "Unit B, lapilli tuff",
            "depth_cm": 125,
            "gps": {
                "lat": 37.3652,
                "lon": -81.0965,
                "datum": "WGS84"
            },
            "depositional_context": "Distal tephra fall bed overlying lacustrine clay"
        },
        "metadata_flags": ["complete"],
        "associated_projects": [
            {"project_id": 1, "role": "Primary"},
            {"project_id": 3, "role": "Imaging"}
        ],
        "attachments": {
            "images": [
                {"filename": "CULS-2025-001_overview.jpg", "caption": "Sample bag with GPS puck"},
                {"filename": "CULS-2025-001_field-closeup.jpg", "caption": "Fresh surface at collection point"}
            ],
            "notes": [
                "Collected immediately below weathered contact; moisture high.",
                "Samples split in field for particle-size and geochemical workflows."
            ],
            "instrument_logs": [
                {"instrument": "Garmin GPSMAP 66i", "detail": "PDOP 1.6, averaged for 30 seconds"},
                {"instrument": "Brunton compass", "detail": "Bedding 112/18"}
            ]
        },
        "processing": {
            "sieve_stack": ["2 mm", "1 mm", "63 µm", "Pan"],
            "fraction_targets": [
                {"fraction": "2-1 mm", "expected_percent": 15},
                {"fraction": "1 mm - 63 µm", "expected_percent": 60},
                {"fraction": "<63 µm", "expected_percent": 25}
            ],
            "mass_entries": [
                {"fraction": "2-1 mm", "wet_mass_g": 80, "dry_mass_g": 72},
                {"fraction": "1 mm - 63 µm", "wet_mass_g": 250, "dry_mass_g": 238},
                {"fraction": "<63 µm", "wet_mass_g": 190, "dry_mass_g": 184}
            ],
            "derived_metrics": {
                "total_dry_mass_g": 494,
                "mass_recovery_percent": 98.8
            }
        },
        "physical_analysis": {
            "particle_size_distribution": "Pending laser diffraction run",
            "density_g_cc": 2.35,
            "clast_size": "Coarse ash / lapilli",
            "componentry_summary": "Glass shards 70%, crystals 20%, lithics 10%",
            "uploads": [
                {"filename": "CULS-2025-001_graincount.xlsx", "status": "Uploaded"}
            ]
        },
        "imaging": {
            "sessions": [
                {
                    "instrument": "JEOL JSM-IT200 SEM",
                    "date": "2025-09-21",
                    "operator": "Killian Bertsch",
                    "settings": "15 kV, 10 mm WD, gold sputter coat",
                    "files": ["SEM_001.tif", "SEM_002.tif"],
                    "status": "Uploaded"
                }
            ],
            "next_steps": "Schedule EPMA session for glass chemistry"
        },
        "geochemistry": {
            "raw_uploads": ["CULS-2025-001_XRF_raw.xlsx"],
            "processed_uploads": [],
            "reference_standards": ["GSR-5", "SCO-1"],
            "qa_notes": "Awaiting standard drift check",
            "auto_processing": "Enabled - converts raw XRF to oxide percentages"
        },
        "correlation": {
            "targets": [
                {
                    "sample_code": "CULS-2025-018",
                    "project": "Summit Lake Core",
                    "basis": "Glass shard major oxides",
                    "confidence": "High"
                }
            ],
            "checklist": [
                {"item": "Stratigraphic alignment documented", "status": True},
                {"item": "Geochemical match within tolerance", "status": False},
                {"item": "Notes recorded", "status": True}
            ],
            "summary": "Preliminary correlation to lacustrine tephra at Summit Lake pending geochem validation."
        },
        "workflow_status": [
            {"name": "Collection", "state": "Complete", "updated": "2025-09-15"},
            {"name": "Processing", "state": "In Progress", "updated": "2025-09-20"},
            {"name": "Physical Analysis", "state": "Queued", "updated": None},
            {"name": "Geochemical Analysis", "state": "Pending", "updated": None}
        ]
    },
    {
        "id": 2,
        "sample_code": "CULS-2025-018",
        "nickname": "Lake core fraction",
        "collected_on": date(2025, 8, 2),
        "collected_by": ["Ian Keitlan"],
        "site": {
            "project": 4,
            "site_name": "Summit Lake Core",
            "station": "SL-01",
            "stratum": "60-65 cm",
            "depth_cm": 62,
            "gps": {
                "lat": 37.5423,
                "lon": -81.0152,
                "datum": "WGS84"
            },
            "depositional_context": "Laminated silt with organic stringers"
        },
        "metadata_flags": ["needs-lab-notes"],
        "associated_projects": [
            {"project_id": 4, "role": "Primary"},
            {"project_id": 7, "role": "Geochem QA"}
        ],
        "attachments": {
            "images": [
                {"filename": "CULS-2025-018_core-box.jpg", "caption": "Core sections prior to splitting"}
            ],
            "notes": [
                "Stored at 4°C. Pending FTIR spectrum.",
                "Request geochem lab to include reference standards GSR-5, SCO-1."
            ],
            "instrument_logs": [
                {"instrument": "UWITEC corer", "detail": "Core recovery 98%"},
                {"instrument": "Analytical balance", "detail": "Initial wet mass 1.25 kg"}
            ]
        },
        "processing": {
            "sieve_stack": ["500 µm", "125 µm", "63 µm", "Pan"],
            "fraction_targets": [
                {"fraction": ">500 µm", "expected_percent": 5},
                {"fraction": "500-125 µm", "expected_percent": 35},
                {"fraction": "125-63 µm", "expected_percent": 40},
                {"fraction": "<63 µm", "expected_percent": 20}
            ],
            "mass_entries": [
                {"fraction": ">500 µm", "wet_mass_g": 40, "dry_mass_g": 18},
                {"fraction": "500-125 µm", "wet_mass_g": 310, "dry_mass_g": 280},
                {"fraction": "125-63 µm", "wet_mass_g": 380, "dry_mass_g": 344},
                {"fraction": "<63 µm", "wet_mass_g": 520, "dry_mass_g": 495}
            ],
            "derived_metrics": {
                "total_dry_mass_g": 1137,
                "mass_recovery_percent": 102.6
            }
        },
        "physical_analysis": {
            "particle_size_distribution": "Laser diffraction uploaded",
            "density_g_cc": 1.65,
            "clast_size": "Silt",
            "componentry_summary": "Organic matter 12%, diatoms 25%, mineral fines 63%",
            "uploads": [
                {"filename": "CULS-2025-018_psd.csv", "status": "Uploaded"},
                {"filename": "CULS-2025-018_density.xlsx", "status": "Pending QA"}
            ]
        },
        "imaging": {
            "sessions": [],
            "next_steps": "Consider micro-CT for porosity assessment"
        },
        "geochemistry": {
            "raw_uploads": ["CULS-2025-018_ICPMS_raw.xlsx"],
            "processed_uploads": ["CULS-2025-018_ICPMS_processed.xlsx"],
            "reference_standards": ["GSR-5", "BHVO-2"],
            "qa_notes": "Standard recoveries within ±3%",
            "auto_processing": "Manual review required for organic-rich fractions"
        },
        "correlation": {
            "targets": [
                {
                    "sample_code": "CULS-2025-001",
                    "project": "Tephra Analysis",
                    "basis": "TiO2 vs FeO*/MgO plot",
                    "confidence": "Moderate"
                }
            ],
            "checklist": [
                {"item": "Stratigraphic alignment documented", "status": True},
                {"item": "Geochemical match within tolerance", "status": True},
                {"item": "Notes recorded", "status": True}
            ],
            "summary": "Correlation strengthens distal-proximal interpretation for Summit Lake tephra."
        },
        "workflow_status": [
            {"name": "Collection", "state": "Complete", "updated": "2025-08-02"},
            {"name": "Processing", "state": "Complete", "updated": "2025-08-09"},
            {"name": "Geochemical Analysis", "state": "In Review", "updated": "2025-09-19"},
            {"name": "Correlation", "state": "Draft", "updated": None}
        ]
    },
    {
        "id": 3,
        "sample_code": "CULS-2025-034",
        "nickname": "Legacy thin section",
        "collected_on": date(1998, 6, 12),
        "collected_by": ["Unknown"],
        "site": {
            "project": None,
            "site_name": "Legacy archive",
            "station": "Archived slide drawer 4",
            "stratum": "Unknown",
            "depth_cm": None,
            "gps": None,
            "depositional_context": "Legacy dataset imported from departmental records"
        },
        "metadata_flags": ["legacy", "partial"],
        "associated_projects": [
            {"project_id": 9, "role": "Migration"}
        ],
        "attachments": {
            "images": [],
            "notes": [
                "Digitized metadata pending.",
                "Mark as usable but highlight missing stratigraphic log."
            ],
            "instrument_logs": []
        },
        "processing": None,
        "physical_analysis": None,
        "imaging": {
            "sessions": [
                {
                    "instrument": "Petrographic microscope",
                    "date": "2025-09-05",
                    "operator": "John Wright",
                    "settings": "Cross-polars, 4x & 10x",
                    "files": ["legacy_thinsection_scan.pdf"],
                    "status": "Digitized"
                }
            ],
            "next_steps": "Assess need for SEM backscatter images"
        },
        "geochemistry": None,
        "correlation": {
            "targets": [],
            "checklist": [
                {"item": "Stratigraphic alignment documented", "status": False},
                {"item": "Geochemical match within tolerance", "status": False},
                {"item": "Notes recorded", "status": True}
            ],
            "summary": "Legacy record requires metadata reconciliation before correlation."
        },
        "workflow_status": [
            {"name": "Collection", "state": "Legacy", "updated": None},
            {"name": "Imaging", "state": "Complete", "updated": "2025-09-05"},
            {"name": "Correlation", "state": "Needs Review", "updated": None}
        ]
    }
]


project_lookup = {project["id"]: project for project in project_catalog}


def format_sample(sample):
    formatted = sample.copy()
    if isinstance(formatted["collected_on"], date):
        formatted["collected_on_display"] = formatted["collected_on"].strftime("%Y-%m-%d")
    else:
        formatted["collected_on_display"] = "Unknown"

    formatted["projects"] = [
        {
            "project": project_lookup.get(link["project_id"]),
            "role": link["role"]
        }
        for link in formatted["associated_projects"]
        if link["project_id"] in project_lookup
    ]
    return formatted


@bp.route("/")
def sample_list():
    formatted_samples = [format_sample(sample) for sample in samples]
    workflow_entry_count = sum(len(sample["workflow_status"]) for sample in samples)
    return render_template(
        "samples/sample_list.html",
        title="Samples",
        samples=formatted_samples,
        workflow_entry_count=workflow_entry_count,
    )


@bp.route("/register")
def sample_register():
    return render_template(
        "samples/sample_register.html",
        title="Register Sample",
        projects=project_catalog,
    )


@bp.route("/bulk-upload")
def sample_bulk_upload():
    workbook_templates = [
        {"name": "Collection Workbook", "filename": "CULS_collection_template.xlsx"},
        {"name": "Processing & Preparation", "filename": "CULS_processing_template.xlsx"},
        {"name": "Physical Analysis", "filename": "CULS_physical_analysis_template.xlsx"},
        {"name": "Geochemical Analysis", "filename": "CULS_geochem_template.xlsx"},
        {"name": "Correlation Workbook", "filename": "CULS_correlation_template.xlsx"},
    ]
    return render_template(
        "samples/sample_bulk_upload.html",
        title="Bulk Upload Samples",
        templates=workbook_templates,
    )


@bp.route("/<sample_code>")
def sample_detail(sample_code):
    sample = next((s for s in samples if s["sample_code"] == sample_code), None)
    if not sample:
        abort(404)
    formatted = format_sample(sample)
    return render_template(
        "samples/sample_detail.html",
        title=formatted["sample_code"],
        sample=formatted,
    )
