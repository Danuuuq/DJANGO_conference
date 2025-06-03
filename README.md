# 🏢 Conference Booking

**Conference Booking** — это веб-приложение для управления и бронирования конференций, созданное с использованием Django. Система позволяет пользователям просматривать доступные конференции, бронировать участие, а администраторам — управлять мероприятиями и отслеживать регистрацию участников.

### 📌 Основные возможности

* 📋 **Список конференций**: просмотр всех доступных мероприятий с деталями (название, место, дата, описание).
* 📝 **Бронирование**: авторизованные пользователи могут зарегистрироваться на участие в конференции.
* 🔐 **Аутентификация**: регистрация, вход и выход пользователей.
* 🛠 **Админ-панель Django**: управление конференциями, пользователями и бронированиями.
* 📎 **Разделение ролей**: пользователи и администраторы имеют разные уровни доступа.

### ⚙️ Технологии

* **Python 3**
* **Django 4+**
* **SQLite** (по умолчанию)
* HTML/CSS (для базового шаблона интерфейса)

## 🚀 Установка и запуск

### Клонируйте репозиторий:

   ```bash
   git clone https://github.com/Danuuuq/DJANGO_conference.git
   cd DJANGO_conference
   ```

### 1. Сборка и запуск контейнеров
Для сборки и запуска всех контейнеров (БД, бэкенд, Nginx) выполните команду:

```bash
sudo docker compose up --build
```

#### 1.1 Пересборка без контейнера с БД
Если вы хотите пересобрать только бэкенд и шлюз (без пересоздания контейнера с БД, чтобы сохранить данные), выполните:

```bash
sudo docker compose up --build backend gateway
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

#### 2.1 Обновление данных по АКС номерам (интеграция с Протей, временная схема)
1. Выгрузите файл `acs_phone.csv` с АКС сервера из директории: `/home/protei/backup_json`.
2. Добавьте файл `acs_phone.csv` в директорию `portal_project/PET_PROJECT_conference/portal_conf/data` под именем `acs_phone_update.csv`. Формат данных: `id АКС с сервера, новый ПИН`, например:
   ```
   11;9804
   12;3666
   13;6389
   ```  
   Выполнить на АКСС в директории `/home/protei/backup_json`
   ```bash
   scp acs_phone.csv conference@<ip адрес АКС сервера>:/home/conference/portal_project/PET_PROJECT_conference/portal_conf/data/acs_phone_update.csv
   ```  
3. Перейти в дирктори:  
   ```bash
   cd /home/conference/portal_project/PET_PROJECT_conference 
   ```  
3. Остановите сервер в директории:  
   ```bash
   sudo docker compose down
   ```
4. Запустите сервер с пересборкой контейнера backend:  
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

6. Перейдите по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000) для использования приложения.

Панель администратора доступна по адресу [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).

### 🗂 Структура проекта

* `conference/` — основное приложение с моделями, представлениями и шаблонами.
* `templates/` — HTML-шаблоны интерфейса.
* `static/` — статические файлы (CSS, JS, изображения).
* `manage.py` — точка входа в Django-проект.

### 📌 Будущие улучшения

* Расширенная система уведомлений (email)
* Более современный UI с использованием Bootstrap
* Сквозная авторизация через AD
* Выгрузка записей конференций с транскрибацией 

### Как работает автозапуск (работающий сервер):  
 - проверка работы nginx и его запуск:  
```bash
sudo systemctl status nginx 
```  
```bash
sudo systemctl start nginx
```  
 - проверка работы портала и его запуск/перезапуск:  
```bash
sudo systemctl status portal-conf  
```  
```bash
sudo systemctl start portal-conf  
```  
```bash
sudo systemctl restart portal-conf  
```  


#### Что требуется для сквозной авторизации:  
 sudo apt-get install krb5-user libkrb5-dev
 sudo apt-get install nginx-extras
 sudo apt-get update
 sudo apt-get install -y libsasl2-dev python3-dev libldap2-dev libssl-dev libpython3-dev
 pip install --upgrade pip setuptools
 pip install python-ldap
 pip install django-auth-ldap
 python -m pip install python-ldap
 pip list
 python -m pip install setuptools
 sudo apt install slapd ldap-utils
 apt-get install build-essential python3-dev     libldap2-dev libsasl2-dev slapd ldap-utils tox     lcov valgrind
 sudo apt-get install build-essential python3-dev     libldap2-dev libsasl2-dev slapd ldap-utils tox     lcov valgrind
 sudo apt-get install python3-dev libxml2-dev libxslt1-dev zlib1g-dev libsasl2-dev libldap2-dev build-essential libssl-dev libffi-dev libmysqlclient-dev libjpeg-dev libpq-dev libjpeg8-dev liblcms2-dev libblas-dev libatlas-base-dev
 sudo apt install openldap-devel
 python3.10 --version
 sudo apt install python3.10-dev
 pip install django-auth-ldap python-ldap

