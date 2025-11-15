from django.db import models


class PolarizingMicroscope(models.Model):
    """FD26: Microanalysis - polarizing microscope observations."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    image_instrument_id = models.CharField(max_length=100, blank=True)
    sample_mount_id = models.CharField(max_length=100, blank=True)
    type_of_material_analyzed = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'polarizing_microscope'
        verbose_name_plural = 'Polarizing microscope analyses'


class ElectronImagingElementMap(models.Model):
    """FD27: Microanalysis - electron microscopy and element mapping."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    image_instrument_id = models.CharField(max_length=100, blank=True)
    sample_mount_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'electron_imaging_element_map'
        verbose_name_plural = 'Electron imaging element maps'


class Tomography(models.Model):
    """FD28: Microanalysis - X-ray or electron tomography."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    image_instrument_id = models.CharField(max_length=100, blank=True)
    sample_mount_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tomography'
        verbose_name_plural = 'Tomography analyses'


class OtherImagingData(models.Model):
    """FD29: Microanalysis - other imaging techniques."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    image_instrument_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'other_imaging_data'
        verbose_name_plural = 'Other imaging data'


class MicroanalysisImagingData(models.Model):
    """FD30: Microanalysis - imaging instrument settings and parameters."""
    image_instrument_id = models.CharField(max_length=100, primary_key=True)
    analysis = models.ForeignKey('analyses.Analysis', on_delete=models.CASCADE, related_name='imaging_data')
    file_id = models.CharField(max_length=100, blank=True)
    date_of_image_analysis = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'microanalysis_imaging_data'
        verbose_name_plural = 'Microanalysis imaging data'
