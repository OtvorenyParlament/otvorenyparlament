"""
Update geo app content. This command imports data from this very
cool repository https://github.com/gunsoft/obce-okresy-kraje-slovenska.
You need to clone it to your local path first to use it.
"""

import json
from django.core.management.base import BaseCommand, CommandError

from geo.models import Region, District, Village


class Command(BaseCommand):

    """
    Have github.com/gunsoft/obce-okresy-kraje-slovenska cloned
    and point the --input-dir into a subdirectory where json files are stored
    """
    help = 'Import Regions, Districts and Villages'

    def add_arguments(self, parser):
        """
        Command arguments. Currently only input directory containing JSON files
        """
        parser.add_argument(
            '--input-dir',
            action='store',
            dest='input_dir',
            help='Input dir containing districts.json, villages.json, regions.json',
            required=True
        )

    def update_regions(self, input_dir):
        """Update Region model"""
        regions = {x.id: x for x in Region.objects.all()}
        json_regions = json.loads(
            open('{}/regions.json'.format(input_dir)).read())
        for region in json_regions:
            if region['id'] not in regions:
                new_region = Region(
                    id=region['id'],
                    name=region['name'],
                    shortcut=region['shortcut']
                )
                new_region.save()

    def update_districts(self, input_dir):
        """UPdate District model"""
        districts = {x.id: x for x in District.objects.all()}
        json_districts = json.loads(
            open('{}/districts.json'.format(input_dir)).read())
        for district in json_districts:
            if district['id'] not in districts:
                new_district = District(
                    id=district['id'],
                    region_id=district['region_id'],
                    name=district['name'],
                    shortcut=district['veh_reg_num']
                )
                new_district.save()

    def update_villages(self, input_dir):
        """Update Village model"""
        villages = {
            '{}_{}'.format(x.full_name, x.district_id): x
            for x in Village.objects.all()
        }
        json_villages = json.loads(
            open('{}/villages.json'.format(input_dir)).read())
        for village in json_villages:
            keystring = '{}_{}'.format(village['fullname'], village['district_id'])
            if keystring not in villages:
                try:
                    obj = Village(
                        id=village['id'],
                        district_id=village['district_id'],
                        full_name=village['fullname'],
                        short_name=village['shortname'],
                    )
                    obj.save()
                    villages[keystring] = obj
                except Exception as exc:
                    raise CommandError(exc)
            else:
                obj = villages[keystring]

    def handle(self, *args, **options):
        input_dir = options['input_dir']

        self.update_regions(input_dir)
        self.update_districts(input_dir)
        self.update_villages(input_dir)
