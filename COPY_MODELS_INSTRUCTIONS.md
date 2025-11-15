# Copy Model Code to Django Apps

You need to copy the model code from `KUEHNLAB_DJANGO_MODELS.md` into each app's `models.py` file.

## Quick Method: Copy & Paste

### Domain 1: accounts (FD1-FD5)

**File**: `django_app/apps/accounts/models.py`

**Copy from** `KUEHNLAB_DJANGO_MODELS.md` lines 15-436:
- Look for "## Domain 1: USER & ACCESS (FD1-FD5)"
- Copy everything from "### Common Imports" through the PersonLog model (ends around line 436)
- Paste into `apps/accounts/models.py` (replacing the default content)

### Domain 2: projects (FD6-FD10)

**File**: `django_app/apps/projects/models.py`

**Copy from** `KUEHNLAB_DJANGO_MODELS.md` lines 438-652:
- Look for "## Domain 2: PROJECT (FD6-FD10)"
- Copy everything including imports and all 5 models
- Paste into `apps/projects/models.py`

### Domain 3: samples (FD11-FD15)

**File**: `django_app/apps/samples/models.py`

**Copy from** `KUEHNLAB_DJANGO_MODELS.md` lines 654-891:
- Look for "## Domain 3: SAMPLE (FD11-FD15)"
- Copy all 5 models
- Paste into `apps/samples/models.py`

### Domain 4: analyses (FD16-FD18)

**File**: `django_app/apps/analyses/models.py`

**Copy from** `KUEHNLAB_DJANGO_MODELS.md` lines 893-1004:
- Look for "## Domain 4: ANALYSIS (FD16-FD18)"
- Copy all 3 models
- Paste into `apps/analyses/models.py`

### Domain 5: physical_analyses (FD19-FD25)

**File**: `django_app/apps/physical_analyses/models.py`

**Copy from** `KUEHNLAB_DJANGO_MODELS.md` lines 1006-1309:
- Look for "## Domain 5: PHYSICAL WORKFLOWS (FD19-FD25)"
- Copy all 7 models
- Paste into `apps/physical_analyses/models.py`

### Domain 6: microanalyses (FD26-FD30)

**File**: `django_app/apps/microanalyses/models.py`

**Copy from** `KUEHNLAB_DJANGO_MODELS.md` lines 1311-1631:
- Look for "## Domain 6: MICROANALYSIS (FD26-FD30)"
- Copy all 5 models
- Paste into `apps/microanalyses/models.py`

### Domain 7: geochemical (FD31-FD37)

**File**: `django_app/apps/geochemical/models.py`

**Copy from** `KUEHNLAB_DJANGO_MODELS.md` lines 1633-2045:
- Look for "## Domain 7: GEOCHEMICAL (FD31-FD37)"
- Copy all 7 models
- Paste into `apps/geochemical/models.py`

### Domain 8: data_management (FD38-FD46)

**File**: `django_app/apps/data_management/models.py`

**Copy from** `KUEHNLAB_DJANGO_MODELS.md` lines 2047-2484:
- Look for "## Domain 8: DATA MANAGEMENT (FD38-FD46)"
- Copy all 9 models
- Paste into `apps/data_management/models.py`

---

## Verification Checklist

After copying, make sure each `models.py` file:
- ✅ Has the imports at the top
- ✅ Has all the models for that domain
- ✅ Ends with a blank line

---

## After Copying All Models

Run this to check for syntax errors:

```bash
cd django_app
python manage.py check
```

**Expected**: `System check identified no issues (0 silenced).`

Then proceed to migrations!
