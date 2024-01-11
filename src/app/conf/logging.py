LOGGING = {
    "version": 1,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "companies.services.stock.material_type_creator": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
