cd %~dp0

pip install -r requirements.txt

py manage.py makemigrations
py manage.py migrate

py manage.py createsuperuser