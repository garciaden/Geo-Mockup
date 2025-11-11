# Database Schema Comparison

## Current Database Folder vs FinalNormalization

**Date**: 2025-11-11
**Purpose**: Compare existing SQL scripts with FinalNormalization diagrams

---

##  **Schema Extracted from FinalNormalization Diagrams**

### **Key Differences Identified**

#### **1. USER DOMAIN - More Detailed**

**FinalNormalization has**:

- `user_status` (lookup table) - NEW
- `session_status` (lookup table) - NEW
- `system_role` (lookup table) - UPDATED structure
- `user` table - Links to `person` table
- `user_session` table - NEW (tracks login sessions)

**Current Database has**:

- `culs.user` - Simpler structure
- `culs.system_role` - Basic roles

**ACTION NEEDED**: Add session tracking and status lookup tables

---

#### **2. PERSON DOMAIN - Significantly Expanded**

**FinalNormalization has**:

- `person` table - Core person record
- `organization` table - NEW
- `contact` table - NEW (multiple contacts per person)
- `person_identifier` table - NEW (passports, IDs, etc.)
- `contact_type` lookup - NEW
- `identifier_type` lookup - NEW
- `organization_type` lookup - NEW
- `country` lookup - NEW

**Current Database has**:

- `culs.person` - Basic person table

**ACTION NEEDED**: Major expansion - add organization, contact, and identifier tables

---

#### **3. PROJECT DOMAIN - Similar but Enhanced**

**FinalNormalization has**:

- `project` table - Core project
- `project_user` (junction) - Project memberships with roles
- `project_sample_bridge` (junction) - Links projects to samples
- `project_grant` (junction) - Links projects to grants
- `project_transfer` - Transfer tracking

**Current Database has**:

- `culs.project` - Similar
- `culs.project_user` - Similar
- `culs.project_transfer` - Similar

**ACTION NEEDED**: Add `project_sample_bridge` and `project_grant` tables

---

#### **4. SAMPLE DOMAIN - Needs Full Review**

**FinalNormalization** has detailed sample schema including:

- Sample relationships
- Sample status tracking
- Location tracking
- Sample preparation states

**Current Database**: `culs.sample` exists but needs comparison

**ACTION NEEDED**: Review 30_Sample_Normalization.drawio.xml for complete schema

---

#### **5. ANALYSIS DOMAIN - Needs Full Review**

**FinalNormalization** has separate files for:

- 40_Analysis_Normalization.drawio.xml
- 41_Physical_Analysis_Normalization.drawio.xml
- 42_Microphysical_Normalization.drawio.xml
- 43_Geochemical_Normalization.drawio.xml

**Current Database**: Has `physical_analysis`, `geochem_analysis`, `imaging_analysis`

**ACTION NEEDED**: Detailed comparison required

---

#### **6. INSTRUMENT & CALIBRATION - More Detailed**

**FinalNormalization has**:

- `instrument` table
- `calibration` table - NEW structure
- `reference_material` table - NEW
- `calibration_measurement` table - NEW
- `LookupMaterialType` - NEW
- `LookupMaterialSource` - NEW
- `LookupAnalyte` - NEW
- `LookupUnit` - NEW

**Current Database has**:

- `culs.instrument`
- `culs.instrument_calibration`

**ACTION NEEDED**: Expand calibration tracking with reference materials and measurements

---

#### **7. FILE STORAGE - Needs Review**

**FinalNormalization**: 70_File_Storage_Normalization.drawio.xml

**Current Database**: `files.*` schema exists

**ACTION NEEDED**: Review file storage normalization

---

##  **Detailed Comparison Needed**

The following areas need thorough analysis:

1. **Sample Schema** (30_Sample_Normalization)
2. **Analysis Schemas** (40-43 files)
3. **File Storage** (70 file)
4. **Supporting Tables** (90 file)

---

##  **What We Know So Far**

### **Tables to ADD**:

- `user_status` (lookup)
- `session_status` (lookup)
- `user_session` (session tracking)
- `organization`
- `contact`
- `person_identifier`
- `contact_type` (lookup)
- `identifier_type` (lookup)
- `organization_type` (lookup)
- `country` (lookup)
- `project_sample_bridge` (junction)
- `project_grant` (junction)
- `grant` (if not exists)
- `reference_material`
- `calibration_measurement`
- `LookupMaterialType`
- `LookupMaterialSource`
- `LookupAnalyte`
- `LookupUnit`

### **Tables to UPDATE**:

- `user` - Link to person, update fields
- `person` - Link to organization
- `system_role` - Verify structure
- `instrument` - Verify fields
- `calibration` - Expand structure

### **Tables to REVIEW**:

- All analysis tables (need detailed comparison)
- All sample tables (need detailed comparison)
- File storage tables (need detailed comparison)

---

## ¯ **Recommended Next Steps**

### **Option 1: Full Automated Conversion (Recommended)**

I can create a Python script to parse all Draw.io XML files and generate complete SQL DDL scripts.

**Pros**: Accurate, complete, automated
**Cons**: Takes 2-3 hours to develop

### **Option 2: Manual Review & Update**

You provide specific requirements, and I update SQL scripts incrementally.

**Pros**: Focused on priority changes
**Cons**: May miss some relationships

### **Option 3: Team Member Guidance**

Your team member who created these diagrams provides a summary of key changes.

**Pros**: Fastest, most accurate
**Cons**: Requires team collaboration

---

##  **Questions for You**

1. **Priority**: Which domain is most critical to update first?

   - User/Authentication?
   - Person/Organization?
   - Sample?
   - Analysis?
2. **Scope**: Do you want:

   - Complete database rebuild from FinalNormalization?
   - Incremental updates to existing database?
   - Just fix the most critical gaps?
3. **Timeline**: When do you need this by?

   - This needs to align with Phase 1 of TASK_ASSIGNMENTS (Nov 6-9)
4. **Team Member**: Can they provide a summary document of the key changes they made in the normalization?

---

##  **What I Can Do Right Now**

Tell me which option you prefer:

**A.** Create Python script to parse all Draw.io files and generate complete SQL DDL
**B.** Focus on User/Person/Project domains first (most critical for authentication)
**C.** Wait for team member's change summary document
**D.** Do a detailed manual comparison of specific tables you care about most

I'm ready to proceed once you tell me which approach you prefer!
