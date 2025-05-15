from conftest import Client
import json
from httpx import Response
from typing import Dict, Any


def assert_response(response: Response, expected_status: int = 200) -> Dict[str, Any]:
    assert (
        response.status_code == expected_status
    ), f"Expected status {expected_status}, got {response.status_code}"
    return response.json()


def log_test_step(step_name: str, response: Response) -> None:
    print(f"\n{step_name}")
    print(f"Request: {response.request.method} {response.request.url}")
    if response.request.content:
        print(f"Payload: {response.request.content}")
    print(f"Response: {response.status_code}")
    print("[Success]" if response.is_success else "[Failed]")


def test_update_profile_names(client: Client, fake):
    payload = {"login": "rosevinnur@gmail.com", "password": "7tfym8rX9N"}
    response = client.post("/login", data=payload)
    log_test_step("Login", response=response)
    assert_response(response=response)

    cookies = response.cookies
    assert "llt" in cookies, "Missing llt cookie in response"
    log_test_step("Session cookie verification", response=response)

    first_name = fake.first_name()
    last_name = fake.last_name()
    payload = {
        "ad_allowed": False,
        "beta": False,
        "country": "ru",
        "dateformat": 0,
        "language": "en",
        "name": first_name,
        "surname": last_name,
        "timezone": 0,
    }
    response = client.post(
        "/dashboard/settings/account/update", json=payload, cookies=cookies
    )
    log_test_step("Profile update", response=response)
    assert_response(response=response)

    response = client.get("/dashboard/account/info", cookies=cookies)
    log_test_step("Profile verification", response=response)
    profile_data = assert_response(response=response)

    assert (
        profile_data["name"] == first_name
    ), f"Expected name {first_name}, got {profile_data['name']}"
    assert (
        profile_data["surname"] == last_name
    ), f"Expected surname {last_name}, got {profile_data['surname']}"
