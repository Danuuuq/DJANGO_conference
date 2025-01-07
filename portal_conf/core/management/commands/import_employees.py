import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from audioconf.models import Employees, Department


class Command(BaseCommand):
    help = 'Импорт данных из CSV-файлов в базу данных'

    def handle(self, *args, **kwargs):

        data_dir = settings.BASE_DIR / 'data'

        self.import_data(data_dir / 'employees.csv',
                         Employees)

    def import_data(self, file_path, model):
        with open(file_path, encoding='utf-8') as file:
            departments = Department.objects.all()
            reader = csv.reader(file, delimiter=';')
            data = [model(department=departments.get(id=row[0]),
                          last_name=row[1], first_name=row[2],
                          middle_name=row[3], email=row[4])
                    for row in reader]
            model.objects.bulk_create(data)
        self.stdout.write(self.style.SUCCESS('Успешная загрузка '
                                             f'данных из {file_path}'))
