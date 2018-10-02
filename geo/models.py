"""
Geography models
"""

from django.db import models


class Region(models.Model):
    """
    Region
    """
    name = models.CharField(max_length=64, db_index=True)
    shortcut = models.CharField(max_length=2, db_index=True)

    def __str__(self):
        return self.name


class District(models.Model):
    """
    District
    """
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, db_index=True)
    shortcut = models.CharField(max_length=10, db_index=True)

    def __str__(self):
        return self.name


class Village(models.Model):
    """
    Village information
    """
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=64, db_index=True)
    short_name = models.CharField(max_length=64, null=True)

    class Meta:
        unique_together = ('district', 'full_name')

    def __str__(self):
        return self.full_name
