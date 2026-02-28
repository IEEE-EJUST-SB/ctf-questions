FROM python:3.12-alpine

ADD \
    app/requirements.txt \
    app/__init__.py \
    app/flag.py \
    app/lottery.py \
    app/main.py \
    /app/
ADD \
    app/util/ \
    /app/util/
RUN pip install -r /app/requirements.txt

USER nobody:nobody
WORKDIR /app
CMD ["python", "/app/main.py", "host", "-a", "0.0.0.0", "-p", "1024"]
