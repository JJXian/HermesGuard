FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY apps/server /app
RUN pip install .
RUN addgroup --system hermesguard \
    && adduser --system --ingroup hermesguard hermesguard \
    && chown -R hermesguard:hermesguard /app

USER hermesguard

EXPOSE 8000

CMD ["uvicorn", "hermesguard_server.main:app", "--host", "0.0.0.0", "--port", "8000"]
