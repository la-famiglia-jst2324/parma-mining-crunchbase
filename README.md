# parma-mining-crunchbase

[![Chore](https://github.com/la-famiglia-jst2324/parma-mining-crunchbase/actions/workflows/chore.yml/badge.svg?branch=main)](https://github.com/la-famiglia-jst2324/parma-mining-crunchbase/actions/workflows/chore.yml)
[![CI](https://github.com/la-famiglia-jst2324/parma-mining-crunchbase/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/la-famiglia-jst2324/parma-mining-crunchbase/actions/workflows/ci.yml)
[![Deploy](https://github.com/la-famiglia-jst2324/parma-mining-crunchbase/actions/workflows/release.yml/badge.svg)](https://github.com/la-famiglia-jst2324/parma-mining-crunchbase/actions/workflows/release.yml)
[![Major Tag](https://github.com/la-famiglia-jst2324/parma-mining-crunchbase/actions/workflows/tag-major.yml/badge.svg)](https://github.com/la-famiglia-jst2324/parma-mining-crunchbase/actions/workflows/tag-major.yml)

ParmaAI mining module for Crunchbase. This module collects data from Crunchbase by using Apify and provides these data to Parma Analytics.

## Getting Started

The following steps will get you started with the project.

1. Pre-requisites: to be able to contribute to JST in this repository, make sure to comply with the following prerequisites.

   - Configure GitHub via an ssh key. Key based authenticated is highly encouraged. See [GitHub Docs](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh) for more information.
   - Please make sure to have an GPG key configured for GitHub. See [GitHub Docs](https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-gpg-key-to-your-github-account) for more information.
   - Install **micromamba**, a conda environment management package manager, as described [here](https://mamba.readthedocs.io/en/latest/micromamba-installation.html). Alternatively conda or mamba installations should also work, but are highly discouraged because of their slow performance.

2. **Clone the repository**

   ```bash
   git@github.com:la-famiglia-jst2324/parma-mining-crunchbase.git
   ```

3. **Precommit & environment setup**:

   ```bash
   make install  # execute the last 2 steps manually!
   ```

4. **Start the api server**:

   ```bash
   make dev
   ```

   **Open [http://localhost:8000](http://localhost:8000) with your browser to see the result.**

   FastApi will provide you with an interactive documentation of the api. You can also use the swagger ui at [http://localhost:8000/docs](http://localhost:8000/docs) or the redoc ui at [http://localhost:8000/redoc](http://localhost:8000/redoc).

5. Optional: Running the pre-commit pipeline manually

   ```bash
   pre-commit run --all
   ```

6. Test your code:

   ```bash
   make test
   ```

## PR workflow

1. **Create a new branch**
   [linear.app](linear.app) offers a button to copy branch names from tickets.
   In case there is no ticket, please use feel free to use an arbitrary name or create a ticket.
   GitHub CI doesn't care about the branch name, only the PR title matters.

   ```bash
   # format: e.g. robinholzingr/meta-1-create-archtecture-drafts-diagrams-list-of-key-priorities
   git checkout -b <branch-name>
   ```

2. Open a PR and use a [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) PR title.

3. Wait for CI pipeline to pass and if you are happy with your changes request a review.

4. Merge the PR (using the "Squash and merge" option) and delete the branch.
   Pay attention to include co-authors if anyone else contributed to the PR.

5. If you want to release a new version to production, create a new release on GitHub.
   The release version will be automatically derived from the PR titles
   (breaking changes yield new major versions, new features yield new minor versions).

### Directory structure

```bash
.
├── parma_mining.crunchbase: Main sourcing code
│   └── api: FastAPI REST API
│   └── mining_common: Collection of common classes to be used in the repo.
├─ tests: Tests for mining module
├── Makefile: Recipes for easy simplified setup and local development
├── README.md
├── docker-compose.yml: Docker compose file for local database
├── environment.yml: conda environment file
└── pyproject.toml: Python project configuration file
```

## Tech Stack and Dependencies

Core libraries that this project uses:

- [FastAPI](https://fastapi.tiangolo.com/): FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- [Pydantic](https://pydantic-docs.helpmanual.io/): Data validation and settings management using python type annotations.
- [Typer](https://typer.tiangolo.com/): Typer is a library for building CLI applications that users will love using and developers will love creating.
- [Polars](https://pola.rs): Polars is a blazingly fast data processing library written in Rust. It has a DataFrame API that is similar to Pandas and a Series API that is similar to NumPy.
- [Pytest](https://docs.pytest.org/en/6.2.x/): The pytest framework makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries.
- [Python-Jose](https://python-jose.readthedocs.io/en/latest/): The JavaScript Object Signing and Encryption (JOSE) technologies collectively can be used to encrypt and/or sign content using a variety of algorithms.
- [HTTPX](https://www.python-httpx.org/): HTTPX is a fully featured HTTP client for Python 3, which provides sync and async APIs, and support for both HTTP/1.1 and HTTP/2.
- [Apify Client](https://github.com/apify/apify-client-python): The Apify API Client for Python is the official library to access the Apify API from your Python applications. It provides useful features like automatic retries and convenience functions to improve your experience with the Apify API.
- [Google](https://pypi.org/project/google/): The Google module provides the opportunity to perform Google searches with Python.
- [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/): Beautiful Soup is a Python library for pulling data out of HTML and XML files.

## Deployment

The deployment of Parma Mining Modules are managed through a combination of Terraform for infrastructure management and GitHub Actions for continuous integration and delivery. Our deployment strategy ensures that our application is consistently deployed across different environments with high reliability and minimal manual intervention.

### Infrastructure as Code with Terraform

We use Terraform for defining, provisioning, and managing the cloud infrastructure required for Parma Mining Modules. Our Terraform configuration files are organized under the `terraform` directory, divided into different environments like staging (`staging`), and production (`prod`). Each environment has its own set of configurations and variables, ensuring isolation and control over different deployment stages.

A pivotal aspect of our Terraform strategy is the use of a common module, which is housed in the `module` directory. This module encompasses the core infrastructure components that are shared across all environments. The utilization of a shared module ensures consistency and streamlines our infrastructure management.

Each environment, staging and production, references this common `module` but with its own set of environment-specific configurations and variables. This structure ensures that each environment, while based on a common foundation, is independently configurable and isolated, thus providing precise control over the deployment in various stages.

The application is containerized and deployed to **Google Cloud Run**, providing a scalable and serverless environment for running our APIs. This is defined in `service.tf`.

### Continuous Deployment with GitHub Actions

Our GitHub Actions workflow, defined in `.github/workflows/deploy.yml`, automates the deployment process. The workflow is triggered on pushes to the main branch and on published releases. It encompasses steps for:

- Setting up the Google Cloud CLI and authenticating with Google Cloud services.
- Building and pushing Docker images to Google Container Registry.
- Executing Terraform commands (`init`, `plan`, `apply`) to deploy the infrastructure and services as per the Terraform configurations.
- Environment-specific variables and secrets (like database passwords, API keys, etc.) are securely managed through GitHub Secrets and are injected into the deployment process as needed.

### Deployment Environments

We maintain two primary environments for our application:

- Staging (staging): A pre-production environment that closely resembles the production setup, used for final testing before a release.
- Production (prod): The live environment where our application is available to end-users.

## Module Interface

### **Endpoint 1: Initialize**

**Path: `/initialize`**

**Method: GET**

**Description:**
This endpoint initializes the module, that will be done during the handshake with Parma Analytics. It introduces data format to analytics. This process includes registering the measurements which are defined in the normalization map.

**Input:**

- **Type**: integer
- **Content**: Source id of the module

**Output:**

- **Type**: JSON response
- **Content**: Frequency of module and the normalization map of the data format.

### **Endpoint 2: Discovery**

**Path: `/discover`**

**Method: POST**

**Description:**
This endpoint allows clients to search for identifiers based on a query string. It is designed to facilitate the discovery of organizations, domains, channels etc. by keyword. For this module, this endpoint takes name of the company as parameter and returns Crunchbase profile url of the company.

**Input:**

- **Type**: JSON body
- **Content**: A dict containing company ids and names.

**Output:**

- **Type**: JSON response
- **Content**: An object that contains information about an organization/domain/etc. that matches the search query.

### **Endpoint 3: Get Company Details**

**Path: `/companies`**

**Method: POST**

**Description:**
This endpoint retrieves detailed information about a list of companies using their unique IDs and feed the collected raw data to analytics backend.

**Input:**

- **Type**: JSON body
- **Content**: A dictionary of companies and relative handles for these companies.

**Output:**
HTTP status OK

## Disclaimer

In case there are any issues with the initial setup or important architectural decisions/integrations missing, please contact the meta team or @robinholzi directly.
