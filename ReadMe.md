## Проект API для сайта заказов

### Запуск проекта:
**1. скопировать репозиторий командой**  
git clone https://github.com/AndinaZS/ordering 


**2. перейти в папку проекта и установить зависимости**    
    pip install -r requirements.txt


**3. для удобтсва postgres можно запусти через докер**  
docker-compose up  


**4. требуемые переменные окружения:**  
- для настройки отправки писем:  
   EMAIL_USE_TLS  (True)
   EMAIL_HOST  (например, smtp.gmail.com для g-mail)
   EMAIL_FROM  
   EMAIL_BCC - адрес эл.почты для скрытой копии
   EMAIL_HOST_USER и  EMAIL_HOST_PASSWORD - адрес и пароль для аутентификации на smtp сервере
   EMAIL_PORT  порт для smtp-хоста  
   ADMIN_EMAIL
- Джанго:  
SECRET_KEY  
DEBUG 
- База данных (эти данные прописаны в docker-compose):  
DB_NAME='netology_project'  
DB_USER='postgres'  
DB_PASSWORD='postgres' 

**5. выполнить миграции**   
python manage.py makemigrations   
python manage.py migrate   
python manage.py createsuperuser   

**7. создать суперпользователя**   
python manage.py createsuperuser

**6. запустить сервер**   
python3 manage.py runserver


[Примеры запросов Postman](https://documenter.getpostman.com/view/18527099/2s8YmKTk21)


