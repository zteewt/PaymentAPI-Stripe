FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/


CMD ["bash", "-lc", "\
  mkdir -p $(dirname ${SQLITE_PATH:-/app/data/db.sqlite3}) && \
  python manage.py migrate && \
  if [ \"${CREATE_SUPERUSER:-0}\" = \"1\" ]; then \
    python manage.py createsuperuser --noinput || true; \
  fi && \
  python manage.py runserver 0.0.0.0:${PORT:-8000} \
"]