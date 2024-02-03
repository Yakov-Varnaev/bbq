from app.conf.boilerplate import BASE_DIR
from app.conf.environ import env

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / env("STATIC_ROOT", cast=str, default="static")
