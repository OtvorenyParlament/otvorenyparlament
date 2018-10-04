"""
Person Admin
"""

from django.contrib import admin

from person.models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('surname', 'forename')
