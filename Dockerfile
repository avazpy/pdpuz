FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /app

COPY . /app
RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip install -r /app/requirements.txt && pip install gunicorn
EXPOSE 8000
CMD ["python3" , "manage.py" , "runserver" , "0:8000"]
