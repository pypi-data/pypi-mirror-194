# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import os
from unittest.mock import MagicMock, patch
import wget
import pytest

os.environ["IRIS_DEBUG"] = "True"  # set debug variable for iris

from iris.sdk import get, login, logout, post, pull
from iris.sdk.exception import (
    BadRequestError,
    DownloadLinkExpiredError,
    EndpointNotFoundError,
    InvalidCommandError,
    InvalidLoginError,
)

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                     Test Module                                                      #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


# --------------------------------------       iris post    -------------------------------------- #


@patch("requests.get")
def test_iris_get_with_401_response(mock_get, mocker):
    mock_response = MagicMock()
    mock_response.ok = False
    mock_response.status_code = 401
    mock_get.return_value = mock_response

    with pytest.raises(Exception) as exc:
        post()

    assert str(exc.value) == "Invalid login credentials. Are you logged in?"


@patch("requests.get")
def test_iris_get_with_404_response(mock_get):
    mock_response = MagicMock()
    mock_response.ok = False
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    with pytest.raises(Exception) as exc:
        post()

    assert str(exc.value) == "Endpoint not found:  - experiment"


# --------------------------------------       iris get     -------------------------------------- #


@patch("requests.get")
def test_iris_get_with_401_response(mock_get):
    mock_response = MagicMock()
    mock_response.ok = False
    mock_response.status_code = 401
    mock_get.return_value = mock_response

    with pytest.raises(InvalidLoginError) as exc:
        get()

    assert str(exc.value) == "Invalid login credentials. Are you logged in?"


@patch("requests.get")
def test_iris_get_with_404_response(mock_get):
    mock_response = MagicMock()
    mock_response.ok = False
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    with pytest.raises(EndpointNotFoundError) as exc:
        get()

    assert str(exc.value) == "Endpoint not found:  - experiment"


# --------------------------------------      iris pull     -------------------------------------- #


def test_iris_pull_with_invalid_experiment_cmd():
    with pytest.raises(InvalidCommandError) as exc:
        pull("invalid")

    assert str(exc.value) == "Invalid command. Please check your command again!"


@patch("requests.get")
def test_pull_with_bad_request_error(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "failure"}
    mock_get.return_value = mock_response

    with pytest.raises(BadRequestError):
        pull("experiment_id:job_tag")


@patch("requests.get")
def test_pull_with_download_link_expired_error(mock_get):
    test_url = "https://pantheon-models.s3.amazonaws.com/b745218f-1097-468b-b6e8-ad94b262f585.tar.gz?AWSAccessKeyId=ASIASUF67VUBQVOLTG5E&Signature=xgtqhwbXxrAZ%2Ff1ycCzA56eKpjY%3D&x-amz-security-token=IQoJb3JpZ2luX2VjECwaCXVzLWVhc3QtMSJHMEUCIFWHYvIKUaFZYL7MuP%2BhgaDUs0Y9GZykxOjDmKLegj6YAiEApPCKEwkXc6%2Fmyud6sazqZiPTJ4e5WoYbVJZe5lx%2BIRUqjQUIxP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARACGgwxODA3ODkxNjEyMTkiDIslwBrsvMoGRuNHvCrhBEtWjUTxiNuZ%2B0YVMNPMH%2BZfDpx02mdWxnr82%2F%2BhxKBd2NFLG%2BAXvu%2FywNrusxmxc8sg4K16p7MVqb4LAqOhYxmjUZIinsfscA%2B2Z61N%2BvESnTMqDsi5aPj%2FLK%2B1e1e8clWEJcqNP6u3BPl20TTwtjZouOzHkomi4kEz%2BPCuNaE7cplex%2B%2FDqli4kVDvcJ1MFUJ84rCOQTRCeeMgP08W0u9dclxSoMmn65crENjh9oaGIJOZUWSc%2F%2BSF0SrR%2FeZexUvwA2nf8jSFXz2jaionN%2BLBaAENwQgl4e9ZhJbrR7k9QFYPOtsnNbpCwm%2F5KW9k25%2BL4NCf9DJLMkawSlv4lzURkY2TEbKISqk37qW4ap2JVm7IXN3i40lSI4la%2FfnjApm7ku94Q%2BUnJt2M%2BXWhCWPsGY0mgJDlcfNp914KF5TYGM1WwFako0kYCChCmjQALgdiCk6SnXgh1cEETzOTF5MtkBIUAUpbctIV9YSMKSL3%2F%2BX04%2BTNxtYeMpLw7kr8YFYP6b2u4zX2xpfRMIGPuDQAIenG6ZYLPJCmNitRcVWX5DRRzdWcnH153tPtIZScTtsQg62AMoONJYmMTPpQMlC%2FrLh5BOIcaFY%2FnZjPW2mpZTcYIRbX94MJTupmRRmE%2B7IwNgzF9N2c%2FOsD2dCSMxj7HhpJPmfFgPxQ8GOGT%2B9b5%2BUg4KswSIC3EOANLhJoF8VMZwxX1xWRxULd7F%2F5GJY%2FFhSurp63qrs43Ehls5ExjbOi7sqsnngWHQcgCW7r%2F%2FGETiiN04Mze6vYFihOwByZBoVQ45xOuyvVIH%2BlMXqTdTChsNSfBjqaAUKityuL92j6eBRSY32P06FF1NhnYioVUruDkgwGxIxN%2FdVkur969II9PWPEgwcRoUNzYOlfFwCxmG%2BI5QyiYMVybN8NcMe%2FeaVyyKemFuJbyUFm6PwDGKsGKgUUWSUUfIRFIQPoUDGkF%2B%2BQZqJmrrAxsl3YZHGOW%2FEg2YyrO2QXai5lxzgIJJRF78cTX0H0gjuZqZN3V5qwxTI%3D&Expires=1677010915"

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": "success",
        "experiment": {
            "jobs": [
                {
                    "name": "some_experiment_job_tag",
                    "download_link": {"link": test_url},
                    "flags": {"task": "glue"},
                }
            ]
        },
    }
    mock_get.return_value = mock_response

    with pytest.raises(DownloadLinkExpiredError):
        pull("experiment_id:job_tag")
