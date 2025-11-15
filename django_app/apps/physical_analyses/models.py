from django.db import models


class MacroCharacteristics(models.Model):
    """FD19: Physical analysis - macroscopic sample characteristics."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    particle_size = models.CharField(max_length=100, blank=True)
    petrography = models.CharField(max_length=100, blank=True)
    alteration_hydration = models.CharField(max_length=100, blank=True)
    color_of_juvenile_components = models.CharField(max_length=100, blank=True)
    glass_color = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'macro_characteristics'
        verbose_name_plural = 'Macro characteristics'


class Componentry(models.Model):
    """FD20: Physical analysis - componentry breakdown."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    size_fraction_analyzed = models.CharField(max_length=100, blank=True)
    total_amount_of_sample_analyzed = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'componentry'
        verbose_name_plural = 'Componentry analyses'


class ParticleSizeDistribution(models.Model):
    """FD21: Physical analysis - particle size distribution."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    median_particle_size = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    sorting = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'particle_size_distribution'
        verbose_name_plural = 'Particle size distributions'


class MaximumClastMeasurements(models.Model):
    """FD22: Physical analysis - maximum clast size measurements."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    how_sampled = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'maximum_clast_measurements'
        verbose_name_plural = 'Maximum clast measurements'


class Density(models.Model):
    """FD23: Physical analysis - density measurements."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    density_method = models.CharField(max_length=255, blank=True)
    juvenile_clast_density = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'density'
        verbose_name_plural = 'Density measurements'


class CoreMeasurements(models.Model):
    """FD24: Physical analysis - sediment core measurements."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    core_id = models.CharField(max_length=100)
    core_logging = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'core_measurements'
        verbose_name_plural = 'Core measurements'


class Cryptotephra(models.Model):
    """FD25: Physical analysis - cryptotephra identification."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    type_of_material = models.CharField(max_length=100, blank=True)
    identification_method = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cryptotephra'
        verbose_name_plural = 'Cryptotephra analyses'
