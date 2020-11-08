# Django Backend Of COMP30022 IT Project

#*Must Run With Linux/MacOS*

## Run directly:
1. pip3 install -r requirement.txt
1. python3 manage.py runserver --settings=ITProjectBackend.settings.prod 0:{port}

## Run with Docker:
1. sh build.sh
2. docker run -d -p 8080:8080 --name itproject-backend itproject-backend
