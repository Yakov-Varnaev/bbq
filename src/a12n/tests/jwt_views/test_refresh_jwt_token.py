import pytest

from freezegun import freeze_time
from rest_framework_simplejwt.tokens import RefreshToken  # type: ignore

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.freeze_time("2049-01-05"),
]


@pytest.fixture
def refresh_token(as_user):
    def _refresh_token(token, expected_status=200):
        return as_user.post(
            "/api/v1/auth/jwt/refresh/",
            {
                "refresh": token,
            },
            format="json",
            expected_status=expected_status,
        )

    return _refresh_token


@pytest.fixture
def initial_token(as_user):
    return str(RefreshToken.for_user(as_user.user))


def test_refresh_token_ok(initial_token, refresh_token):
    result = refresh_token(initial_token)

    assert "access" in result


def test_refreshed_token_is_a_token(initial_token, refresh_token):
    result = refresh_token(initial_token)

    assert len(result["access"]) > 32


def test_refreshed_token_is_new_one(initial_token, refresh_token):
    result = refresh_token(initial_token)

    assert result["access"] != initial_token


def test_refresh_token_fails_with_incorrect_previous_token(refresh_token):
    result = refresh_token("some-invalid-previous-token", expected_status=401)

    assert "detail" in result


def test_token_is_not_allowed_to_refresh_if_expired(initial_token, refresh_token):
    with freeze_time("2049-02-05"):
        result = refresh_token(initial_token, expected_status=401)

    assert "detail" in result


def test_received_token_works(as_anon, refresh_token, initial_token):
    token = refresh_token(initial_token)["access"]
    as_anon.credentials(HTTP_AUTHORIZATION=f"JWT {token}")

    result = as_anon.get("/api/v1/users/me/")

    assert result is not None
