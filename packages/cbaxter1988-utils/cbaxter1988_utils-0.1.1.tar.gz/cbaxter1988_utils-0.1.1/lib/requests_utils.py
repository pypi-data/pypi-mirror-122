import http
import json
from typing import Union

import requests
from cbaxter1988_models.src.http_response_models import ProblemDetailModel, PROBLEM_DETAIL_HEADER_JSON


def get_html_page(url) -> str:
    return requests.get(url).text


def get_request(url):
    return requests.get(url)


def post_request(url, body):
    response = requests.post(url=url, json=body, headers={"Content-Type": "application/json"})
    return response


def build_problem_detail_response(
        status: http.HTTPStatus,
        detail: str,
        type_name: str,
        title: str,
        instance: BaseException,
) -> requests.Response:
    """
    Builds a ProblemDetail response based on RFC 7807

    :param status: The HTTP status code ([RFC7231]
    :param detail: A human-readable explanation specific to this
occurrence of the problem.
    :param type_name: A URI reference [RFC3986] that identifies the problem type.
    :param title:  A short, human-readable summary of the problem type.
    :param instance:  A URI reference that identifies the specific
occurrence of the problem.
    :return:
    """
    model = ProblemDetailModel(
        type=type_name,
        status=status.value,
        detail=detail,
        instance=str(exception),
        title=title,
    )
    return requests.Response(
        status=status,
        headers=PROBLEM_DETAIL_HEADER_JSON,
        response=model.to_json()

    )


def build_json_response(status: http.HTTPStatus, payload: Union[dict, str]):
    if isinstance(payload, dict):
        return requests.Response(
            status=status,
            headers={"content-type": "application/json"},
            response=json.dumps(payload)
        )

    if isinstance(payload, str):
        return requests.Response(
            status=status,
            headers={"content-type": "application/json"},
            response=payload
        )
