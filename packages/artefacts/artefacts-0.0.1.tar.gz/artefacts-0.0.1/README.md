# artefacts

A library for parsing dbt artifacts.

## Development

Create a python virtual environment with python3.6+

```
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
```

Install the dependencies.

```
pip install -r requirements.txt
pip install --editable .
```

Start a postgres database.

```
docker run --name artefacts-postgres \
    -e POSTGRES_PASSWORD=artefacts \
    -e POSTGRES_USER=artefacts \
    -e POSTGRES_DB=artefacts \
    --publish 5434:5432 \
    --detach \
    postgres:13
```

Build the jaffle shop dbt project.

```
dbt seed --project-dir jaffle_shop --profiles-dir $(pwd)
dbt run --project-dir jaffle_shop --profiles-dir $(pwd)
dbt docs generate --project-dir jaffle_shop --profiles-dir $(pwd)
```

Run the test suite.

```
pytest
```

Compile and serve the documentation site at http://127.0.0.1:8000

```
mkdocs serve
```