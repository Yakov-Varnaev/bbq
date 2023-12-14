from app.conf.environ import env

ALLOWED_HOSTS = ["*", "http://localhost:3000"]  # host validation is not necessary in 2020
CSRF_TRUSTED_ORIGINS = [
    "http://your.app.origin",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True


if env("DEBUG"):
    ABSOLUTE_HOST = "http://localhost:3000"
else:
    ABSOLUTE_HOST = "https://your.app.com"
