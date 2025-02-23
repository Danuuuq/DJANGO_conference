```markdown
# PET_PROJECT_conference

Проект представляет собой портал для управления конференциями с использованием АКС (автоматизированной конференц-связи). В проекте используются Docker-контейнеры для запуска базы данных, бэкенда и Nginx для просмотра логов.

## Порядок запуска проекта

### 1. Сборка и запуск контейнеров
Для сборки и запуска всех контейнеров (БД, бэкенд, Nginx) выполните команду:

```bash
sudo docker compose up --build
```

#### 1.1 Пересборка без контейнера с БД
Если вы хотите пересобрать только бэкенд и шлюз (без пересоздания контейнера с БД, чтобы сохранить данные), выполните:

```bash
docker-compose up --build backend gateway
```

#### 1.2 Запуск в фоновом режиме
Для запуска контейнеров в фоновом режиме используйте:

```bash
sudo docker compose up -d
```

### 2. Инициализация базы данных
Эти шаги необходимо выполнить только при первом запуске проекта.

#### 2.0 Создание таблиц и импорт данных
1. Создание таблиц в БД:
   ```bash
   sudo docker compose exec backend python manage.py migrate
   ```

2. Импорт департаментов:
   ```bash
   sudo docker compose exec backend python manage.py import_department
   ```

3. Импорт АКС номеров:
   ```bash
   sudo docker compose exec backend python manage.py import_acs
   ```

4. Импорт сотрудников:
   ```bash
   sudo docker compose exec backend python manage.py import_employees
   ```

#### 2.1 Обновление данных по АКС номерам (временная схема)
1. Выгрузите файл `acs_phone.csv` с АКС сервера из директории: `/home/protei/backup_json`.
2. Добавьте файл `acs_phone.csv` в директорию `portal_project/PET_PROJECT_conference/portal_conf/data` под именем `acs_phone_update.csv`. Формат данных: `id АКС с сервера, новый ПИН`, например:
   ```
   11;9804
   12;3666
   13;6389
   ```
3. Остановите сервер:
   ```bash
   sudo docker compose down
   ```
4. Запустите сервер с пересборкой:
   ```bash
   sudo docker compose up -d --build
   ```
5. Обновите ПИН-коды в базе данных:
   ```bash
   sudo docker compose exec backend python manage.py update_acs
   ```

### 3. Создание суперпользователя
Для создания суперпользователя выполните команду:

```bash
sudo docker compose exec backend python manage.py createsuperuser
```

### 4. Сбор статики для фронта
Соберите статические файлы для фронтенда:

```bash
sudo docker compose exec backend python manage.py collectstatic
```

### 5. Копирование статики в директорию Nginx
Скопируйте собранные статические файлы в директорию Nginx:

```bash
sudo docker compose exec backend cp -r /app/static/. /static
```

### 6. Остановка сервера
Для остановки сервера выполните:

```bash
sudo docker compose down
```

---

Этот проект предоставляет удобный интерфейс для управления конференциями и автоматизированной конференц-связью. Убедитесь, что все шаги выполнены в правильном порядке для успешного запуска системы.
```