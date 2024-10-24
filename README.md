# libgen-scraper

## Introduction

The `libgen-scraper` project is a Django-based application designed to facilitate the scraping and management of book data. It uses Celery for task management and Redis as a message broker and result backend.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Getting Started with Docker](#getting-started-with-docker)

## Installation

### Requirements

- Python 3.9+
- Django 4.2
- Redis
- Docker 

### Setup

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/CodeSymphonyy/libgen-scraper.git
cd libgen-scraper
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Docker Setup

To run the application using Docker, ensure you have Docker and Docker Compose installed, then run:

```bash
docker-compose up --build
```

This command builds the Docker images and starts the services specified in `docker-compose.yml`.

## Usage


To access the Django admin interface, type `http://127.0.0.1:8000/` in your web browser after starting the server.
## Getting Started with Docker

### Prerequisites
Ensure you have Docker and Docker Compose installed on your machine. See [Docker's official documentation](https://docs.docker.com/get-docker/) for installation instructions.

### Running the Application
To start the application, run the following command in the root of the project directory:

```bash
docker-compose up --build
```

## Features

- **Scraping Interface**: Provides an admin interface to initiate and monitor scraping tasks.
- **Task Management**: Utilizes Celery for handling asynchronous task execution.
- **Data Management**: Provide download link for scraped data, and you can navigate through the latest search results in admin interface.

## Dependencies

List of main libraries and frameworks used:

- Django==4.2
- Celery
- Redis
- BeautifulSoup4
- Requests
- Flower for Celery monitoring

## Configuration

To configure the project for local development and production environments, follow these steps:

### Setting Up Configuration Files

1. **Local Settings**:
   - A sample configuration file `sample_settings.py` is provided as a template.
   - Copy `sample_settings.py` to `local_settings.py` and modify it according to your local environment.
   - This file should not be committed to version control as it contains settings specific to your environment.

2. **Environment Variables**:
   - A sample environment file `.env.sample` is provided.
   - Copy `.env.sample` to `.env` and adjust the variables to suit your deployment needs.
   - The `.env` file will contain sensitive information such as database configurations and secret keys, hence it should also not be committed to your version control system.

### Creating a Superuser for Admin Access

To access the admin interface, you need to create a superuser. Run the following command in your terminal:

```bash
python manage.py createsuperuser
```

Follow the prompts to set the username, email, and password for the superuser. Once created, you can log in to the admin panel to manage the application.

## Documentation

For more information on Django settings and structure, see the official Django documentation for version 4.2: https://docs.djangoproject.com/en/4.2/

## Examples

To start a scrape task via Django admin:

1. Navigate to the admin dashboard.
2. Go to Search Queries.
3. Add a new query and save to automatically initiate the scraping process.
4. Refresh the web page after some time to see the results. 

To monitor Celery workers and tasks, use the Flower dashboard accessible at:
[http://localhost:5555/](http://localhost:5555/)

## Troubleshooting

- **Celery not receiving tasks**: Ensure Redis service is up and running and that the Celery worker is correctly configured to listen to the right Redis instance.
- **Static files not found**: Run `python manage.py collectstatic` to collect static files into the static directory.

## License

This software is proprietary and protected under copyright laws. CodeSymphonyy retains all rights to the software, and it is available for use under the following conditions:

- The software may be used on up to three devices owned by the user.
- The user is not permitted to modify, distribute, or sublicense the software.
- This license does not grant any rights to the source code or to make derivative works.

For the full license terms, please refer to the License Agreement included with the software or contact CodeSymphonyy for more details.
