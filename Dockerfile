FROM python:3.9

ENV PYTHONPATH="${PYTHONPATH}:/app"

WORKDIR /app

COPY requirements.txt /app/

RUN true \
	&& pip install -r requirements.txt \
	&& rm -rf ~/.cache/pip/*

COPY ./ /app/

EXPOSE 8080

CMD	gunicorn app:app --bind 0.0.0.0:8080 --worker-class aiohttp.GunicornWebWorker --access-logfile - --error-logfile - --log-level debug