# /bin/bash

python mi_salud_api/manage.py migrate
python mi_salud_api/manage.py runserver 0.0.0.0:8000
