# PET_PROJECT_conference
Проект по порталу с АКС конференциями

Порядок запуска:
1. sudo docker compose up --build # Сборки контейнеров с БД, Бэкендом и nginx для просмотра логов
1.1 sudo docker compose up -d # Запуск в фоновом режиме
2.0 Создания таблиц БД и импорт данных (порядок сохранить как описано ниже) Выполнять только при первоначальном запуске проекта:
sudo docker compose exec backend python manage.py migrate # создание таблиц БД
sudo docker compose exec backend python manage.py import_department # Загрузка департаментов
sudo docker compose exec backend python manage.py import_acs # Загрузка АКС номеров
sudo docker compose exec backend python manage.py import_employees # Загрузка сотрудников
2.1 Обновление данных по АКС номерам (временная схема):
выгрузить файл acs_phone.csv с АКС сервера из директории: /home/protei/backup_json
добавить файл acs_phone.csv в portal_project/PET_PROJECT_conference/portal_conf/data
формат данных id АКС с сервера, новый ПИН:
11;9804
12;3666
13;6389
sudo docker compose down - остановка сервера
sudo docker compose up -d --build - запуск сервера, в него добавится новый файл с пинкодами
sudo docker compose exec backend python manage.py update_acs - обновление ПИН-кодов в базе данных
3. sudo docker compose exec backend python manage.py createsuperuser # Создание суперадмина
4. sudo docker compose exec backend python manage.py collectstatic # Сбор статики для фронта
5. sudo docker compose exec backend cp -r /app/static/. /static # Копирование её в директорию с nginx
6. sudo docker compose down # Остановить сервер
