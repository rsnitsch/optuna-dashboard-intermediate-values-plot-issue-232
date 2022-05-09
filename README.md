# Minimal bug reproduction code for intermediate value plots issue

This code is intended to reproduce the issue I reported here: https://github.com/optuna/optuna-dashboard/issues/232

## Running the example

To run the example:

    docker run --rm -e POSTGRES_PASSWORD=example -p 127.0.0.1:5555:5432 postgres
    pipenv install
    pipenv run python example.py
    pipenv run optuna-dashboard postgresql://postgres:example@localhost:5555/postgres

## Screenshots of the result

Note how the lines are sometimes broken and circle back to random steps in the past.

Sequential study:

![sequential](screenshots/sequential.png)

Parallel study:

![parallel](screenshots/parallel.png)
