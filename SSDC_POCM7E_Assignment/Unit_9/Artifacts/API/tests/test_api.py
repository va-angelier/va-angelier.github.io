import os
import sys

import pytest

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
)

from app import app, reset_state, seed_default_admin  # noqa: E402

AUTH_HEADERS = {"X-API-Key": "my-secret-api-access-token"}


@pytest.fixture
def client():
    """
    Create a Flask test client and reset in-memory state before each test.
    """
    app.config["TESTING"] = True
    reset_state()

    with app.test_client() as test_client:
        yield test_client


def register_user(
    client,
    username="testuser",
    password="Password123!",
    role="user",
):
    """
    Register a user for reuse across tests.
    """
    return client.post(
        "/api/register",
        json={
            "username": username,
            "password": password,
            "role": role,
        },
    )


def login_user(client, username="testuser", password="Password123!"):
    """
    Log in a user and return the response.
    """
    return client.post(
        "/api/login",
        json={
            "username": username,
            "password": password,
        },
    )


def authenticated_headers(
    client,
    username="testuser",
    password="Password123!",
):
    """
    Return headers containing both API key and session token.
    """
    register_user(client, username=username, password=password)
    login_response = login_user(client, username=username, password=password)
    token = login_response.get_json()["session_token"]

    return {
        "X-API-Key": "my-secret-api-access-token",
        "X-Session-Token": token,
        "X-Username": username,
    }


def admin_headers(client):
    """
    Seed and authenticate the default admin user.
    """
    seed_default_admin()
    login_response = login_user(client, username="admin", password="AdminPass123!")
    token = login_response.get_json()["session_token"]

    return {
        "X-API-Key": "my-secret-api-access-token",
        "X-Session-Token": token,
        "X-Username": "admin",
    }


def create_sample_record(
    client,
    headers,
    name="Test Record",
    description="Test Description",
):
    """
    Create a sample record for reuse across tests.
    """
    return client.post(
        "/api/records",
        json={
            "name": name,
            "description": description,
        },
        headers=headers,
    )


# ------------------------
# USER REGISTRATION TESTS
# ------------------------

def test_register_user_success(client):
    response = register_user(client)

    assert response.status_code == 201
    data = response.get_json()

    assert data["message"] == "User registered successfully."
    assert data["username"] == "testuser"
    assert data["role"] == "user"


def test_register_user_with_duplicate_username_returns_409(client):
    register_user(client)

    response = register_user(client)

    assert response.status_code == 409
    assert response.get_json()["error"] == "Username already exists."


def test_register_user_with_invalid_password_returns_400(client):
    response = register_user(client, password="short")

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "Field 'password' must be a string of at least 8 characters."
    )


def test_register_user_with_invalid_role_returns_400(client):
    response = register_user(client, role="manager")

    assert response.status_code == 400
    assert response.get_json()["error"] == "Field 'role' must be 'user' or 'admin'."


# ------------------------
# LOGIN TESTS
# ------------------------

def test_login_success_returns_session_token(client):
    register_user(client)

    response = login_user(client)

    assert response.status_code == 200
    data = response.get_json()

    assert data["message"] == "Login successful."
    assert data["username"] == "testuser"
    assert data["role"] == "user"
    assert "session_token" in data


def test_login_with_invalid_password_returns_401(client):
    register_user(client)

    response = login_user(client, password="WrongPass123!")

    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid credentials."


def test_login_with_unknown_user_returns_401(client):
    response = login_user(client, username="unknown", password="Password123!")

    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid credentials."


def test_login_lockout_after_repeated_failures_returns_423(client):
    register_user(client)

    for _ in range(5):
        client.post(
            "/api/login",
            json={
                "username": "testuser",
                "password": "WrongPass123!",
            },
        )

    response = client.post(
        "/api/login",
        json={
            "username": "testuser",
            "password": "Password123!",
        },
    )

    assert response.status_code == 423
    assert response.get_json()["error"] == "Account temporarily locked."


# ------------------------
# PROFILE TESTS
# ------------------------

def test_get_profile_success(client):
    headers = authenticated_headers(client)

    response = client.get(
        "/api/profile/testuser",
        headers=headers,
    )

    assert response.status_code == 200
    data = response.get_json()

    assert data["username"] == "testuser"
    assert data["role"] == "user"
    assert "created_at" in data


def test_get_profile_without_session_returns_401(client):
    register_user(client)

    response = client.get("/api/profile/testuser")

    assert response.status_code == 401
    assert response.get_json()["error"] == "Valid session token required."


# ------------------------
# AUTHENTICATION / AUTHORISATION TESTS
# ------------------------

def test_create_record_without_api_key_returns_401(client):
    headers = authenticated_headers(client)
    headers.pop("X-API-Key")

    response = client.post(
        "/api/records",
        json={
            "name": "Record One",
            "description": "First description",
        },
        headers=headers,
    )

    assert response.status_code == 401
    assert response.get_json()["error"] == "Unauthorized"


def test_create_record_without_session_returns_401(client):
    register_user(client)

    response = client.post(
        "/api/records",
        json={
            "name": "Record One",
            "description": "First description",
        },
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 401
    assert response.get_json()["error"] == "Valid session token required."


def test_delete_record_as_non_admin_returns_403(client):
    user_headers = authenticated_headers(client)
    admin_user_headers = admin_headers(client)

    create_sample_record(client, admin_user_headers)

    response = client.delete(
        "/api/records/1",
        headers=user_headers,
    )

    assert response.status_code == 403
    assert response.get_json()["error"] == "Forbidden"


# ------------------------
# CREATE RECORD TESTS
# ------------------------

def test_create_record_success(client):
    headers = authenticated_headers(client)

    response = client.post(
        "/api/records",
        json={
            "name": "Record One",
            "description": "First description",
        },
        headers=headers,
    )

    assert response.status_code == 201

    data = response.get_json()
    assert data["id"] == 1
    assert data["name"] == "Record One"
    assert data["description"] == "First description"
    assert "created_at" in data
    assert "updated_at" in data


def test_create_record_with_missing_name_returns_400(client):
    headers = authenticated_headers(client)

    response = client.post(
        "/api/records",
        json={
            "description": "Missing name",
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Field 'name' is required."


def test_create_record_with_empty_name_returns_400(client):
    headers = authenticated_headers(client)

    response = client.post(
        "/api/records",
        json={
            "name": "   ",
            "description": "Invalid name",
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Field 'name' cannot be empty."


def test_create_record_with_non_string_name_returns_400(client):
    headers = authenticated_headers(client)

    response = client.post(
        "/api/records",
        json={
            "name": 123,
            "description": "Invalid type",
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Field 'name' must be a string."


def test_create_record_with_name_too_long_returns_400(client):
    headers = authenticated_headers(client)

    response = client.post(
        "/api/records",
        json={
            "name": "A" * 101,
            "description": "Too long",
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "Field 'name' must not exceed 100 characters."
    )


def test_create_record_with_non_string_description_returns_400(client):
    headers = authenticated_headers(client)

    response = client.post(
        "/api/records",
        json={
            "name": "Valid Name",
            "description": 999,
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "Field 'description' must be a string."
    )


def test_create_record_with_description_too_long_returns_400(client):
    headers = authenticated_headers(client)

    response = client.post(
        "/api/records",
        json={
            "name": "Valid Name",
            "description": "B" * 501,
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "Field 'description' must not exceed 500 characters."
    )


def test_create_record_with_unexpected_field_returns_400(client):
    headers = authenticated_headers(client)

    response = client.post(
        "/api/records",
        json={
            "name": "Valid Name",
            "description": "Valid Description",
            "admin": True,
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Unexpected field(s): admin."


def test_create_record_with_missing_description_uses_default_empty_string(client):
    headers = authenticated_headers(client)

    response = client.post(
        "/api/records",
        json={
            "name": "Record Without Description",
        },
        headers=headers,
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["description"] == ""


def test_create_record_with_invalid_json_returns_400(client):
    headers = authenticated_headers(client)

    response = client.post(
        "/api/records",
        data="not-json",
        content_type="application/json",
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "Request body must be a valid JSON object."
    )


def test_create_record_with_non_object_json_returns_400(client):
    headers = authenticated_headers(client)

    response = client.post(
        "/api/records",
        json=["not", "an", "object"],
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "Request body must be a valid JSON object."
    )


def test_create_record_with_suspicious_input_returns_400_when_secure_mode_on(
    client,
):
    headers = authenticated_headers(client)

    response = client.post(
        "/api/records",
        json={
            "name": "' OR 1=1 --",
            "description": "Malicious input",
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "Field 'name' contains suspicious input."
    )


# ------------------------
# READ RECORD TESTS
# ------------------------

def test_get_all_records_returns_empty_list_initially(client):
    response = client.get("/api/records")

    assert response.status_code == 200
    assert response.get_json() == []


def test_get_all_records_returns_created_records(client):
    headers = authenticated_headers(client)

    create_sample_record(client, headers, "Record A", "Description A")
    create_sample_record(client, headers, "Record B", "Description B")

    response = client.get("/api/records")

    assert response.status_code == 200
    data = response.get_json()

    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[0]["name"] == "Record A"
    assert data[0]["description"] == "Description A"
    assert data[1]["id"] == 2
    assert data[1]["name"] == "Record B"
    assert data[1]["description"] == "Description B"


def test_get_single_record_success(client):
    headers = authenticated_headers(client)

    create_sample_record(client, headers, "Single Record", "Single Description")

    response = client.get("/api/records/1")

    assert response.status_code == 200
    data = response.get_json()

    assert data["id"] == 1
    assert data["name"] == "Single Record"
    assert data["description"] == "Single Description"


def test_get_single_record_not_found_returns_404(client):
    response = client.get("/api/records/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Record not found."


# ------------------------
# UPDATE RECORD TESTS
# ------------------------

def test_update_record_success(client):
    headers = authenticated_headers(client)

    create_sample_record(client, headers, "Old Name", "Old Description")

    response = client.put(
        "/api/records/1",
        json={
            "name": "New Name",
            "description": "New Description",
        },
        headers=headers,
    )

    assert response.status_code == 200
    data = response.get_json()

    assert data["id"] == 1
    assert data["name"] == "New Name"
    assert data["description"] == "New Description"
    assert "updated_at" in data


def test_update_record_not_found_returns_404(client):
    headers = authenticated_headers(client)

    response = client.put(
        "/api/records/999",
        json={
            "name": "Updated",
            "description": "Updated",
        },
        headers=headers,
    )

    assert response.status_code == 404
    assert response.get_json()["error"] == "Record not found."


def test_update_record_with_missing_name_returns_400(client):
    headers = authenticated_headers(client)

    create_sample_record(client, headers)

    response = client.put(
        "/api/records/1",
        json={
            "description": "Updated only",
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Field 'name' is required."


def test_update_record_with_empty_name_returns_400(client):
    headers = authenticated_headers(client)

    create_sample_record(client, headers)

    response = client.put(
        "/api/records/1",
        json={
            "name": "",
            "description": "Updated",
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Field 'name' cannot be empty."


def test_update_record_with_non_string_name_returns_400(client):
    headers = authenticated_headers(client)

    create_sample_record(client, headers)

    response = client.put(
        "/api/records/1",
        json={
            "name": 456,
            "description": "Updated",
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Field 'name' must be a string."


def test_update_record_with_name_too_long_returns_400(client):
    headers = authenticated_headers(client)

    create_sample_record(client, headers)

    response = client.put(
        "/api/records/1",
        json={
            "name": "A" * 101,
            "description": "Updated",
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "Field 'name' must not exceed 100 characters."
    )


def test_update_record_with_non_string_description_returns_400(client):
    headers = authenticated_headers(client)

    create_sample_record(client, headers)

    response = client.put(
        "/api/records/1",
        json={
            "name": "Updated Name",
            "description": 123,
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "Field 'description' must be a string."
    )


def test_update_record_with_description_too_long_returns_400(client):
    headers = authenticated_headers(client)

    create_sample_record(client, headers)

    response = client.put(
        "/api/records/1",
        json={
            "name": "Updated Name",
            "description": "B" * 501,
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "Field 'description' must not exceed 500 characters."
    )


def test_update_record_with_unexpected_field_returns_400(client):
    headers = authenticated_headers(client)

    create_sample_record(client, headers)

    response = client.put(
        "/api/records/1",
        json={
            "name": "Updated Name",
            "description": "Updated Description",
            "created_at": "hack",
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Unexpected field(s): created_at."


def test_update_record_with_invalid_json_returns_400(client):
    headers = authenticated_headers(client)

    create_sample_record(client, headers)

    response = client.put(
        "/api/records/1",
        data="not-json",
        content_type="application/json",
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "Request body must be a valid JSON object."
    )


def test_update_record_with_non_object_json_returns_400(client):
    headers = authenticated_headers(client)

    create_sample_record(client, headers)

    response = client.put(
        "/api/records/1",
        json=["not", "an", "object"],
        headers=headers,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "Request body must be a valid JSON object."
    )


# ------------------------
# DELETE RECORD TESTS
# ------------------------

def test_delete_record_success_as_admin(client):
    record_creator_headers = authenticated_headers(client)
    create_sample_record(client, record_creator_headers)

    headers = admin_headers(client)

    response = client.delete(
        "/api/records/1",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == (
        "Record 1 deleted successfully."
    )

    follow_up = client.get("/api/records")
    assert follow_up.status_code == 200
    assert follow_up.get_json() == []


def test_delete_record_not_found_returns_404(client):
    headers = admin_headers(client)

    response = client.delete(
        "/api/records/999",
        headers=headers,
    )

    assert response.status_code == 404
    assert response.get_json()["error"] == "Record not found."


# ------------------------
# USER DELETION TESTS
# ------------------------

def test_delete_user_success_as_admin(client):
    register_user(client, username="victim", password="Password123!")

    headers = admin_headers(client)

    response = client.delete(
        "/api/users/victim",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "User victim deleted successfully."


def test_delete_user_not_found_returns_404(client):
    headers = admin_headers(client)

    response = client.delete(
        "/api/users/ghost",
        headers=headers,
    )

    assert response.status_code == 404
    assert response.get_json()["error"] == "User not found."


# ------------------------
# SECURITY MODE TESTS
# ------------------------

def test_get_security_mode_returns_boolean(client):
    response = client.get("/api/security/mode")

    assert response.status_code == 200
    assert isinstance(response.get_json()["secure_mode"], bool)


def test_set_security_mode_off_success(client):
    response = client.post(
        "/api/security/mode",
        json={"enabled": False},
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.get_json()["secure_mode"] is False


def test_create_record_with_suspicious_input_succeeds_when_secure_mode_off(client):
    register_user(client)
    login_response = login_user(client)
    token = login_response.get_json()["session_token"]

    mode_response = client.post(
        "/api/security/mode",
        json={"enabled": False},
        headers=AUTH_HEADERS,
    )

    assert mode_response.status_code == 200

    response = client.post(
        "/api/records",
        json={
            "name": "' OR 1=1 --",
            "description": "Malicious input",
        },
        headers={
            "X-Session-Token": token,
        },
    )

    assert response.status_code == 201
    assert response.get_json()["name"] == "' OR 1=1 --"


# ------------------------
# EVENT LOGGING TESTS
# ------------------------

def test_get_security_events_success_as_admin(client):
    headers = admin_headers(client)

    create_sample_record(
        client,
        headers,
        name="Logged Record",
        description="Event test",
    )

    response = client.get(
        "/api/security/events",
        headers=headers,
    )

    assert response.status_code == 200
    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) >= 1
    assert "event_type" in data[0]
    assert "outcome" in data[0]
    assert "timestamp" in data[0]
