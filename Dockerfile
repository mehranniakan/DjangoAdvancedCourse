FROM python:3.8-bullseye
ARG app_path=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR ${app_path}
COPY requirements.txt /${app_path}
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y curl
RUN pip install -r requirements.txt
COPY ./core /${app_path}/
EXPOSE 8000
CMD ["python","manage.py", "runserver", "0.0.0.0:8000"]