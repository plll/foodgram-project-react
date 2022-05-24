FROM python:3.7-slim
COPY ./ /web
WORKDIR /web/
RUN pip install -r requirements.txt
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]
RUN python manage.py collectstatic --no-input
