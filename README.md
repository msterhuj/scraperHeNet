# Scraper for he.net

Start docker compose locally before running this script.

In folder run `python -m scraperHeNet`

Retart all chrome instances with `docker-compose restart chrome`

Start worker node `celery -A interdex worker --loglevel=INFO`