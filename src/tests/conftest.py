# fmt: off
pytest_plugins = [
    "tests.asserts.app",
    "tests.factories.app",
    "tests.fixtures.app",

    "tests.factories.apps.a12n",
    "tests.fixtures.apps.a12n",

    "tests.factories.apps.companies",
    "tests.fixtures.apps.companies",
    "tests.asserts.apps.companies",

    "tests.factories.apps.users",
    "tests.fixtures.apps.users",
    "tests.asserts.apps.users",
]
# fmt: on
