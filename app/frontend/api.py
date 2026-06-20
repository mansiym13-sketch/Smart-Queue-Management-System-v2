import requests

BASE_URL = "https://smart-queue-management-system-gv9s.onrender.com"

# =====================
# AUTH
# =====================

def signup(username, email, password, role="customer"):

    response = requests.post(
        f"{BASE_URL}/signup",
        json={
            "username": username,
            "email": email,
            "password": password,
            "role": role
        }
    )

    return response.json()


def login(username, password):

    response = requests.post(
        f"{BASE_URL}/login",
        data={
            "username": username,
            "password": password
        }
    )

    return response.json()


# =====================
# USERS
# =====================

def get_users():

    response = requests.get(
        f"{BASE_URL}/users"
    )

    return response.json()


# =====================
# QUEUES
# =====================

def get_queues():

    response = requests.get(
        f"{BASE_URL}/queues"
    )

    return response.json()


def create_queue(name, description):

    response = requests.post(
        f"{BASE_URL}/queues",
        json={
            "name": name,
            "description": description
        }
    )

    print("Status:", response.status_code)
    print("Response:", response.text)

    return response.text


# =====================
# HELPER
# =====================

def is_backend_running():

    try:
        response = requests.get(
            f"{BASE_URL}/queues",
            timeout=3
        )
        return response.status_code == 200

    except:
        return False