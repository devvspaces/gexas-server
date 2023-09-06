# Gexas Server

Generate charts for exam results.

## Installation

1. Install requirements

    Create virtual environment and install requirements

    ```bash
    pip install -r requirements.txt
    ```

2. Create .env secret file in the root folder `src`

    ```bash
    cp env.dev .env
    ```

3. Create logs folder

    ```bash
    mkdir logs
    ```

4. Run migrations

    ```bash
    python manage.py migrate
    ```

## Usage

1. Run server

    ```bash
    python manage.py runserver
    ```

2. Make API Post request to `http://localhost:8000/create/`. Provide the `X-API-HEADER` and the csv file to the file field. The make request. This will generate the files required and organize them accordingly. These will return a url to you in the json response. You can use this url to view the processed html page.

    ```bash
    curl -X POST \
        -H "X-API-HEADER: <API_KEY>" \
        -F "file=@<CSV_FILE>" \
        http://localhost:8000/create/
    ```

3. To view the generated html page, go to `http://localhost:8000/<URL_FROM_RESPONSE>`.
