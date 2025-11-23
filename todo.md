- The code must be formatted in accordance with [PEP 8](https://www.python.org/dev/peps/pep-0008/) using the [black](https://black.readthedocs.io/en/stable/) formatter and [pylint](https://pylint.org/) linter to ensure correctness.

- Unit tests using [pytest](https://docs.pytest.org/en/7.2.x/) must be written for the client device code that provide at least 80% code coverage of the client code, as reported by the [coverage](https://coverage.readthedocs.io/) tool.

- The client must have a Continuous Integration (CI) workflow using [GitHub Actions](https://github.com/features/actions) that automatically builds and tests the updated client subsystem every time a pull request is approved and code is merged into the `main` branch.
- Like the other parts, the machine learning client must run within its own Docker container.
- Put all code for this subsystem within the `machine-learning-client` subdirectory of this repository.

### Web app

- The code must also be formatted in accordance with `PEP 8` using the `black` formatter and `pylint` linter to ensure correctness.

- Unit tests using `pytest` and [pytest-flask](https://pytest-flask.readthedocs.io/en/latest/) must be written for the web app code that provide at least 80% code coverage of the server code.

- The web app must have a Continuous Integration / (CI) workflow using [GitHub Actions](https://github.com/features/actions) that automatically builds, tests the updated subsystem every time a pull request is approved and code is merged into the `main` branch.
- Like the other parts, the web app must run within its own Docker container.
- Put all code for this subsystem within the `web-app` subdirectory of this repository.



### Code linting and formatting

A [GitHub Actions workflow script](./.github/workflows/lint.yml) is included in this repository that will automatically run the `pylint` linter and the `black` formatter in both the `web-app` and `machine-learning-client` subdirectories to check the code in every pull request for its adherence to the proper code conventions. If the code does not pass such a check, the pull request must not be approved or merged.

Due to its general-purpose design, and the fact that it checks all code the same way, regardless of whether that code is part of the web app, machine learning client, or other subsystem, **the given workflow script may not be appropriate for all projects**. You are welcome to modify it as necessary to suit your project's needs, as long as the spirit of the check remains the same.

For example, you may need to set up separate linting and formatting jobs for each subsystem and/or set the linter or formatter to ignore certain files or dependencies that are incapable of passing the linter/formatter checks for reasons outside the control of this project's developers, for example by using `pylint`'s `--ignore` or `--ignored-modules` flags or `black`'s `--exclude` flag. It is up to your team to research and implement any such changes.


- two [badges](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge) at the top of the `README.md` file showing the result of the latest build/test workflow of both the machine learning client and web app subsystems.
