FROM python:3.8-slim-buster
ARG app_path=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR ${app_path}
COPY requirements.txt /${app_path}
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY ./core /${app_path}/
EXPOSE 8000
CMD ["python","manage.py", "runserver", "0.0.0.0:8000"]