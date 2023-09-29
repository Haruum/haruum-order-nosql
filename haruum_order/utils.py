from haruum_order.exceptions import (
    InvalidRequestException,
    FailedToFetchException
)
from rest_framework import status
import requests
import uuid


def is_valid_uuid_string(uuid_string: str) -> bool:
    try:
        uuid.UUID(uuid_string)
        return True

    except (TypeError, ValueError):
        return False


def request_post_and_return_response(request_data, url):
    try:
        response = requests.post(url, json=request_data)
        response_data = response.json()

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            raise InvalidRequestException(response_data.get('message'))

        if response.status_code != status.HTTP_200_OK:
            raise FailedToFetchException(response_data.get('message'))

        return response_data

    except requests.exceptions.RequestException as exc:
        raise FailedToFetchException('Failed to communicate with external service')


def request_get_and_return_response(request_data, url):
    try:
        modified_url = query_builder(url, request_data)

        response = requests.get(modified_url)
        response_data = response.json()

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            raise InvalidRequestException(response_data.get('message'))

        if response.status_code != status.HTTP_200_OK:
            raise FailedToFetchException(f'{response.status_code}: {response_data.get("message")}')

        return response_data

    except requests.exceptions.RequestException:
        raise FailedToFetchException('Failed to communicate with external service')


def query_builder(base_url, params):
    modified_url = base_url + '?'

    for k, v in params.items():
        modified_url = f'{modified_url}{k}={v}&'

    return modified_url[:-1]