FROM python:3.8-alpine

ENV PATH="/scripts:${PATH}"

COPY ./django/requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN apk add libffi-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /django
COPY ./django /django
WORKDIR /django

# If need restart DB sqlite
#RUN rm -f ./django/db.sqlite3

# Create if not exist sqlite3 database
RUN if [ ! -f /django/db.sqlite3 ]; then \
    cp /django/db.sqlite3.example /django/db.sqlite3; \
fi

COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user

CMD ["entrypoint.sh"]
