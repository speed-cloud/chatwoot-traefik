FROM python:3.11-alpine
LABEL maintainer="Groupe Speed Cloud <contact@speed-cloud.fr>"
LABEL org.opencontainers.image.source="https://github.com/speed-cloud/chatwoot-traefik"

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:3000", "app:app"]
HEALTHCHECK --interval=15s --retries=5 --start-period=60s --timeout=5s \
  CMD curl -f http://localhost:3000/health