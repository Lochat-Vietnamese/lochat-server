FROM python:3.12

ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /lochat

COPY pyproject.toml poetry.lock .
RUN poetry install --no-interaction --no-ansi --no-root
COPY . .

CMD python manage.py makemigrations app && \
    python manage.py migrate app && \
    daphne -b 0.0.0.0 -p 8080 config.asgi:application
    # python manage.py runserver 8080