"""
Geo admin
"""


from django.contrib import admin

from geo.models import District, Region, Village


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):

    pass


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):

    pass


@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):

    list_display = ('district', 'full_name')
    list_select_related = ('district',)
