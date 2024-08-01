from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest


User = get_user_model()


register_test_cases = [
    (
        "testuser1",
        "testuser1@test.com",
        "testpassword123",
        "testpassword123",
        302,
        "login",
    ),
    (
        "testuser2",
        "testuser2@test.com",
        "testpassword123",
        "wrongpassword",
        200,
        None,
    ),
    (
        "testuser3",
        "testuser3.com",
        "testpassword123",
        "wrongpassword",
        200,
        None,
    ),
]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, email, password1, password2, status_code, redirect_url",
    register_test_cases,
)
def test_registration(
    client, username, email, password1, password2, status_code, redirect_url
):
    url = reverse("register")
    data = {
        "username": username,
        "email": email,
        "password1": password1,
        "password2": password2,
    }
    response = client.post(url, data)

    assert response.status_code == status_code

    if status_code == 302:
        assert User.objects.filter(username=username).exists()
        assert response.headers["Location"] == reverse(redirect_url)
    else:
        assert "Location" not in response.headers


login_test_cases = [
    ("testuser", "testpassword123", 302, "index"),
    ("wronguser", "testpassword123", 200, None),
    ("testuser", "wrongpassword", 200, None),
]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, password, status_code, redirect_url", login_test_cases
)
def test_login(client, username, password, status_code, redirect_url):
    if username == "testuser" and status_code == 302:
        User.objects.create_user(
            username="testuser", password="testpassword123"
        )
    url = reverse("login")
    data = {
        "username": username,
        "password": password,
    }
    response = client.post(url, data)
    assert response.status_code == status_code
    if status_code == 302:
        assert response.headers["Location"] == reverse(redirect_url)
    else:
        assert "Location" not in response.headers


logout_test_cases = [
    ("testuser", "testpassword123", 302, "login"),
]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, password, status_code, redirect_url", logout_test_cases
)
def test_logout(client, username, password, status_code, redirect_url):
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    url = reverse("logout")
    response = client.get(url)
    assert response.status_code == status_code
    if status_code == 302:
        assert response.headers["Location"] == reverse(redirect_url)
        assert "_auth_user_id" not in client.session
