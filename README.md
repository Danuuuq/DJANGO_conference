# PET_PROJECT_conference
Проект по порталу с АКС конференциями

Порядок запуска:
1. sudo docker compose up --build # Сборки контейнеров с БД, Бэкендом и nginx для просмотра логов
1.1 sudo docker compose up -d # Запуск в фоновом режиме
2. Создания таблиц БД и импорт данных (порядок сохранить как описано ниже):
sudo docker compose exec backend python manage.py migrate # создание таблиц БД
sudo docker compose exec backend python manage.py import_department # Загрузка департаментов
sudo docker compose exec backend python manage.py import_acs # Загрузка АКС номеров
sudo docker compose exec backend python manage.py import_employees # Загрузка сотрудников
3. sudo docker compose exec backend python manage.py createsuperuser # Создание суперадмина
4. sudo docker compose exec backend python manage.py collectstatic # Сбор статики для фронта
5. sudo docker compose exec backend cp -r /app/static/. /static # Копирование её в директорию с nginx
6. sudo docker compose down # Остановить сервер