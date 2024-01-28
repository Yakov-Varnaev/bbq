# Application definition

APPS = [
    "app",
    "a12n",
    "users",
    "companies",
    "purchases",
]

THIRD_PARTY_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_jwt.blacklist",
    "djoser",
    "django_filters",
    "axes",
]

INSTALLED_APPS = APPS + THIRD_PARTY_APPS
