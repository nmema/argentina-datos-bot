FROM python:3.8-buster

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /home/app
COPY poetry.lock pyproject.toml argentina-bot /home/app/

# https://github.com/python-poetry/poetry/issues/1227
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

CMD ["poetry", "run", "python", "app.py"]
