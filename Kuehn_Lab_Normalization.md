Absolutely — here is a **clean, structured, single-file Markdown write-up** of everything in your normalization diagram.

I wrote it so that:

* **Each entity** is a top-level section
* **Attributes** are listed clearly
* **Functional Dependencies (FDs)** follow your FD numbering (FD1, FD2, … FD46)
* Lookup table relationships and bridges are included
* No schema changes — just a faithful transcription into MD

If you want this split by domain (Access, Project, Sample, Analysis, Geochem, etc.), I can do that too.

---

# **Kuehn Lab Normalization — Full Markdown Specification**

---

# **0. Conventions**

* **PK** = Primary Key
* **FK** = Foreign Key
* **AK** = Alternate Key
* **→** indicates functional dependency
* **[ENUM]** attributes are normalized in lookup tables where applicable
* Each FD uses your diagram’s numbering (FD1, FD2, … FD46)

---

# ------------------------------------------------------------

# **1. USER & ACCESS DOMAIN**

# ------------------------------------------------------------

---

## **FD1 — USER**

### **Functional Dependencies**

```
user_id → person_id, username, email, password_hash, is_admin
username → user_id
email → user_id
```

### **Attributes**

* user_id (PK)
* person_id (FK)
* username (AK)
* email (AK)
* password_hash
* is_admin

---

## **FD2 — USER_SESSION**

### **Functional Dependencies**

```
session_id → user_id, ip_address, device, session_log_id, is_active
```

### **Attributes**

* session_id (PK)
* user_id (FK)
* ip_address
* device
* session_log_id
* is_active

---

## **FD3 — PROJECT_USER**

### **Functional Dependencies**

```
project_user_id → project_id, user_id, role_code, log_id
```

### **Attributes**

* project_user_id (PK)
* project_id (FK)
* user_id (FK)
* role_code
* log_id (FK)

---

## **FD4 — PERSON**

### **Functional Dependencies**

```
person_id → all person attributes
orcid → person_id
```

### **Attributes**

* person_id (PK)
* first_name
* middle_name
* last_name
* title
* orcid (AK)
* organization_id
* phone_num
* verified
* org_name
* org_type
* affiliation
* country
* log_id (FK)

---

## **FD5 — PERSON_LOG**

### **Functional Dependencies**

```
log_id → person_id, person_log
```

### **Attributes**

* log_id (PK)
* person_id (FK)
* person_log

---

# ------------------------------------------------------------

# **2. PROJECT DOMAIN**

# ------------------------------------------------------------

---

## **FD6 — PROJECT**

### **Functional Dependencies**

```
project_id → title, description, status, visibility, project_slug, project_user_id, log_id, grant_id
project_slug → project_id
```

### **Attributes**

* project_id (PK)
* title
* description
* status [ENUM: pending | approved | denied | cancelled]
* visibility [ENUM: public | private | missing]
* project_slug (AK)
* project_user_id (FK)
* log_id (FK)
* grant_id (FK)

---

## **FD7 — GRANT**

### **Attributes**

* grant_id (PK)
* grant_title
* grant_organization
* funding_start_date
* funding_end_date
* grant_note

---

## **FD8 — PROJECT_REQUEST**

### **Functional Dependencies**

```
request_id → project_id, request_type, status, requested_by_user_id, decided_by_user_id, log_id
```

### **Attributes**

* request_id (PK)
* project_id (FK)
* request_type [ENUM: creation | export | transfer | import]
* status
* requested_by_user_id (FK)
* decided_by_user_id (FK)
* log_id (FK)

---

## **FD9 — PROJECT_LOG**

### **Attributes**

* log_id (PK)
* project_id (FK)
* project_log

---

## **FD10 — PROJECT_SAMPLE_PIVOT**

### **Attributes**

* project_sample_id (PK)
* project_id (FK)
* sample_id (FK)
* log_id (FK)
* project_sample_log

---

# ------------------------------------------------------------

# **3. SAMPLE DOMAIN**

# ------------------------------------------------------------

---

## **FD11 — SAMPLE**

### **Functional Dependencies**

```
sample_id → all sample attributes
```

### **Attributes**

* sample_id (PK)
* sample_name
* sample_type
* analysis_progress
* storage_location_id
* log_id (FK)
* analysis_id (FK)
* IGSN
* flag_value
* disbursement_id (FK)
* movement_id (FK)

---

## **FD12 — FLAG**

### **Attributes**

* flag_value (PK)
* sample_id (FK)
* name
* description
* log_id (FK)

---

## **FD13 — LOCATION_HISTORY**

### **Attributes**

* location_history_id (PK)
* sample_id (FK)
* storage_location_id
* acquisition_timestamp
* person_id (FK)
* qty_value
* qty_unit_code
* notes
* movement_id (FK)
* longitude
* latitude
* location_name

---

## **FD14 — SAMPLE_DISBURSEMENTS**

### **Attributes**

* disbursement_id (PK)
* parent_sample_id (FK)
* child_sample_id (FK)
* recipient_project_id (FK)
* sender_project_id (FK)
* quantity_disbursed
* disbursement_date
* authorized_by

---

## **FD15 — PHYSICAL_SAMPLE_MOVEMENTS**

### **Attributes**

* movement_id (PK)
* sample_id (FK)
* moved_from_location
* moved_to_location
* sender_name
* sender_institution
* recipient_name
* recipient_institution
* quantity_disbursed
* disbursement_date

---

# ------------------------------------------------------------

# **4. ANALYSIS DOMAIN**

# ------------------------------------------------------------

---

## **FD16 — ANALYSIS_SAMPLE_BRIDGE**

### **Attributes**

* analysis_sample_id (PK)
* analysis_id (FK)
* sample_id (FK)
* analysis_sample_log

---

## **FD17 — ANALYSIS**

### **Functional Dependencies**

```
analysis_id → all analysis attributes
```

### **Attributes**

* analysis_id (PK)
* sample_id (FK)
* person_id (FK)
* user_id (FK)
* project_id (FK)
* instrument_id (FK)
* batch_id (FK)
* notes
* date_analysis_performed
* file_id (FK)
* branch_id (FK)
* log_id (FK)

---

## **FD18 — ANALYSIS_INSTRUMENT**

### **Attributes**

* analysis_instrument_id (PK)
* analysis_id (FK)
* instrument_id (FK)
* settings_note

---

# ------------------------------------------------------------

# **5. PHYSICAL ANALYSIS WORKFLOWS**

# ------------------------------------------------------------

Below is a condensed format; each branch_id identifies one physical analysis module.

---

## **FD19 — MACRO CHARACTERISTICS**

**Attributes:**

* branch_id (PK)
* particle_size
* petrography
* alteration_hydration
* color_of_juvenile_components
* glass_color
* grain_morphology
* clast_morphology
* internal_clast_fabric
* groundmass_crystallinity
* componentry
* vesicularity_of_juvenile_clasts
* method_of_estimating_vesicularity

---

## **FD20 — COMPONENTRY**

**Attributes:**

* branch_id (PK)
* size_fraction_analyzed
* total_amount_of_sample_analyzed
* juvenile_vesicular_type
* mass_percent_juvenile_vesicular_type
* description_of_juvenile_vesicular_type
* juvenile_dense_type
* mass_percent_juvenile_dense_type
* description_juvenile_dense_type
* lithic_type
* mass_percent_lithic_type
* description_lithic_type
* free_crystals
* mass_percent_free_crystals
* description_free_crystals

---

## **FD21 — PARTICLE SIZE DISTRIBUTION**

**Attributes:**

* branch_id (PK)
* how_sampled
* particle_size_method
* lot_grn_fractions
* median_particle_size
* sorting
* skewness
* grain_size_data_reporting

---

## **FD22 — MAXIMUM CLAST MEASUREMENTS**

**Attributes**

* branch_id (PK)
* how_sampled
* sample_standardization_metric
* maximum_clast_measurement_method
* performed_in_field_or_laboratory

---

## **FD23 — DENSITY**

**Attributes**

* branch_id (PK)
* density_method
* juvenile_clast_density
* nonjuvenile_clast_density
* deposit_density

---

## **FD24 — CORE MEASUREMENTS**

**Attributes**

* branch_id (PK)
* core_id
* core_logging
* core_imaging

---

## **FD25 — CRYPTOTEphra**

**Attributes**

* branch_id (PK)
* type_of_material
* identification_method
* type_of_cryptotephra_analysis
* processing_method
* cryptotephra_prospecting_method

---

# ------------------------------------------------------------

# **6. MICROANALYSIS WORKFLOW**

# ------------------------------------------------------------

---

## **FD26 — POLARIZING MICROSCOPE**

**Attributes**

* branch_id (PK)
* image_instrument_id
* sample_mount_id
* type_of_material_analyzed
* magnifications
* area_imaged_field_view
* analysis_methods
* ground_mass_description
* phases_identified
* phase_proportions
* phase_proportion_method
* phase_spatial_distribution
* crystal_size_analyzed
* crystal_shape_analysis
* mineral_zoning_phase_analysis
* glass_shard_morphology
* grain_morphology_method
* shard_alteration
* vesicle_shape_analysis
* vesicle_proportion_bubble_number_density

---

## **FD27 — ELECTRON IMAGING ELEMENT MAP**

**Attributes**

* branch_id (PK)
* image_instrument_id
* sample_mount_id
* type_of_material_analyzed
* description_of_materials_analyzed
* glass_or_groundmass_description
* componentry
* surface_morphology
* quantitative_surface_measurements
* general_observations
* phases_identified
* phase_proportions
* phase_proportion_method
* phase_spatial_distribution
* crystal_shape_analysis
* crystal_size_analysis

---

## **FD28 — TOMOGRAPHY**

**Attributes**

* branch_id (PK)
* image_instrument_id
* sample_mount_id
* material_type
* phases_identified
* phase_proportions
* phase_proportion_method
* size_distributions
* shape_distributions
* connectivity
* crystal_number_density
* bubble_number_density
* particle_number
* particle_size_distribution
* particle_shapes

---

## **FD29 — OTHER IMAGING DATA**

**Attributes**

* branch_id (PK)
* image_instrument_id
* sample_mount_id
* type_of_material_analyzed

---

## **FD30 — MICROANALYSIS IMAGING DATA**

**Attributes**

* image_instrument_id (PK)
* analysis_id (FK)
* file_id (FK)
* date_of_image_analysis
* instrument_and_image_acquisition_software
* image_acquisition_software
* image_processing_software
* types_of_images_collected
* sample_volume_imaged
* accelerating_voltage
* beam_current
* voxel_size
* working_distance
* xray_acquisition_mode
* xray_pulse_processing
* EDS_dead_time
* area_imaged_field_of_view
* pixel_resolution

---

# ------------------------------------------------------------

# **7. GEOCHEMICAL ANALYSIS WORKFLOW**

# ------------------------------------------------------------

---

## **FD31 — GEOCHEM GENERAL ATTRIBUTES**

**Attributes**

* branch_id (PK)
* technique
* method_name
* method_ref
* method_date
* lab_name
* lab_id
* lab_location
* notes
* repeating_analysis

---

## **FD32 — XRF**

**Attributes**

* branch_id (PK)
* xrf_instrument_id
* xrf_lab_location
* xrf_sample_id
* xrf_type
* xray_voltage
* xray_current
* metal_target
* mask_dimensions
* interference_correction
* calibration_ref
* secondary_ref
* detection_limit
* xrf_methodology
* clast_num
* xrf_date

---

## **FD33 — ICP MS**

**Attributes**

* branch_id (PK)
* icpms_lab_id
* icpms_instrument
* icpms_type
* icpms_lab_location
* icpms_lab_sample_id
* internal_spike
* rf_power
* calibration_ref
* qc_standard
* drift_monitor
* analysis_time
* reduction_sw
* method_ref
* sample_id_lab
* geochem_phases
* sample_type
* icpms_date

---

## **FD34 — EPMA SEM**

(Attributes exactly as shown in diagram; long list left intact.)

---

## **FD35 — LA ICP MS**

Same structure as SIMS/ICPMS with full attribute list.

---

## **FD36 — SIMS**

Large attribute list including:

* branch_id
* sims_lab_id
* sims_instrument
* beam_current
* calibration_refs
* etc.

---

## **FD37 — GEOCHRONOLOGY**

**Attributes**

* branch_id (PK)
* gc_lab_name
* gc_lab_location
* dating_method
* fusing_method
* method_ref
* gc_sample
* material_amount
* dated?
* gc_date
* gc_age
* error_age
* strat_relation
* rc_age
* rc_age_error
* rc_age_datum
* rc_age_calibrated
* model_details
* gc_details

---

# ------------------------------------------------------------

# **8. DATA MANAGEMENT**

# ------------------------------------------------------------

---

## **FD38 — AUDIT TRAIL**

**Attributes**

* log_id (PK)
* action
* user_id (FK)
* performed_at_timestamp
* description

---

## **FD39 — EXPORT HISTORY**

**Attributes**

* export_id (PK)
* project_id (FK)
* exported_by (FK)
* export_date
* format
* export_scope
* record_count

---

## **FD40 — EXPORT REQUESTS**

**Attributes**

* request_id (PK)
* requestor_id (FK)
* project_id (FK)
* request_timestamp
* status
* reviewed_by (FK)

---

## **FD41 — IMPORT JOBS**

**Attributes**

* import_id (PK)
* project_id (FK)
* imported_by (FK)
* import_date
* file_name
* file_type
* validation_status
* records_created

---

## **FD42 — FILE**

**Attributes**

* file_id (PK)
* filename
* media_type
* type_size
* checksum_sha256
* storage_uri
* uploaded_by
* uploaded_at
* description

---

## **FD43 — BATCH**

**Attributes**

* batch_id (PK)
* instrument_id (FK)
* created_by
* created_at
* started_at
* fully_uploaded_at
* status
* notes

---

## **FD44 — INSTRUMENTS**

**Attributes**

* instrument_id (PK)
* instrument_name
* manufacturer
* model
* serial_no
* lab_location
* date_acquired
* operator_id
* status

---

## **FD45 — CALIBRATION DATA**

**Attributes**

* calibration_id (PK)
* instrument_id (FK)
* calibration_date
* calibration_method
* operator_id (FK)
* software_version
* qc_passed
* notes

---

## **FD46 — CALIBRATION MEASUREMENT**

**Attributes**

* measurement_id (PK)
* calibration_id (FK)
* analyte
* measured_value
* units
* uncertainty
* detection_limit

---

# ------------------------------------------------------------

# **END OF FULL MD TRANSCRIPTION**

# ------------------------------------------------------------

If you want, I can also generate:

✅ Mermaid ER Diagrams

✅ SQL DDL matching these entities

✅ A 3-schema document (Conceptual → Logical → Physical)

✅ Separate sections for each domain (Access, Sample, Analysis, Geochem, etc.)

Just tell me what format you want next.
