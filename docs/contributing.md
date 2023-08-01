# Contributing

## Environment Setup

1. Install [hatch](https://hatch.pypa.io/latest/)
    ```shell
    pipx install hatch
    ```
2. Build the Virtual Environment
    ```shell
    hatch env create
    ```
3. `(Optional)` Link hatch's virtual environment to your IDE:
    ```shell
    echo "$(hatch env find default)/bin/python"
    ```
4. Activate the Virtual Environment
    ```shell
    hatch shell
    ```

## Running the Application

### Run via Python

```shell
uvicorn zoo.app:app \
   --reload \
   --workers 1 \
   --host 0.0.0.0 \
   --port 8000
```

### Run via Docker

```shell
docker compose up --build
```
