# Template Service

Welcome to the Template Service project! This service is a Django-based microservice designed to manage and serve customizable templates for various applications. It provides a centralized and efficient way to handle email and push notifications, allowing for dynamic content injection and easy modification of template designs.

## Table of Contents

-  [About](#about)
-  [Features](#features)
-  [Technologies Used](#technologies-used)
-  [Getting Started](#getting-started)
   -  [Prerequisites](#prerequisites)
   -  [Installation](#installation)
   -  [Environment Variables](#environment-variables)
   -  [Database Migrations](#database-migrations)
   -  [Running the Application](#running-the-application)
-  [Project Structure](#project-structure)
-  [Contributing](#contributing)
-  [License](#license)

## About

The Template Service is a backend microservice built with Django that provides a RESTful API for managing and retrieving templates. It's designed to be used by other services that need to send notifications or generate content based on predefined templates. The service supports variable substitution within templates, allowing for personalized and dynamic content generation. Templates can be stored in the database and retrieved via API calls.

## Features

-  **Template Management:** CRUD (Create, Read, Update, Delete) operations for templates.
-  **Variable Substitution:** Support for dynamic content injection using variables within templates.
-  **RESTful API:** Exposes a RESTful API for managing and retrieving templates.
-  **Database Storage:** Stores templates in a relational database (SQLite by default, configurable to PostgreSQL or others).
-  **Version Control:** Basic versioning of templates (future enhancement).
-  **Template Types:** Supports various template types (e.g., email, SMS, HTML).
-  **Logging:** Detailed logging for debugging and monitoring.
-  **Caching:** Integration with Redis for fast data retrieval and reduced database queries.

## Technologies Used

-  **Python:** Programming Language
-  **Django:** Web Framework
-  **Django REST Framework:** For building RESTful APIs
-  **PostgreSQL/SQLite:** Database (configurable via `DATABASE_URL`)
-  **Gunicorn/uWSGI:** (Implicit for production deployment)
-  **Docker/Docker Compose:** (Recommended for local development)

## Getting Started

Follow these instructions to set up and run the Template Service on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:

-  **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/).
-  **pip**: Python package installer (comes with Python).
-  **virtualenv (recommended)**: For isolated Python environments.

   ```bash
   pip install virtualenv
   ```

-  **Docker and Docker Compose (recommended)**: For easily running the service and its dependencies. Download from [docker.com](https://www.docker.com/products/docker-desktop).

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/KhalifahMB/Template_Service.git
cd TemplateService
```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install project dependencies:**

```bash
pip install -r requirements.txt
```

### Environment Variables

The project uses environment variables for configuration. Create a `.env` file in the root directory of the project based on the following sample:

```/dev/null/sample.env#L1-5
SECRET_KEY=your_django_secret_key_here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS="*"
```

-  `SECRET_KEY`: A unique secret key for Django. Generate a strong one.
-  `DEBUG`: Set to `True` for development, `False` for production.
-  `DATABASE_URL`: Connection string for your database (e.g., PostgreSQL, SQLite). Example for PostgreSQL: `postgres://user:password@db:5432/mydatabase` Replace `db` with the service name if using docker-compose.
-  `ALLOWED_HOSTS`: A comma-separated list of strings representing the host/domain names that this Django site can serve. Use `"*"` for development, but restrict this in production.

### Database Migrations

Apply the initial database migrations to set up your database schema:

```bash
python manage.py makemigrations templates
python manage.py migrate
```

If you make changes to your models, remember to run `makemigrations` and `migrate` again. The `templates` argument specifies the app name.

### Running the Application

To run the Template Service locally:

```bash
python manage.py runserver
```

The service will typically be available at `http://127.0.0.1:8000/`.

Alternatively, you can use Docker Compose:

```bash
docker-compose up --build
```

This will build and start the service, including any specified dependencies (e.g., a PostgreSQL database).

## Project Structure

```
.
├── TemplateService/          # Main Django project directory
│   ├── __init__.py
│   ├── asgi.py                # ASGI configuration for asynchronous support
│   ├── settings.py            # Project settings
│   ├── urls.py                # URL configurations
│   ├── wsgi.py                # WSGI configuration for web server deployment
│   └── db.sqlite3             # SQLite Database file
├── dev/                      # Development-related scripts and configurations
├── logs/                     # Application logs directory
├── notification_templates/   # Django app for template management
│   ├── migrations/           # Database migrations for templates
│   ├── __init__.py
│   ├── admin.py              # Django admin configuration for templates
│   ├── apps.py               # App configuration
│   ├── models.py             # Template models
│   ├── serializers.py        # Template serializers for REST API
│   ├── tests.py              # Template tests
│   └── views.py              # Template views for REST API
├── venv/                      # Python virtual environment (ignored by Git)
├── Dockerfile                # Dockerfile for building the service image
├── docker-compose.yml        # Docker Compose file for local development
├── manage.py                 # Django's command-line utility for administrative tasks
├── requirements.txt          # Python dependency list
├── README.md                 # Project README file
```

## Contributing

We welcome contributions to the Template Service! To contribute, please follow these guidelines.

### How to Contribute

1. **Fork the Repository:**
   Go to the GitHub page of this repository and click the "Fork" button. This will create a copy of the repository under your GitHub account.

2. **Clone Your Fork:**
   Clone your forked repository to your local machine:

   ```bash
   git clone https://github.com/your-username/TemplateService.git
   cd TemplateService
   ```

   Replace `your-username` with your actual GitHub username.

3. **Set Up Your Development Environment:**
   Ensure you have followed the [Prerequisites](#prerequisites), [Installation](#installation), and [Environment Variables](#environment-variables) steps to get the project running locally.

4. **Create a New Branch:**
   Before making any changes, create a new branch for your feature or bug fix:

   ```bash
   git checkout -b feature/your-feature-name
   # Or for a bugfix
   git checkout -b bugfix/issue-description
   ```

   Choose a descriptive name for your branch.

5. **Make Your Changes:**
   Implement your feature or fix the bug. Ensure your code adheres to the project's coding standards and includes necessary comments.

6. **Run Database Migrations (if applicable):**
   If your changes involve modifying models, create and apply migrations:

   ```bash
   python manage.py makemigrations templates
   python manage.py migrate
   ```

7. **Write and Run Tests:**
   Write comprehensive tests for your new features or bug fixes. Ensure all existing tests pass as well:

   ```bash
   python manage.py test notification_templates
   ```

8. **Commit Your Changes:**
   Commit your changes with a clear, concise, and descriptive commit message. We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.
   Examples:

   -  `feat: Add support for SMS templates`
   -  `fix: Resolve issue with variable substitution in HTML templates`
   -  `docs: Update contribution guide`
   -  `refactor: Improve template caching logic`

   ```bash
   git commit -m "feat: Your descriptive commit message"
   ```

9. **Push Your Branch:**
   Push your local branch to your forked repository on GitHub:

   ```bash
   git push origin feature/your-feature-name
   ```

10.   **Open a Pull Request (PR):**
      Go to the original repository on GitHub and you will see a prompt to open a Pull Request from your recently pushed branch.
      -  Provide a detailed description of your changes.
      -  Reference any related issues (e.g., `Closes #123`).
      -  Explain the problem your PR solves and how it solves it.
      -  Include screenshots or GIFs if your changes involve UI aspects.

### Contribution Guidelines

-  **Code Style:** Adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
-  **Documentation:** Document your code where necessary, especially for complex functions or new modules. Update the README or other relevant documentation if your changes impact the project setup or usage.
-  **Tests:** All new features and bug fixes must be accompanied by appropriate tests.
-  **Review Process:** Be responsive to feedback during the code review process. We might ask for changes or clarifications.
-  **Single Responsibility:** Keep pull requests focused on a single feature or bug fix to make reviews easier.

## License

This project is licensed under the MIT License
