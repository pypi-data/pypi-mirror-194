"""
This module contains the authentication utils for the iris package
"""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import jwt
import requests
import typer
from rich import print
import time
import json
import functools
from auth0.v3.authentication.token_verifier import (
    AsymmetricSignatureVerifier,
    TokenVerifier,
)

# internal imports
from .exception import (
    EndpointNotFoundError,
    InvalidLoginError,
    NotLoggedInError,
    UnprocessableEntityError,
)
from .conf_manager import conf_mgr


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                      Auth Utils                                                      #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


def validate_token(id_token):
    """
    Verify the token and its precedence

    :param id_token:
    """
    jwks_url = f"https://{conf_mgr.AUTH0_DOMAIN}/.well-known/jwks.json"
    issuer = f"https://{conf_mgr.AUTH0_DOMAIN}/"
    sv = AsymmetricSignatureVerifier(jwks_url)
    tv = TokenVerifier(
        signature_verifier=sv, issuer=issuer, audience=conf_mgr.AUTH0_CLIENT_ID
    )
    tv.verify(id_token)


def auth0_login():
    """
    Runs the device authorization flow and stores the user object in memory
    """
    device_code_payload = {
        "client_id": conf_mgr.AUTH0_CLIENT_ID,
        "scope": "openid profile",
        "audience": conf_mgr.AUTH0_AUDIENCE,
    }
    device_code_response = requests.post(
        f"https://{conf_mgr.AUTH0_DOMAIN}/oauth/device/code",
        data=device_code_payload,
    )

    if device_code_response.status_code != 200:
        print("Error generating the device code")
        raise typer.Exit(code=1)

    device_code_data = device_code_response.json()
    print(
        "1. On your computer or mobile device navigate to: ",
        device_code_data["verification_uri_complete"],
    )
    print("2. Enter the following code: ", device_code_data["user_code"])

    token_payload = {
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        "device_code": device_code_data["device_code"],
        "client_id": conf_mgr.AUTH0_CLIENT_ID,
    }

    authenticated = False
    while not authenticated:
        print("Checking if the user completed the flow...")
        token_response = requests.post(
            f"https://{conf_mgr.AUTH0_DOMAIN}/oauth/token", data=token_payload
        )

        token_data = token_response.json()

        if token_response.status_code == 200:
            validate_token(token_data["id_token"])

            print("Token verified!")
            conf_mgr.current_user = jwt.decode(
                token_data["id_token"],
                algorithms=conf_mgr.ALGORITHMS,
                options={"verify_signature": False},
            )
            conf_mgr.access_token = token_data.get("access_token", None)
            authenticated = True

            print("Authenticated!")
        elif token_data["error"] not in ("authorization_pending", "slow_down"):
            print(token_data["error_description"])
            raise typer.Exit(code=1)
        else:
            time.sleep(device_code_data["interval"])


def store_credentials(filename):
    json.dump(
        {"current_user": conf_mgr.current_user, "access_token": conf_mgr.access_token},
        open(filename, "w"),
    )


def load_credentials(filename):
    try:
        credentials = json.load(open(filename, "r"))
    except FileNotFoundError:
        raise NotLoggedInError

    conf_mgr.current_user = credentials["current_user"]
    conf_mgr.access_token = credentials["access_token"]


def auth(fn: callable):
    """A decorator to add the key to the function kwargs

    Args:
        fn (callable): The function to decorate

    Returns:
        callable: The decorated function
    """

    @functools.wraps(fn)
    def auth0_wrapper(*args, **kwargs):
        try:
            load_credentials(conf_mgr.CREDENTIALS_PATH)
        except NotLoggedInError:
            try:
                auth0_login()
            except Exception as e:
                raise e
            else:
                store_credentials(
                    conf_mgr.CREDENTIALS_PATH
                )  # store if no errors in login
        return fn(*args, **kwargs)

    @functools.wraps(fn)
    def dummy_wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return auth0_wrapper if conf_mgr.AUTHENTICATE else dummy_wrapper


def handle_bad_response(response, endpoint):
    if response.status_code == 401:
        print("Invalid login credentials. Are you logged in?")
        raise InvalidLoginError
    elif response.status_code == 404:
        print(f"Endpoint [green]{endpoint}[/green] not found")
        raise EndpointNotFoundError(details=endpoint)
    elif response.status_code == 422:
        print("Invalid request")
        raise UnprocessableEntityError
    else:
        print(f"Received bad response {response}")
        raise typer.Abort()
