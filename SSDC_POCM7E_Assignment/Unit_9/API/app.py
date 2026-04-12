"""
Secure Online Retailer API / CLI prototype for Unit 11.

This module provides:
- secure account creation
- authentication and session management
- role-based access control
- CRUD operations for records
- security mode ON/OFF behaviour
- input validation
- event monitoring
- password hashing

The implementation uses in-memory storage for demonstration purposes
and is designed to align more closely with the Unit 6 team design.
"""

import argparse
import hashlib
import hmac
import logging
import os
import secrets
from datetime import UTC, datetime, timedelta
from functools import wraps

from flask import Flask, jsonify, request

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

API_KEY = os.environ.get("API_KEY", "my-secret-api-access-token")
SECURITY_ENABLED = True

MAX_NAME_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_MINUTES = 5

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

# ---------------------------------------------------------------------
# In-memory repository
# Required data structures:
# - dict: users
# - list: records / orders / events
# - set: active sessions
# ---------------------------------------------------------------------

users = {}
records = []
security_events = []
active_sessions = set()
failed_login_attempts = {}
locked_accounts = {}
next_record_id = 1


# ---------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------

def current_timestamp():
    """
    Return the current UTC timestamp in ISO 8601 format with a trailing Z.

    Returns:
        str: UTC timestamp string suitable for API responses.
    """
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def reset_state():
    """
    Reset in-memory state for test isolation.
    """
    global next_record_id
    users.clear()
    records.clear()
    security_events.clear()
    active_sessions.clear()
    failed_login_attempts.clear()
    locked_accounts.clear()
    next_record_id = 1


def log_security_event(event_type, outcome, identifier="", details=""):
    """
    Record a structured security event.

    Args:
        event_type (str): Type of event.
        outcome (str): Outcome such as success, failure, blocked.
        identifier (str): Minimal identifier for accountability.
        details (str): Additional context without sensitive data.
    """
    event = {
        "timestamp": current_timestamp(),
        "event_type": event_type,
        "outcome": outcome,
        "identifier": identifier,
        "details": details,
    }
    security_events.append(event)
    logging.info("%s | %s | %s | %s", event_type, outcome, identifier, details)


def hash_password(password, salt=None):
    """
    Hash a password using PBKDF2-HMAC-SHA256.

    Args:
        password (str): Plaintext password.
        salt (str | None): Optional hex salt.

    Returns:
        tuple[str, str]: Hex salt and hex password hash.
    """
    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        100_000,
    ).hex()

    return salt, password_hash


def verify_password(password, salt, expected_hash):
    """
    Verify a plaintext password against a stored hash.

    Args:
        password (str): Plaintext password.
        salt (str): Hex salt.
        expected_hash (str): Stored hex hash.

    Returns:
        bool: True if valid, otherwise False.
    """
    _, calculated_hash = hash_password(password, salt)
    return hmac.compare_digest(calculated_hash, expected_hash)


def find_record(record_id):
    """
    Return the record with the given ID, or None if not found.

    Args:
        record_id (int): Record identifier.

    Returns:
        dict | None: Matching record or None.
    """
    return next((record for record in records if record["id"] == record_id), None)


def is_account_locked(username):
    """
    Check whether an account is currently locked.

    Args:
        username (str): Username.

    Returns:
        bool: True if locked, otherwise False.
    """
    if username not in locked_accounts:
        return False

    if datetime.now(UTC) >= locked_accounts[username]:
        del locked_accounts[username]
        failed_login_attempts[username] = 0
        return False

    return True


def register_failed_login(username):
    """
    Register a failed login attempt and apply lockout if necessary.

    Args:
        username (str): Username.
    """
    failed_login_attempts[username] = failed_login_attempts.get(username, 0) + 1

    if SECURITY_ENABLED and failed_login_attempts[username] >= MAX_LOGIN_ATTEMPTS:
        locked_accounts[username] = datetime.now(UTC) + timedelta(
            minutes=LOCKOUT_MINUTES
        )
        log_security_event(
            "authentication",
            "blocked",
            username,
            "Account locked after repeated failed logins.",
        )


def validate_user_payload(data):
    """
    Validate incoming JSON payload for account registration.

    Args:
        data (dict | None): Parsed JSON request body.

    Returns:
        tuple[bool, dict | None, dict | None]:
            - validity flag
            - cleaned payload
            - error payload
    """
    if not isinstance(data, dict):
        return False, None, {
            "error": "Request body must be a valid JSON object."
        }

    allowed_fields = {"username", "password", "role"}
    unexpected_fields = set(data.keys()) - allowed_fields

    if unexpected_fields:
        return False, None, {
            "error": (
                f"Unexpected field(s): "
                f"{', '.join(sorted(unexpected_fields))}."
            )
        }

    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")

    if not isinstance(username, str) or not username.strip():
        return False, None, {"error": "Field 'username' must be a non-empty string."}

    if not isinstance(password, str) or len(password) < 8:
        return False, None, {
            "error": "Field 'password' must be a string of at least 8 characters."
        }

    if role not in {"user", "admin"}:
        return False, None, {"error": "Field 'role' must be 'user' or 'admin'."}

    cleaned = {
        "username": username.strip(),
        "password": password,
        "role": role,
    }

    return True, cleaned, None


def validate_record_payload(data, require_name=True):
    """
    Validate incoming JSON payload for create and update operations.

    Validation rules:
    - Request body must be a JSON object
    - Only 'name' and 'description' are allowed
    - 'name' is required when require_name is True
    - 'name' must be a non-empty string
    - 'description' must be a string if provided
    - strict pattern rejection applies when SECURITY_ENABLED is True

    Args:
        data (dict | None): Parsed JSON request body.
        require_name (bool): Whether the 'name' field must be present.

    Returns:
        tuple[bool, dict | None, dict | None]:
            - validity flag
            - cleaned payload
            - error payload
    """
    if not isinstance(data, dict):
        return False, None, {
            "error": "Request body must be a valid JSON object."
        }

    allowed_fields = {"name", "description"}
    unexpected_fields = set(data.keys()) - allowed_fields

    if unexpected_fields:
        return False, None, {
            "error": (
                f"Unexpected field(s): "
                f"{', '.join(sorted(unexpected_fields))}."
            )
        }

    cleaned = {}

    if require_name and "name" not in data:
        return False, None, {"error": "Field 'name' is required."}

    if "name" in data:
        if not isinstance(data["name"], str):
            return False, None, {"error": "Field 'name' must be a string."}

        name = data["name"].strip()

        if not name:
            return False, None, {"error": "Field 'name' cannot be empty."}

        if len(name) > MAX_NAME_LENGTH:
            return False, None, {
                "error": f"Field 'name' must not exceed {MAX_NAME_LENGTH} characters."
            }

        if SECURITY_ENABLED and is_suspicious_input(name):
            return False, None, {
                "error": "Field 'name' contains suspicious input."
            }

        cleaned["name"] = name

    if "description" in data:
        if not isinstance(data["description"], str):
            return False, None, {
                "error": "Field 'description' must be a string."
            }

        description = data["description"].strip()

        if len(description) > MAX_DESCRIPTION_LENGTH:
            return False, None, {
                "error": (
                    "Field 'description' must not exceed "
                    f"{MAX_DESCRIPTION_LENGTH} characters."
                )
            }

        if SECURITY_ENABLED and is_suspicious_input(description):
            return False, None, {
                "error": "Field 'description' contains suspicious input."
            }

        cleaned["description"] = description
    else:
        cleaned["description"] = ""

    return True, cleaned, None


def is_suspicious_input(value):
    """
    Detect simple suspicious input patterns used for demonstration.

    Args:
        value (str): Input string.

    Returns:
        bool: True if suspicious, otherwise False.
    """
    suspicious_patterns = [
        "' OR 1=1",
        "\" OR 1=1",
        "--",
        "<script",
        "DROP TABLE",
    ]
    lowered = value.lower()

    return any(pattern.lower() in lowered for pattern in suspicious_patterns)


# ---------------------------------------------------------------------
# Decorators
# ---------------------------------------------------------------------

def require_api_key(func):
    """
    Require a valid API key for protected endpoints when security is enabled.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not SECURITY_ENABLED:
            return func(*args, **kwargs)

        key = request.headers.get("X-API-Key")
        if key != API_KEY:
            log_security_event(
                "api_key_check",
                "failure",
                "",
                "Invalid or missing X-API-Key header.",
            )
            return jsonify({"error": "Unauthorized"}), 401

        return func(*args, **kwargs)

    return wrapper


def require_session(func):
    """
    Require a valid session token for protected user endpoints.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not SECURITY_ENABLED:
            return func(*args, **kwargs)

        token = request.headers.get("X-Session-Token")
        if not token or token not in active_sessions:
            log_security_event(
                "session_check",
                "failure",
                "",
                "Missing or invalid session token.",
            )
            return jsonify({"error": "Valid session token required."}), 401

        return func(*args, **kwargs)

    return wrapper


def require_role(required_role):
    """
    Enforce simple role-based access control.

    Args:
        required_role (str): Required role.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not SECURITY_ENABLED:
                return func(*args, **kwargs)

            username = request.headers.get("X-Username")
            if not username or username not in users:
                return jsonify({"error": "User context is required."}), 401

            if users[username]["role"] != required_role:
                log_security_event(
                    "authorization",
                    "failure",
                    username,
                    f"Required role: {required_role}",
                )
                return jsonify({"error": "Forbidden"}), 403

            return func(*args, **kwargs)

        return wrapper

    return decorator


# ---------------------------------------------------------------------
# User account endpoints
# ---------------------------------------------------------------------

@app.route("/api/register", methods=["POST"])
def register_user():
    """
    Create a secure user account.

    Returns:
        Response: JSON response confirming account creation or an error.
    """
    data = request.get_json(silent=True)
    is_valid, cleaned, error = validate_user_payload(data)

    if not is_valid:
        return jsonify(error), 400

    username = cleaned["username"]

    if username in users:
        return jsonify({"error": "Username already exists."}), 409

    salt, password_hash = hash_password(cleaned["password"])

    users[username] = {
        "username": username,
        "salt": salt,
        "password_hash": password_hash,
        "role": cleaned["role"],
        "created_at": current_timestamp(),
    }

    failed_login_attempts[username] = 0

    log_security_event(
        "registration",
        "success",
        username,
        "User account created.",
    )

    return jsonify(
        {
            "message": "User registered successfully.",
            "username": username,
            "role": cleaned["role"],
        }
    ), 201


@app.route("/api/login", methods=["POST"])
def login():
    """
    Authenticate a user and issue a session token.

    Returns:
        Response: Session token or error.
    """
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a valid JSON object."}), 400

    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"error": "Username and password are required."}), 400

    username = username.strip()

    if username not in users:
        log_security_event(
            "authentication",
            "failure",
            username,
            "Unknown username.",
        )
        return jsonify({"error": "Invalid credentials."}), 401

    if SECURITY_ENABLED and is_account_locked(username):
        return jsonify({"error": "Account temporarily locked."}), 423

    user = users[username]

    if not verify_password(password, user["salt"], user["password_hash"]):
        register_failed_login(username)
        log_security_event(
            "authentication",
            "failure",
            username,
            "Invalid password.",
        )
        return jsonify({"error": "Invalid credentials."}), 401

    failed_login_attempts[username] = 0
    session_token = secrets.token_hex(16)
    active_sessions.add(session_token)

    log_security_event(
        "authentication",
        "success",
        username,
        "Session issued.",
    )

    return jsonify(
        {
            "message": "Login successful.",
            "session_token": session_token,
            "username": username,
            "role": user["role"],
        }
    ), 200


@app.route("/api/profile/<username>", methods=["GET"])
@require_session
def get_profile(username):
    """
    Return a user's non-sensitive stored profile data.

    Args:
        username (str): Username.

    Returns:
        Response: Profile data or a 404 error.
    """
    if username not in users:
        return jsonify({"error": "User not found."}), 404

    user = users[username]

    return jsonify(
        {
            "username": user["username"],
            "role": user["role"],
            "created_at": user["created_at"],
        }
    ), 200


@app.route("/api/users/<username>", methods=["DELETE"])
@require_api_key
@require_session
@require_role("admin")
def delete_user(username):
    """
    Delete a user account and invalidate sessions conceptually.

    Args:
        username (str): Username.

    Returns:
        Response: Success message or a 404 error.
    """
    if username not in users:
        return jsonify({"error": "User not found."}), 404

    del users[username]
    failed_login_attempts.pop(username, None)
    locked_accounts.pop(username, None)

    log_security_event(
        "user_deletion",
        "success",
        username,
        "User removed from repository.",
    )

    return jsonify({"message": f"User {username} deleted successfully."}), 200


# ---------------------------------------------------------------------
# Record CRUD endpoints
# ---------------------------------------------------------------------

@app.route("/api/records", methods=["POST"])
@require_api_key
@require_session
def create_record():
    """
    Create a new record from validated JSON input.

    Returns:
        Response: Created record or an error.
    """
    global next_record_id

    data = request.get_json(silent=True)
    is_valid, cleaned, error = validate_record_payload(data, require_name=True)

    if not is_valid:
        log_security_event(
            "record_create",
            "failure",
            "",
            "Validation failed.",
        )
        return jsonify(error), 400

    timestamp = current_timestamp()

    record = {
        "id": next_record_id,
        "name": cleaned["name"],
        "description": cleaned["description"],
        "created_at": timestamp,
        "updated_at": timestamp,
    }

    records.append(record)
    next_record_id += 1

    log_security_event(
        "record_create",
        "success",
        "",
        f"Record {record['id']} created.",
    )

    return jsonify(record), 201


@app.route("/api/records", methods=["GET"])
def get_records():
    """
    Return all stored records.

    Returns:
        Response: JSON array of records.
    """
    return jsonify(records), 200


@app.route("/api/records/<int:record_id>", methods=["GET"])
def get_record(record_id):
    """
    Return a single record by ID.

    Args:
        record_id (int): Record identifier.

    Returns:
        Response: Record or a 404 error.
    """
    record = find_record(record_id)

    if not record:
        return jsonify({"error": "Record not found."}), 404

    return jsonify(record), 200


@app.route("/api/records/<int:record_id>", methods=["PUT"])
@require_api_key
@require_session
def update_record(record_id):
    """
    Replace an existing record using validated JSON input.

    Args:
        record_id (int): Record identifier.

    Returns:
        Response: Updated record or an error.
    """
    record = find_record(record_id)

    if not record:
        return jsonify({"error": "Record not found."}), 404

    data = request.get_json(silent=True)
    is_valid, cleaned, error = validate_record_payload(data, require_name=True)

    if not is_valid:
        log_security_event(
            "record_update",
            "failure",
            "",
            f"Validation failed for record {record_id}.",
        )
        return jsonify(error), 400

    record["name"] = cleaned["name"]
    record["description"] = cleaned["description"]
    record["updated_at"] = current_timestamp()

    log_security_event(
        "record_update",
        "success",
        "",
        f"Record {record_id} updated.",
    )

    return jsonify(record), 200


@app.route("/api/records/<int:record_id>", methods=["DELETE"])
@require_api_key
@require_session
@require_role("admin")
def delete_record(record_id):
    """
    Delete a record by ID.

    Args:
        record_id (int): Record identifier.

    Returns:
        Response: Success message or a 404 error.
    """
    record = find_record(record_id)

    if not record:
        return jsonify({"error": "Record not found."}), 404

    records.remove(record)

    log_security_event(
        "record_delete",
        "success",
        "",
        f"Record {record_id} deleted.",
    )

    return jsonify(
        {"message": f"Record {record_id} deleted successfully."}
    ), 200


@app.route("/api/security/events", methods=["GET"])
@require_api_key
@require_session
@require_role("admin")
def get_security_events():
    """
    Return structured security events for monitoring.

    Returns:
        Response: JSON array of security events.
    """
    return jsonify(security_events), 200


@app.route("/api/security/mode", methods=["GET"])
def get_security_mode():
    """
    Return the current security mode.

    Returns:
        Response: Current value of SECURITY_ENABLED.
    """
    return jsonify({"secure_mode": SECURITY_ENABLED}), 200


@app.route("/api/security/mode", methods=["POST"])
@require_api_key
def set_security_mode():
    """
    Enable or disable security mode at runtime.

    Returns:
        Response: Updated security mode or validation error.
    """
    global SECURITY_ENABLED

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or "enabled" not in data:
        return jsonify({"error": "Field 'enabled' is required."}), 400

    if not isinstance(data["enabled"], bool):
        return jsonify({"error": "Field 'enabled' must be boolean."}), 400

    SECURITY_ENABLED = data["enabled"]

    log_security_event(
        "security_mode_change",
        "success",
        "",
        f"secure_mode set to {SECURITY_ENABLED}.",
    )

    return jsonify({"secure_mode": SECURITY_ENABLED}), 200


# ---------------------------------------------------------------------
# CLI helpers
# ---------------------------------------------------------------------

def seed_default_admin():
    """
    Create a default admin account for CLI/demo use if it does not exist.
    """
    if "admin" in users:
        return

    salt, password_hash = hash_password("AdminPass123!")

    users["admin"] = {
        "username": "admin",
        "salt": salt,
        "password_hash": password_hash,
        "role": "admin",
        "created_at": current_timestamp(),
    }

    failed_login_attempts["admin"] = 0

    log_security_event(
        "seed",
        "success",
        "admin",
        "Default admin account seeded.",
    )


def cli_list_records():
    """
    Print records to the terminal for simple CLI access.
    """
    if not records:
        print("No records found.")
        return

    for record in records:
        print(record)


def cli_list_users():
    """
    Print users to the terminal without sensitive data.
    """
    if not users:
        print("No users found.")
        return

    for username, user in users.items():
        print(
            {
                "username": username,
                "role": user["role"],
                "created_at": user["created_at"],
            }
        )


# ---------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Secure Online Retailer API / CLI prototype"
    )
    parser.add_argument(
        "--run-api",
        action="store_true",
        help="Run the Flask API.",
    )
    parser.add_argument(
        "--secure",
        choices=["on", "off"],
        default="on",
        help="Toggle secure_mode on or off.",
    )
    parser.add_argument(
        "--seed-admin",
        action="store_true",
        help="Seed a default admin account.",
    )
    parser.add_argument(
        "--list-records",
        action="store_true",
        help="List records through the CLI.",
    )
    parser.add_argument(
        "--list-users",
        action="store_true",
        help="List users through the CLI.",
    )

    args = parser.parse_args()

    SECURITY_ENABLED = args.secure == "on"

    if args.seed_admin:
        seed_default_admin()

    if args.list_records:
        cli_list_records()

    if args.list_users:
        cli_list_users()

    if args.run_api:
        app.run(debug=True)
