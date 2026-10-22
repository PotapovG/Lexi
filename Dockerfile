# No heavyweight model runtime: the web application is Python stdlib only.
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    GREEK_HOST=0.0.0.0 GREEK_PORT=18560 \
    GREEK_DB=/data/progress.sqlite3 GREEK_PEPPER=/data/login-pepper
WORKDIR /app
COPY --chown=10001:10001 *.py *.js *.html *.css *.json *.tsv /app/
COPY --chown=10001:10001 pocket-listening/manifest.json pocket-listening/source.json /app/pocket-listening/
COPY --chown=10001:10001 pocket-pronunciation/manifest.json /app/pocket-pronunciation/
RUN mkdir -p /data /app/pocket-listening/wav /app/pocket-pronunciation/wav \
    && chown -R 10001:10001 /data /app/pocket-listening /app/pocket-pronunciation
USER 10001:10001
EXPOSE 18560
VOLUME ["/data"]
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:18560/health', timeout=3)" || exit 1
CMD ["python","server.py"]
