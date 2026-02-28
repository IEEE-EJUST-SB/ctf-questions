FROM python:3

WORKDIR /usr/src/app

RUN pip install django django-unicorn==0.60.0

COPY . .
COPY flag.txt /tmp/flag.txt

#CMD ["django-admin", "runserver", "--pythonpath=.", "--settings=myproject.settings"]

# --insecure is not the point of the challenge btw
CMD sh -c "cp db.sqlite3 /tmp/db.sqlite3 && ./manage.py runserver 0.0.0.0:1337 --pythonpath=. --settings=myproject.settings --insecure"

