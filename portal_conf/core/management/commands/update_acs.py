import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from audioconf.models import AcsPhone, Department


class Command(BaseCommand):
    help = 'Импорт данных из CSV-файлов в базу данных'

    def handle(self, *args, **kwargs):

        data_dir = settings.BASE_DIR / 'data'

        self.import_data(data_dir / 'acs_phone_update.csv',
                         AcsPhone)

    def import_data(self, file_path, model):
        with open(file_path, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                acs_id = row[0]
                password = row[1]
                model.objects.filter(acs_id=acs_id).update(password=password)
                # obj, created = model.objects.update_or_create(
                #     acs_id=acs_id,
                #     defaults={'password': password})
        self.stdout.write(self.style.SUCCESS('Успешное обновление '
                                             f'данных из {file_path}'))
