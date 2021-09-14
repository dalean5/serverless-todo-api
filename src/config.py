import os


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", 5432)
    password = os.environ.get("DB_PASSWORD", "password")
    user = os.environ.get("DB_USER", "user")
    name = os.environ.get("DB_NAME", "todos")

    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = os.environ.get("API_PORT", 7071)

    return f"http://{host}:{port}"
