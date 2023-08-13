# Contributing

## Environment Setup

!!! tip "pipx"

    This documentaion uses [pipx](https://pipxproject.github.io/pipx/) to
    install and manage non-project command line tools like `hatch` and
    `pre-commit`. If you don't already have `pipx` installed, make sure to
    see their [documentation](https://pipxproject.github.io/pipx/installation/).
    If you prefer not to use `pipx`, you can use `pip` instead.

1. Install [hatch](https://hatch.pypa.io/latest/)

    ```shell
    pipx install hatch
    ```

!!! note "pre-commit"

    Hatch will attempt to set up pre-commit hooks for you using
    [pre-commit](https://pre-commit.com/). If you don't already,
    make sure to install pre-commit as well: `pipx install pre-commit`

2. Build the Virtual Environment
    ```shell
    hatch env create
    ```
3. `(Optional)` Link hatch's virtual environment to your IDE.
   It's located in the `.venv` directory at the root of the project.

4. Activate the Virtual Environment
    ```shell
    hatch shell
    ```

## Using Hatch

### Hatch Cheat Sheet

| Command Description               | Command                     | Notes                                                      |
| --------------------------------- | --------------------------- | ---------------------------------------------------------- |
| Run Tests                         | `hatch run cov`             | Runs tests with `pytest` and `coverage`                    |
| Run Formatting                    | `hatch run lint:fmt`        | Runs `black` and `ruff` code formatters                    |
| Run Linting                       | `hatch run lint:all`        | Runs `ruff` and `mypy` linters / type checkers             |
| Generate OpenAPI Spec and Clients | `hatch run gen:all`         |                                                            |
| Update Requirements Lock Files    | `hatch run gen:reqs`        | Updating lock file using `pip-compile`                     |
| Upgrade Dependencies              | `hatch run gen:reqs-update` | Updating lock file using `pip-compile` and `--update` flag |
| Serve the Documentation           | `hatch run docs:serve`      | Serve the documentation using MkDocs                       |
| Run the Application Locally       | `hatch run app:serve`       | Serve the app with uvicorn using a SQLite Database         |
| Run the Application in Docker     | `hatch run app:container`   | Serve the app using a docker compose stack                 |
| Run the `pre-commit` Hooks        | `hatch run lint:precommit`  | Runs the `pre-commit` hooks on all files                   |

### Hatch Explanation

Hatch has a variety of environments, to see them simply ask hatch:

```bash exec="on" result="markdown" source="tabbed-left" tabs="hatch CLI|Output"
hatch env show
```

That above command will tell you that there are five environments that
you can use:

-   `default`
-   `app`
-   `docs`
-   `gen`
-   `lint`

Each of these environments has a set of commands that you can run.
To see the commands for a specific environment, run:

```bash exec="on" result="markdown" source="tabbed-left" tabs="hatch CLI|Output"
hatch env show docs
```

Here we can see that the `default` environment has the following commands:

-   `cov`
-   `cov-report`
-   `test`
-   `test-cov`

The one that we're interested in is `cov`, which will run the tests
for the project.

```bash
hatch run cov
```

Since `cov` is in the default environment, we can run it without
specifying the environment. However to run the `serve` command in the
`docs` environment, we need to specify the environment:

```bash
hatch run docs:serve
```
