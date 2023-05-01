FROM python:3.10.8

ADD ./requirements.txt /webapp/server/requirements.txt

RUN apt-get update \
    && apt-get install -y nginx \
    && mkdir -p /webapp/uwsgi \
    && mkdir -p /webapp/server \
    && pip install uwsgi pip --upgrade \
    && pip install -r /webapp/server/requirements.txt

ADD . /webapp/server
WORKDIR /webapp/server

ENV NGINX_SET_REAL_IP_FROM="172.18.0.0/16"\
    UWSGI_SOCKET="/webapp/uwsgi/webapp.sock"\
    UWSGI_PID="/webapp/uwsgi/webapp.pid"\
    UWSGI_CHDIR="/webapp/server"\
    UWSGI_MODULE="cafe_backend.wsgi"\
    RUNNING_ENV="local"

RUN mv ./conf/run.sh / \
    && chmod 755 /run.sh \
    && mv ./conf/nginx.conf /etc/nginx/nginx.conf \
    && mv ./conf/webapp.conf /etc/nginx/conf.d/webapp.conf \
    && mv ./conf/uwsgi.ini /webapp/uwsgi/uwsgi.ini

EXPOSE 80 443

CMD ["/run.sh"]