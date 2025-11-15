from django.db import models


class GeochemGeneralAttributes(models.Model):
    """FD31: Geochemical analysis - general metadata."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    technique = models.CharField(max_length=100)
    method_name = models.CharField(max_length=255, blank=True)
    lab_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'geochem_general_attributes'
        verbose_name_plural = 'Geochem general attributes'


class XRF(models.Model):
    """FD32: Geochemical analysis - X-ray fluorescence."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    xrf_instrument_id = models.CharField(max_length=100, blank=True)
    xrf_type = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'xrf'
        verbose_name = 'XRF'
        verbose_name_plural = 'XRF analyses'


class ICPMS(models.Model):
    """FD33: Geochemical analysis - ICP-MS."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    icpms_lab_id = models.CharField(max_length=100, blank=True)
    icpms_type = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'icpms'
        verbose_name = 'ICP-MS'
        verbose_name_plural = 'ICP-MS analyses'


class EPMASEM(models.Model):
    """FD34: Geochemical analysis - EPMA/SEM."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    instrument_type = models.CharField(max_length=50, choices=[('EPMA', 'EPMA'), ('SEM', 'SEM')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'epma_sem'
        verbose_name = 'EPMA/SEM'
        verbose_name_plural = 'EPMA/SEM analyses'


class LAICPMS(models.Model):
    """FD35: Geochemical analysis - LA-ICP-MS."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    lab_location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'la_icpms'
        verbose_name = 'LA-ICP-MS'
        verbose_name_plural = 'LA-ICP-MS analyses'


class SIMS(models.Model):
    """FD36: Geochemical analysis - SIMS."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    sims_lab_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sims'
        verbose_name = 'SIMS'
        verbose_name_plural = 'SIMS analyses'


class Geochronology(models.Model):
    """FD37: Geochemical analysis - age dating."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    gc_lab_name = models.CharField(max_length=255, blank=True)
    dating_method = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'geochronology'
        verbose_name_plural = 'Geochronology analyses'
