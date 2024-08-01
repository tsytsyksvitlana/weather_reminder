FROM python:3.12

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD ["python", "weather_reminder/manage.py", "runserver", "0.0.0.0:8000"]
