FROM python:3.12-alpine AS builder
COPY --from=ghcr.io/astral-sh/uv:0.8.6 /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

RUN apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev

WORKDIR /app

COPY uv.lock pyproject.toml /app/

RUN uv sync --locked --no-dev --no-install-project --no-editable

COPY src/ /app/src/
COPY main.py /app/
COPY gunicorn.conf.py /app/

RUN uv sync --locked --no-dev --no-editable


FROM python:3.12-alpine AS runtime

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

RUN apk add --no-cache \
    ca-certificates \
    openssl \
    libffi \
    curl \
    postgresql-client

WORKDIR /app

RUN addgroup -S app && adduser -S app -G app

COPY --from=builder --chown=app:app /app/.venv/ /app/.venv/
COPY --from=builder --chown=app:app /app/src/ /app/src/
COPY --from=builder --chown=app:app /app/main.py /app/main.py
COPY --from=builder --chown=app:app /app/gunicorn.conf.py /app/gunicorn.conf.py
COPY docker/entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "main:app", "--config=gunicorn.conf.py"]


FROM runtime AS staging

RUN apk add --no-cache make

WORKDIR /app

COPY --from=builder /bin/uv /bin/uv
COPY --from=builder --chown=app:app /app/uv.lock /app/uv.lock
COPY --from=builder --chown=app:app /app/pyproject.toml /app/pyproject.toml

RUN uv sync --locked --dev --no-editable

COPY Makefile /app/

ENTRYPOINT []
CMD ["make", "ci"]
