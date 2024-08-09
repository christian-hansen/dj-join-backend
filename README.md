# Kanban Backend

## Project Description

This is a learning project for my studies with the Developer Akademie. This projects serves as backend for a kanban board application. The frontend can be found here: https://github.com/christian-hansen/ng-kanban-app.


## Installation and Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/benjaminBennewitz/binge_hub_backend.git
    ```
2. Change to the project directory:
    ```bash
    cd dj-join-backend
    ```
3. Create a virtual environment and install the dependencies:
    ```bash
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```
4. Run the migrations:
    ```bash
    python manage.py makemigrations
    ```
5. Create Superuser
    ```bash
    python manage.py migrate
    ```
6. Start the Django development server:
    ```bash
    python manage.py runserver
    ```
7. Check URLS and Ports:
    ```right port/url
    make sure to use port :8000 for backend otherwhise some links doesnt work
    ```

## License

This project is licensed under the MIT License