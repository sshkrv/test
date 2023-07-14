# event app

- install requirements
-  python manage.py makemigrations
-  python manage.py migrate
-  python manage.py test
-  python manage.py runserver

you can test all features in swagger - http://localhost:8000/swagger/
or you can go directly to each endpoint, e.g. - http://localhost:8000/events/
in swagger it's necessary to get jwt token first and authorise, make sure you put 'Bearer' before it


python 3.11
