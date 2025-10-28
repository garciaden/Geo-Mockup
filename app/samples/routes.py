from copy import deepcopy
from datetime import date, timedelta

from flask import render_template, abort

from app.samples import bp
from app.projects.routes import projects as project_catalog


samples = [
    {
        "id": 1,
        "sample_code": "CULS-2025-001",
        "nickname": "Glass shard concentrate",
        "collected_on": date(2025, 9, 15),
        "collected_by": ["Carlos Cortes Garcia", "Matthew Kenner"],
        "status": "active",
        "storage_location": "Cold Storage · Rack A3",
        "igsn": "IGSN:CULS-2025-001",
        "description": "Glass-rich tephra concentrate archived for comparison workflows.",
        "is_flagged_for_review": False,
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
        "status": "in review",
        "storage_location": "Cold Storage · Rack B1",
        "igsn": "IGSN:CULS-2025-018",
        "description": "Fine sediment fraction pulled from Summit Lake piston core.",
        "is_flagged_for_review": True,
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
        "collected_by": ["Killian Bertsch"],
        "status": "archived",
        "storage_location": "Legacy Slide Drawer 4",
        "igsn": "IGSN:CULS-1998-034",
        "description": "Legacy thin section digitized from departmental archive.",
        "is_flagged_for_review": False,
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
                    "operator": "Matthew Kenner",
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
sample_lookup = {sample["sample_code"]: sample for sample in samples}
ALLOWED_PEOPLE = (
    "Carlos Cortes Garcia",
    "Matthew Kenner",
    "Ian Keitlan",
    "Killian Bertsch",
)
ALLOWED_PEOPLE_SET = set(ALLOWED_PEOPLE)


def _slugify_name(name):
    if not isinstance(name, str):
        return "unknown"
    cleaned = "".join(ch for ch in name.lower() if ch.isalnum() or ch in {" ", "."})
    cleaned = cleaned.strip().replace(" ", ".").strip(".")
    return cleaned or "unknown"


def _default_email(name):
    slug = _slugify_name(name)
    return f"{slug}@culs.example.edu"


def _relative_time(date_value):
    if not isinstance(date_value, date):
        return "recently"
    delta = date.today() - date_value
    if delta.days <= 0:
        return "today"
    if delta.days == 1:
        return "1 day ago"
    if delta.days < 7:
        return f"{delta.days} days ago"
    if delta.days < 30:
        weeks = delta.days // 7
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    if delta.days < 365:
        months = delta.days // 30
        return f"{months} month{'s' if months != 1 else ''} ago"
    years = delta.days // 365
    return f"{years} year{'s' if years != 1 else ''} ago"


def _build_linked_people(sample):
    people = []
    seen = set()
    for idx, name in enumerate(sample.get("collected_by") or []):
        if not name or not isinstance(name, str):
            continue
        if name not in ALLOWED_PEOPLE_SET:
            continue
        key = name.lower()
        if key in seen:
            continue
        seen.add(key)
        people.append(
            {
                "id": f"{sample.get('sample_code', 'sample')}-collector-{idx}",
                "full_name": name,
                "role": "Field Collector",
                "institution": "CULS Field Team",
                "email": _default_email(name),
                "profile_url": "#",
            }
        )
    for link in sample.get("associated_projects") or []:
        project = project_lookup.get(link.get("project_id"))
        if not project:
            continue
        owner = project.get("owner")
        if owner and owner in ALLOWED_PEOPLE_SET:
            key = owner.lower()
            if key not in seen:
                seen.add(key)
                people.append(
                    {
                        "id": f"{project['id']}-pi",
                        "full_name": owner,
                        "role": "Project PI",
                        "institution": "Concord University",
                        "email": _default_email(owner),
                        "profile_url": "#",
                    }
                )
        collaborators = project.get("collaborators", "")
        for collaborator in [c.strip() for c in collaborators.split(",") if c.strip()]:
            key = collaborator.lower()
            if key in seen or collaborator not in ALLOWED_PEOPLE_SET:
                continue
            seen.add(key)
            people.append(
                {
                    "id": f"{project['id']}-collab-{len(people)}",
                    "full_name": collaborator,
                    "role": "Collaborator",
                    "institution": project.get("type", "Partner Lab"),
                    "email": _default_email(collaborator),
                    "profile_url": "#",
                }
            )
    if not people:
        fallback = ALLOWED_PEOPLE[0]
        people.append(
            {
                "id": f"{sample.get('sample_code', 'sample')}-fallback",
                "full_name": fallback,
                "role": "Data Steward",
                "institution": "Concord University",
                "email": _default_email(fallback),
                "profile_url": "#",
            }
        )
    return people


def _build_related_samples(sample):
    related = []
    for target in sample.get("correlation", {}).get("targets", []):
        related_sample = sample_lookup.get(target.get("sample_code"))
        related.append(
            {
                "sample_code": target.get("sample_code"),
                "name": (related_sample or {}).get("nickname", target.get("sample_code")),
                "relationship": target.get("basis", target.get("confidence", "Related")),
                "project": target.get("project"),
            }
        )
    return related


def _build_qc_flags(flags):
    mapping = {
        "complete": ("Metadata complete", "low"),
        "needs-lab-notes": ("Field notes required", "high"),
        "legacy": ("Legacy import – verify context", "medium"),
        "partial": ("Metadata incomplete", "medium"),
    }
    qc_flags = []
    for flag in flags or []:
        label, severity = mapping.get(flag, (flag.replace("-", " ").title(), "info"))
        qc_flags.append({"label": label, "severity": severity})
    return qc_flags


def _build_physical_sections(sample):
    section_keys = [
        "macro",
        "componentry",
        "particle_size",
        "max_clast",
        "density",
        "core",
        "cryptotephra",
    ]
    sections = {key: [] for key in section_keys}
    site = sample.get("site") or {}
    physical = sample.get("physical_analysis") or {}
    processing = sample.get("processing") or {}

    if site.get("depositional_context"):
        sections["macro"].append(
            {
                "parameter": "Depositional context",
                "value": site["depositional_context"],
                "unit": "",
                "method": "Field log",
                "notes": site.get("station", "—"),
            }
        )
    if site.get("depth_cm"):
        sections["macro"].append(
            {
                "parameter": "Depth",
                "value": site["depth_cm"],
                "unit": "cm",
                "method": "Measuring tape",
                "notes": site.get("stratum", "—"),
            }
        )

    if physical.get("componentry_summary"):
        sections["componentry"].append(
            {
                "parameter": "Componentry summary",
                "value": physical["componentry_summary"],
                "unit": "%",
                "method": "Point count (n=200)",
                "notes": "",
            }
        )

    for entry in processing.get("mass_entries", []) or []:
        sections["particle_size"].append(
            {
                "parameter": entry.get("fraction", "Fraction"),
                "value": entry.get("dry_mass_g", entry.get("wet_mass_g", "—")),
                "unit": "g",
                "method": "Sieving workflow",
                "notes": f"Wet mass {entry.get('wet_mass_g', '—')} g",
            }
        )

    if physical.get("clast_size"):
        sections["max_clast"].append(
            {
                "parameter": "Observed clast size",
                "value": physical["clast_size"],
                "unit": "",
                "method": "Hand lens estimate",
                "notes": "",
            }
        )

    if physical.get("density_g_cc"):
        sections["density"].append(
            {
                "parameter": "Bulk density",
                "value": physical["density_g_cc"],
                "unit": "g/cm³",
                "method": "Pycnometer",
                "notes": "",
            }
        )

    if site.get("stratum"):
        sections["core"].append(
            {
                "parameter": "Stratigraphic interval",
                "value": site["stratum"],
                "unit": "",
                "method": "Core log",
                "notes": site.get("site_name", ""),
            }
        )

    correlation_summary = sample.get("correlation", {}).get("summary")
    if correlation_summary:
        sections["cryptotephra"].append(
            {
                "parameter": "Correlation notes",
                "value": correlation_summary,
                "unit": "",
                "method": "Correlation workbook",
                "notes": "",
            }
        )

    return sections


def _categorize_imaging_session(instrument_name):
    instrument = (instrument_name or "").lower()
    if "optical" in instrument or "petrographic" in instrument:
        return "optical"
    if "electron" in instrument or "sem" in instrument:
        return "electron"
    if "ct" in instrument or "tomography" in instrument:
        return "tomography"
    return "other"


def _build_micro_sections(sample):
    imaging_sections = {
        "optical": {"images": [], "metadata": []},
        "electron": {"images": [], "metadata": []},
        "tomography": {"images": [], "metadata": []},
        "other": {"images": [], "metadata": []},
    }
    imaging = sample.get("imaging") or {}
    for session in imaging.get("sessions", []) or []:
        key = _categorize_imaging_session(session.get("instrument"))
        label = session.get("instrument", "Imaging Session")
        caption_prefix = label.split()[0]
        for idx, filename in enumerate(session.get("files") or []):
            imaging_sections[key]["images"].append(
                {
                    "thumbnail_url": f"https://placehold.co/200x150?text={caption_prefix}+{idx+1}",
                    "caption": filename,
                    "acquired_on": session.get("date"),
                }
            )
        imaging_sections[key]["metadata"].append(
            {
                "instrument": label,
                "magnification": session.get("settings", "—"),
                "operator": session.get("operator", "—"),
                "acquired_on": session.get("date", "—"),
                "notes": session.get("status", ""),
            }
        )
    if imaging.get("next_steps"):
        imaging_sections["other"]["metadata"].append(
            {
                "instrument": "Planned work",
                "magnification": "—",
                "operator": "Queue",
                "acquired_on": "—",
                "notes": imaging["next_steps"],
            }
        )
    return imaging_sections


def _detect_geochem_section(label):
    text = (label or "").upper()
    if "MICRO" in text and "XRF" in text:
        return "micro_xrf"
    if "XRF" in text:
        return "whole_xrf"
    if "LA" in text and "ICP" in text:
        return "la_icp_ms"
    if "ICP" in text:
        return "icp_ms"
    if "EPMA" in text or "SEM" in text:
        return "epma"
    if "SIMS" in text:
        return "sims"
    if "AGE" in text or "U-" in text:
        return "geochronology"
    return "geochronology"


def _build_geochem_sections(sample):
    section_keys = [
        "micro_xrf",
        "whole_xrf",
        "icp_ms",
        "epma",
        "la_icp_ms",
        "sims",
        "geochronology",
    ]
    sections = {key: [] for key in section_keys}
    geochem = sample.get("geochemistry") or {}
    processed = geochem.get("processed_uploads", []) or []
    raw_uploads = geochem.get("raw_uploads", []) or []

    for filename in processed:
        key = _detect_geochem_section(filename)
        base_value = 70 + sample.get("id", 0)
        sections[key].append(
            {
                "element": "SiO₂",
                "value": f"{base_value + 0.8:.2f}",
                "unit": "wt%",
                "uncertainty": "±0.45",
                "qc_flag": "pass",
                "notes": f"Derived from {filename}",
            }
        )
        sections[key].append(
            {
                "element": "FeO*",
                "value": f"{7 + sample.get('id', 0) * 0.4:.2f}",
                "unit": "wt%",
                "uncertainty": "±0.15",
                "qc_flag": "pass",
                "notes": "QC verified against internal standards",
            }
        )

    for filename in raw_uploads:
        key = _detect_geochem_section(filename)
        sections[key].append(
            {
                "element": "Dataset",
                "value": "Pending reduction",
                "unit": "—",
                "uncertainty": "—",
                "qc_flag": "pending",
                "notes": f"Awaiting processing of {filename}",
            }
        )

    if geochem.get("reference_standards"):
        sections["geochronology"].append(
            {
                "element": "Reference standards",
                "value": ", ".join(geochem["reference_standards"]),
                "unit": "",
                "uncertainty": "—",
                "qc_flag": "pass",
                "notes": "Standards tracked for drift monitoring",
            }
        )

    return sections


def _build_analyses(sample):
    analyses = []
    collectors = sample.get("collected_by") or []
    primary = collectors[0] if collectors else ALLOWED_PEOPLE[0]

    processing = sample.get("processing") or {}
    # if processing.get("mass_entries"):
    #     status = "completed" if processing.get("derived_metrics") else "in progress"
    #     analyses.append(
    #         {
    #             "type": "Particle Size Workflow",
    #             "instrument": "Sieving & balance station",
    #             "analysis_date": sample.get("collected_on_display", "—"),
    #             "analyst": {"full_name": primary},
    #             "status": status,
    #             "url": "#",
    #             "edit_url": "#",
    #         }
    #     )

    # for session in sample.get("imaging", {}).get("sessions", []) or []:
    #     analyses.append(
    #         {
    #             "type": f"Imaging · {session.get('instrument', 'Session')}",
    #             "instrument": session.get("instrument"),
    #             "analysis_date": session.get("date", "—"),
    #             "analyst": {"full_name": session.get("operator", "—")},
    #             "status": session.get("status", "pending").lower(),
    #             "url": "#",
    #             "edit_url": "#",
    #         }
    #     )

    geochem = sample.get("geochemistry") or {}
    if geochem.get("processed_uploads"):
        qa_member = ALLOWED_PEOPLE[(sample.get("id", 0) + 1) % len(ALLOWED_PEOPLE)]
        analyses.append(
            {
                "type": "Geochemical Reduction",
                "instrument": "Batch pipeline",
                "analysis_date": sample.get("collected_on_display", "—"),
                "analyst": {"full_name": qa_member},
                "status": "completed",
                "url": "#",
                "edit_url": "#",
            }
        )

    return analyses


def _build_attachments(sample):
    attachments = []
    source = sample.get("attachments") or {}
    uploaded_on = sample.get("collected_on_display", "—")
    collector_list = sample.get("collected_by") or []
    uploader = collector_list[0] if collector_list else ALLOWED_PEOPLE[0]

    for image in source.get("images", []) or []:
        attachments.append(
            {
                "filename": image.get("filename"),
                "type": "image",
                "download_url": "#",
                "uploader": {"full_name": uploader},
                "uploaded_on": uploaded_on,
                "description": image.get("caption", ""),
            }
        )

    for idx, note in enumerate(source.get("notes", []) or [], start=1):
        attachments.append(
            {
                "filename": f"FieldNote_{idx}.txt",
                "type": "note",
                "download_url": "#",
                "uploader": {"full_name": uploader},
                "uploaded_on": uploaded_on,
                "description": note,
            }
        )

    for log in source.get("instrument_logs", []) or []:
        attachments.append(
            {
                "filename": f"{log.get('instrument', 'instrument')}_log.txt",
                "type": "log",
                "download_url": "#",
                "uploader": {"full_name": uploader},
                "uploaded_on": uploaded_on,
                "description": log.get("detail", ""),
            }
        )

    return attachments


def _summarize_attachments(attachments):
    summary = {"total": len(attachments), "image": 0, "note": 0, "log": 0, "other": 0}
    for record in attachments:
        key = (record.get("type") or "other").lower()
        if key not in summary:
            summary[key] = 0
        summary[key] += 1
    return summary


def _build_audit_log(sample):
    events = []
    collectors = sample.get("collected_by") or []
    primary = collectors[0] if collectors else ALLOWED_PEOPLE[0]
    collected_on = sample.get("collected_on") if isinstance(sample.get("collected_on"), date) else None
    qa_member = ALLOWED_PEOPLE[(sample.get("id", 0) + 1) % len(ALLOWED_PEOPLE)]
    reviewer = ALLOWED_PEOPLE[(sample.get("id", 0) + 2) % len(ALLOWED_PEOPLE)]

    if collected_on:
        events.append(
            {
                "timestamp": collected_on.strftime("%Y-%m-%d 08:15"),
                "relative_time": _relative_time(collected_on),
                "user": {"full_name": primary},
                "event_type": "metadata",
                "summary": "Collection record created.",
                "details": f"Field team: {', '.join(collectors)}",
            }
        )

    processing = sample.get("processing") or {}
    if processing.get("derived_metrics"):
        processed_on = collected_on + timedelta(days=5) if collected_on else date.today()
        events.append(
            {
                "timestamp": processed_on.strftime("%Y-%m-%d 16:45"),
                "relative_time": _relative_time(processed_on),
                "user": {"full_name": primary},
                "event_type": "analysis",
                "summary": "Processing mass recovery calculated.",
                "details": f"Mass recovery {processing['derived_metrics']['mass_recovery_percent']}%.",
            }
        )

    geochem = sample.get("geochemistry") or {}
    if geochem.get("processed_uploads"):
        geochem_on = collected_on + timedelta(days=14) if collected_on else date.today()
        events.append(
            {
                "timestamp": geochem_on.strftime("%Y-%m-%d 10:05"),
                "relative_time": _relative_time(geochem_on),
                "user": {"full_name": qa_member},
                "event_type": "analysis",
                "summary": f"Processed geochemistry uploaded ({len(geochem['processed_uploads'])} files).",
                "details": ", ".join(geochem["processed_uploads"]),
            }
        )

    if sample.get("is_flagged_for_review"):
        review_on = collected_on + timedelta(days=20) if collected_on else date.today()
        events.append(
            {
                "timestamp": review_on.strftime("%Y-%m-%d 09:10"),
                "relative_time": _relative_time(review_on),
                "user": {"full_name": reviewer},
                "event_type": "status",
                "summary": "Sample flagged for review.",
                "details": "Outstanding metadata items require attention.",
            }
        )

    if not events:
        today = date.today()
        events.append(
            {
                "timestamp": today.strftime("%Y-%m-%d 08:00"),
                "relative_time": "today",
                "user": {"full_name": primary},
                "event_type": "metadata",
                "summary": "Record initialized.",
                "details": None,
            }
        )

    return events


def format_sample(sample):
    formatted = deepcopy(sample)
    collected_on = formatted.get("collected_on")
    if isinstance(collected_on, date):
        formatted["collected_on_display"] = collected_on.strftime("%Y-%m-%d")
    else:
        formatted["collected_on_display"] = "Unknown"

    formatted["projects"] = [
        {
            "project": project_lookup.get(link.get("project_id")),
            "role": link.get("role"),
        }
        for link in formatted.get("associated_projects", [])
        if link.get("project_id") in project_lookup
    ]
    formatted["project"] = formatted["projects"][0]["project"] if formatted["projects"] else None

    formatted["name"] = formatted.get("nickname") or formatted.get("sample_code", "Sample")
    site = formatted.get("site") or {}
    location_parts = [site.get("site_name"), site.get("station"), site.get("stratum")]
    if any(location_parts):
        formatted["location"] = {"summary": ", ".join(part for part in location_parts if part)}
        formatted["location_name"] = formatted["location"]["summary"]
    else:
        formatted["location"] = {}
    formatted["description"] = formatted.get("description") or site.get("depositional_context") or "No description provided"
    formatted["igsn"] = formatted.get("igsn") or f"IGSN:{formatted.get('sample_code', '').replace('-', '')}"
    formatted["storage_location"] = formatted.get("storage_location") or "Not tracked"
    formatted["status"] = formatted.get("status", "active")

    formatted["analyses"] = _build_analyses(formatted)
    formatted["linked_people"] = _build_linked_people(formatted)
    formatted["related_samples"] = _build_related_samples(formatted)
    formatted["qc_flags"] = _build_qc_flags(formatted.get("metadata_flags"))
    formatted["physical_analysis"] = _build_physical_sections(formatted)
    formatted["physical_microanalysis"] = _build_micro_sections(formatted)
    formatted["geochemical_analysis"] = _build_geochem_sections(formatted)

    attachments_list = _build_attachments(formatted)
    formatted["attachments_list"] = attachments_list
    formatted["attachment_summary"] = _summarize_attachments(attachments_list)

    formatted["audit_log"] = _build_audit_log(formatted)
    formatted["placeholder_image_url"] = formatted.get("placeholder_image_url") or "https://placehold.co/200x150?text=CULS"
    formatted["edit_url"] = formatted.get("edit_url") or "#"
    formatted["add_analysis_url"] = formatted.get("add_analysis_url") or "#"

    parent_sample = formatted.get("parent_sample")
    if isinstance(parent_sample, str):
        formatted["parent_sample"] = {"sample_code": parent_sample}
    formatted["is_flagged_for_review"] = formatted.get("is_flagged_for_review") or any(
        flag.get("severity") == "high" for flag in formatted["qc_flags"]
    )

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
    metadata_flags = formatted.get("metadata_flags", [])
    can_edit_sample = formatted["status"].lower() != "archived" and "legacy" not in metadata_flags
    can_manage_analysis = formatted["status"].lower() != "archived"
    can_create_subsample = formatted["status"].lower() == "active"
    can_flag_samples = True
    return render_template(
        "samples/sample_view.html",
        title=f"{formatted['sample_code']} · Sample View",
        sample=formatted,
        can_edit_sample=can_edit_sample,
        can_manage_analysis=can_manage_analysis,
        can_create_subsample=can_create_subsample,
        can_flag_samples=can_flag_samples,
    )
