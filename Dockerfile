FROM python:3.6.0

RUN apt-get update && apt-get -y install vim && rm -rf /var/lib/apt/lists/*

WORKDIR /home/app

ENV PYTHONPATH=/home/app MYSQL_HOST="117.50.19.70" \
    MYSQL_DBNAME="industrial_internet" MYSQL_USER="root" \
    MYSQL_PASSWD="root" MYSQL_PORT="31246"

EXPOSE 10011

COPY . /home/app/

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

CMD ["python3", "app.py","runserver"]
