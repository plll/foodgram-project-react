from django.core.management.base import BaseCommand

from app.models import Ingredient

import csv

class Command(BaseCommand):
    help = 'Load ingedients'

    def handle(self, *args, **options):
        with open('app/data/ingredients.csv', encoding="utf-8") as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                name, unit = row
                Ingredient.objects.get_or_create(name=name, measurement_unit=unit)
