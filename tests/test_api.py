import datetime
import json

import pytest
import requests
from jsonschema import validate

from utils import schemas_path

USERS_URL = "https://reqres.in/api/users"
LOGIN_URL = "https://reqres.in/api/login"


def test_get_users_delay_time():
    delay = 5

    response = requests.get(
        url=USERS_URL,
        params=f"delay={delay}"
    )

    assert datetime.timedelta(seconds=delay) <= response.elapsed


def test_put_updated_job():
    name = "morpheus"
    job = "zion resident"
    payload = {"name": name, "job": job}

    response = requests.put(
        url=USERS_URL + "/2",
        json=payload
    )

    assert job == response.json()["job"]


def test_patch_updated_job():
    name = "morpheus"
    job = "zion resident"
    user = "/2"
    payload = {"name": name, "job": job}

    response = requests.patch(
        url=USERS_URL + user,
        json=payload
    )

    assert name == response.json()["name"]


def test_successful_login_with_status_200():
    payload = {"email": "eve.holt@reqres.in",
               "password": "cityslicka"}

    response = requests.post(
        url=LOGIN_URL,
        data=payload
    )

    assert response.status_code == 200


def test_post_create_with_status_201():
    payload = {"name": "morpheus", "job": "leader"}

    response = requests.post(
        url=USERS_URL,
        json=payload
    )

    assert response.status_code == 201


def test_delete_user_with_status_204():
    user_number = "/2"

    response = requests.delete(
        url=USERS_URL + user_number
    )

    assert response.status_code == 204


def test_unsuccessful_login_with_wrong_email():
    payload = {"email": "kek",
               "password": "cityslicka"}

    response = requests.post(
        url=LOGIN_URL,
        data=payload
    )

    assert response.status_code == 400


def test_users_not_found_404():
    response = requests.get(
        url=USERS_URL + "/unknown"
    )

    assert response.status_code == 404


def test_list_users_schema():
    params = {"page": 2}

    response = requests.get(
        url=USERS_URL,
        params=params
    )

    with open(schemas_path.path("users.json")) as file:
        validate(response.json(), schema=json.loads(file.read()))


def test_user_schema_from_json_file():
    user_number = "/2"

    response = requests.get(
        url=USERS_URL + user_number
    )

    with open(schemas_path.path("single_user.json")) as file:
        validate(response.json(), schema=json.loads(file.read()))


def test_user_schema_from_python_file():
    user_number = "/2"

    response = requests.get(
        url=USERS_URL + user_number
    )

    from schemas.single_user_schema import single_user
    validate(response.json(), schema=single_user)


@pytest.mark.xfail(reason="Этот тест негативный")
def test_patch_updated_schema_with_no_additional_properties():
    name = "morpheus"
    job = "zion resident"
    user = "/2"
    payload = {"name": name, "job": job, "kek": "lel"}

    response = requests.patch(
        url=USERS_URL + user,
        json=payload
    )

    with open(schemas_path.path("update_user_schema.json")) as file:
        validate(response.json(), schema=json.loads(file.read()))


def test_list_users_per_page_param():
    params = {"page": 2}

    response = requests.get(
        url=USERS_URL,
        params=params
    )

    per_page_param = response.json()["per_page"]
    data_len = len(response.json()["data"])
    assert per_page_param == data_len


def test_no_data_on_empty_page():
    params = {"page": 2}

    response = requests.get(
        url=USERS_URL,
        params=params
    )

    total_pages_param = response.json()["total_pages"]

    assert response.json()["data"] != []

    response = requests.get(
        url=USERS_URL,
        params={"page": total_pages_param + 1}
    )
    assert response.json()["data"] == []
