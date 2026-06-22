import os

import requests


BASE_URL = os.getenv(
    "BACKEND_URL",
    "https://smart-queue-management-system-gv9s.onrender.com"
).rstrip("/")

REQUEST_TIMEOUT = 10


def _response_payload(response):
    try:
        payload = response.json()
    except ValueError:
        payload = {
            "message": response.text
        }

    if response.ok:
        return payload

    detail = payload.get("detail") if isinstance(payload, dict) else None

    return {
        "error": detail or payload or f"Request failed with {response.status_code}",
        "status_code": response.status_code
    }


def _request(method, path, **kwargs):
    try:
        response = requests.request(
            method,
            f"{BASE_URL}{path}",
            timeout=REQUEST_TIMEOUT,
            **kwargs
        )
    except requests.RequestException as exc:
        return {
            "error": str(exc)
        }

    return _response_payload(response)


def has_error(payload):
    return isinstance(payload, dict) and "error" in payload


# =====================
# AUTH
# =====================

def signup(username, email, password, role="customer"):
    return _request(
        "POST",
        "/signup",
        json={
            "username": username,
            "email": email,
            "password": password,
            "role": role
        }
    )


def login(username, password):
    return _request(
        "POST",
        "/login",
        data={
            "username": username,
            "password": password
        }
    )


# =====================
# USERS
# =====================

def get_users():
    result = _request("GET", "/users")
    return result if isinstance(result, list) else []


# =====================
# QUEUES
# =====================

def get_queues():
    result = _request("GET", "/queues")
    return result if isinstance(result, list) else []


def create_queue(name, description, status="ACTIVE"):
    return _request(
        "POST",
        "/queues",
        json={
            "name": name,
            "description": description,
            "status": status
        }
    )


def update_queue(queue_id, name=None, description=None, status=None):
    payload = {}

    if name is not None:
        payload["name"] = name

    if description is not None:
        payload["description"] = description

    if status is not None:
        payload["status"] = status

    return _request(
        "PUT",
        f"/queues/{queue_id}",
        json=payload
    )


def delete_queue(queue_id):
    return _request(
        "DELETE",
        f"/queues/{queue_id}"
    )


# =====================
# TOKENS
# =====================

def get_tokens():
    result = _request("GET", "/tokens")
    return result if isinstance(result, list) else []


def get_queue_tokens(queue_id):
    result = _request("GET", f"/queues/{queue_id}/tokens")
    return result if isinstance(result, list) else []


def join_queue(queue_id, user_id, priority_level=1):
    return _request(
        "POST",
        f"/queues/{queue_id}/join",
        json={
            "user_id": user_id,
            "priority_level": priority_level
        }
    )


def join_queue_customer(queue_id, customer_name, email, priority_level=1):
    return _request(
        "POST",
        f"/queues/{queue_id}/join-customer",
        json={
            "customer_name": customer_name,
            "email": email,
            "priority_level": priority_level
        }
    )


def call_next_token(queue_id):
    return _request(
        "POST",
        f"/queues/{queue_id}/call-next"
    )


def update_token_status(token_id, status):
    return _request(
        "PUT",
        f"/tokens/{token_id}/status",
        json={
            "status": status
        }
    )


# =====================
# ANALYTICS
# =====================

def get_dashboard_stats():
    return _request("GET", "/analytics/dashboard")


# =====================
# HELPER
# =====================

def is_backend_running():
    result = _request("GET", "/queues")
    return not has_error(result)
