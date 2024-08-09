# Kanban Backend

## Project Description

This is a learning project created as part of my studies with the Developer Akademie. The project serves as the backend for a Kanban board application. The frontend for this application can be found [here](https://github.com/christian-hansen/ng-kanban-app).

## Installation and Setup

1. Clone the Repository:
    ```bash
    git clone https://github.com/christian-hansen/dj-join-backend.git
    cd dj-join-backend
    ```
2. Create a virtual environment and install the dependencies:
    ```bash
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```
3. Apply migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
4. Create a Superuser
    ```bash
    python manage.py createsuperuser
    ```
5. Start the Django development server:
    ```bash
    python manage.py runserver
    ```
6. Check URLS and Ports (Ensure the backend is running on port 8000, as some links may not work otherwise):
    ```bash
    open http://localhost:8000/admin
    ```

## License

This project is licensed under the MIT License