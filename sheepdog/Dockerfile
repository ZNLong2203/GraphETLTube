FROM quay.io/cdis/python:python3.9-buster-2.0.0

ENV appname=sheepdog

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libffi-dev musl-dev gcc libxml2-dev libxslt-dev \
    curl bash git vim jq \
    postgresql-client \
    uwsgi-plugin-python3

RUN pip install --upgrade pip poetry
RUN pip install python-levenshtein

RUN mkdir -p /var/www/$appname \
    && mkdir -p /var/www/.cache/Python-Eggs/ \
    && mkdir /run/nginx/ \
    && mkdir -p /var/run/gen3/ \
    && ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log \
    && chown nginx -R /var/www/.cache/Python-Eggs/ \
    && chown nginx /var/www/$appname

EXPOSE 80

WORKDIR /$appname

COPY poetry.lock pyproject.toml /$appname/
RUN poetry config virtualenvs.create false \
    && poetry lock \
    && poetry install -vv --no-root --no-dev --no-interaction \
    && poetry show -v

COPY . /$appname
COPY ./deployment/uwsgi/uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY ./bin/settings.py /var/www/$appname/settings.py
COPY ./bin/confighelper.py /var/www/$appname/confighelper.py
COPY dockerrun.sh /$appname/dockerrun.sh
RUN chmod +x /$appname/dockerrun.sh

RUN ls -al /var/www/$appname

RUN poetry config virtualenvs.create false \
    && poetry install -vv --no-dev --no-interaction \
    && poetry show -v

WORKDIR /var/www/$appname

CMD ["/dockerrun.sh"]
