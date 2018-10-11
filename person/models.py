"""
Person models
"""

from django.db import models
from django.utils.translation import gettext as _, pgettext_lazy as _p


class Person(models.Model):
    """
    Person
    """
    UNKNOWN = 'unknown'
    SLOVAK = 'slovak'
    HUNGARIAN = 'hungarian'
    ROMANI = 'romani'
    RUSYN = 'rusyn'
    RUSSIAN = 'russian'
    CZECH = 'czech'
    UKRAINIAN = 'ukrainian'

    # NATIONALITIES = (
    #     (UNKNOWN, 'Neznáma'),
    #     (SLOVAK, 'Slovenská'),
    #     (HUNGARIAN, 'Maďarská'),
    #     (ROMANI, 'Rómska'),
    #     (RUSYN, 'Rusýnska'),
    #     (RUSSIAN, 'Ruská'),
    #     (CZECH, 'Česká'),
    #     (UKRAINIAN, 'Ukrajinská')
    # )

    NATIONALITIES = (
        (UNKNOWN, _p('woman', 'Unknown')),
        (SLOVAK, _p('woman', 'Slovak')),
        (HUNGARIAN, _p('woman', 'Hungarian')),
        (ROMANI, _p('woman', 'Romani')),
        (RUSYN, _p('woman', 'Rusyn')),
        (RUSSIAN, _p('woman', 'Russian')),
        (CZECH, _p('woman', 'Czech')),
        (UKRAINIAN, _p('woman', 'Ukrainian'))
    )

    title = models.CharField(max_length=64, default='')
    forename = models.CharField(max_length=128, db_index=True)
    surname = models.CharField(max_length=128, db_index=True)
    born = models.DateField(null=True, blank=True)
    residence = models.ForeignKey(
        'geo.Village', on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    nationality = models.CharField(
        max_length=24, db_index=True, choices=NATIONALITIES, default=UNKNOWN)
    photo = models.ImageField(upload_to='member_images/', blank=True, null=True)
    external_photo_url = models.URLField(blank=True, null=True)
    external_id = models.PositiveIntegerField(unique=True)
    external_url = models.URLField()

    def __str__(self):
        return '{} {}'.format(self.forename, self.surname)

    @property
    def full_name(self):
        return '{} {}'.format(self.forename, self.surname)
