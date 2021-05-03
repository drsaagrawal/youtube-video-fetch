This project is to frequently update the videos added by youtube

Steps -
docker-compose build
docker-compose run web python manage.py migrate
docker-compose up
