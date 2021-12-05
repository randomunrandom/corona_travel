FROM python:3.9

ENV ASGI_APP="root.app:app"
ENV HOST="0.0.0.0"
ENV PORT="1234"

WORKDIR /corona_travel

RUN pip install poetry
ENV PATH /root/.local/bin:$PATH
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install -r requirements.txt
# RUN pip install fastapi uvicorn git+https://github.com/Corona-Travel/reusable_mongodb_connection.git@main

CMD uvicorn --host $HOST --port $PORT --log-level debug $ASGI_APP
