import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from audioconf.models import Department


class Command(BaseCommand):
    help = 'Импорт данных из CSV-файлов в базу данных'

    def handle(self, *args, **kwargs):

        data_dir = settings.BASE_DIR / 'data'

        self.import_data(data_dir / 'department.csv',
                         Department)

    def import_data(self, file_path, model):
        with open(file_path, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            data = [model(id=row[0], name=row[1])
                    for row in reader]
            model.objects.bulk_create(data)
        self.stdout.write(self.style.SUCCESS('Успешная загрузка '
                                             f'данных из {file_path}'))
