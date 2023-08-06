import json
from typing import Any, TypeVar, Optional
import requests
from .credentials import Credentials
from .authentication import verify_credentials

T = TypeVar('T')


def execute_request(
    credentials: Credentials,
    method: str,
    path: str,
    body: Optional[Any] = None,
    params: Optional[Any] = None,
    file: Optional[str] = None,
) -> Any:
    verified_credentials = verify_credentials(credentials)
    headers = {
        "Authorization": f"Bearer {verified_credentials.token}",
        "X-Tim-Client": verified_credentials.client_name,
    }

    def upload_file():
        return requests.request(
            method=method,
            url=f"{verified_credentials.server}{path}",
            headers=headers,  # type: ignore
            files={
                "configuration": json.dumps(body),
                "file": file,
            },  # type: ignore
            timeout=60
        )

    def handle_request():
        return requests.request(
            method=method,
            url=f"{verified_credentials.server}{path}",
            json=body,
            params=params,
            headers=headers,  # type: ignore
            timeout=60
        )

    response = upload_file() if file else handle_request()

    if not response.ok:
        if response.status_code >= 500:
            raise ValueError(f'Internal error ({response.status_code}) - please contact support')

        try:
            error_message = response.json()['message']
        except Exception:
            error_message = f'Internal error - {response.text}'
        raise ValueError(error_message)

    if response.headers.get('content-type') == 'application/json':
        return response.json()

    return response.text
