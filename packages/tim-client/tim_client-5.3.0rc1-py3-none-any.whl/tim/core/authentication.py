import copy
from datetime import datetime
from requests import post
from .credentials import Credentials


def verify_credentials(
    credentials: Credentials
):
    if is_authenticated(credentials):
        return credentials
    new_credentials = login(credentials)
    if new_credentials.token is not None:
        credentials.token = new_credentials.token
        credentials.token_expiration = new_credentials.token_expiration
    else:
        raise ValueError("Login failed, login response does not contain access token")
    return credentials


def login(
    credentials: Credentials
) -> Credentials:
    if credentials.email is None or credentials.password is None:
        raise ValueError("Credentials not configured")

    response = post(
        f"{credentials.server}/auth/login",
        json={
            "email": credentials.email,
            "password": credentials.password,
        },
        timeout=60
    )

    if not response.ok:
        try:
            error_message = response.json()['message']
        except Exception:
            error_message = 'Invalid credentials'
        raise ValueError(error_message)

    response_json = response.json()
    copied_credentials = copy.deepcopy(credentials)

    copied_credentials.token = response_json.get("token")
    copied_credentials.token_expiration = response_json.get("tokenPayload").get("expiresAt")

    return copied_credentials


def is_authenticated(credentials: Credentials) -> bool:
    if not credentials.token:
        return False

    now = datetime.utcnow()
    expirationDate = datetime.strptime(credentials.token_expiration, "%Y-%m-%dT%H:%M:%SZ")
    if now > expirationDate:
        return False

    return True
