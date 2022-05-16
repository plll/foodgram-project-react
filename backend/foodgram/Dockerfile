FROM python:3.7-slim
COPY ./ /web
RUN pip install -r /web/requirements.txt
WORKDIR /web/
CMD python manage.py runserver 0:5000
