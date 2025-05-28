# ndc-analytics-app

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![License](https://img.shields.io/github/license/undp-data/ndc-analytics-app)](https://github.com/undp-data/ndc-analytics-app/blob/main/LICENSE)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)

An AI-powered Streamlit web application for analysing Nationally Determined Contributions (NDCs) from the [NDC Registry](https://unfccc.int/NDCREG). The codebase is an open-source
of the original project transferred from Azure DevOps.

> [!WARNING]  
> The application is a work in progress. Some features may be missing or may not work as intended. Feel free to [open an issue](https://github.com/UNDP-Data/ndc-analytics-app/issues).

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [Contact](#contact)

## Introduction 

NDC Analytics App is designed to facilitate the analysis of NDC documents that are routinelly published by parties in the NDC Registry. It provides a user-friendly interface to search across and have AI-powered chat conversations about the contents of NDC documents. The application is written in Python `3.12` using [Streamlit](https://streamlit.io) and [st-undp](https://undp-data.github.io/st-undp/).

## Getting Started

To run the application locally, clone the repository, set up an environment and launch the application.

```shell
# Clone the repository
git clone https://github.com/undp-data/ndc-analytics-app

# Navigate to the project folder
cd ndc-analytics-app

# Create and activate a virtual environment
# See https://docs.python.org/3/library/venv.html#how-venvs-work
python -m venv .venv
source .venv/bin/activate

# Install the dependencies using `Make`
make install

# Create and populate .env (see .env.example)
# Launch the application
make run
```

> [!WARNING]  
> The deployed version of the application connects to a LanceDB instance in a private Azure Blob Storage container. The database contains NDC metadata, text chunks and embeddings and is used for full-text and vector search. If you do not provide credentials to connect to
the Storage, you can use a local LanceDB instance. Either way, you would need to
populate the database with the data. This can be done by following the steps described in [main.ipynb](./main.ipynb).

Once launched, the application will be running at http://localhost:8501.

## Contributing

All contributions must follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). The codebase is formatted with `black` and `isort`. Use the provided [Makefile](Makefile) for formatting and linting your code.

1. Clone or fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes in that branch.
4. Ensure your code is properly formatted (`make format`).
5. Run the linter and check for any issues (`make lint`).
6. Execute the tests (`make test`).
7. Commit your changes (`git commit -m 'Add some feature'`).
8. Push to the branch (`git push origin feature-branch`).
9. Open a pull request to `main` branch.

## Contact

This project was originally developed and maintained by [Data Futures Exchange (DFx)](https://data.undp.org) team at UNDP.
If you are facing any issues or would like to make some suggestions, feel free to
[open an issue](https://github.com/undp-data/ndc-analytics-app/issues/new/choose).
For enquiries about DFx, visit [Contact Us](https://data.undp.org/contact-us).
