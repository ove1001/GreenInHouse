""" REST API controllers responsible of handling the server operations.
"""

import json
import time
from typing import Dict, Tuple, Optional
from http import HTTPStatus
from flask import current_app
from authlib.jose import JsonWebSignature  # type: ignore
from dms2223auth.data.config.authconfiguration import AuthConfiguration


def health_test() -> Tuple[None, Optional[int]]:
    """Simple health test endpoint.

    Returns:
        - Tuple[None, Optional[int]]: A tuple of no content and code 204 No Content.
    """
    return (None, HTTPStatus.NO_CONTENT.value)


def login(token_info: Dict) -> Tuple[str, Optional[int]]:
    """Generates a user token if the user validation was passed.

    Args:
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[str, Optional[int]]: A tuple with the JWS token and code 200 OK.
    """
    with current_app.app_context():
        cfg: AuthConfiguration = current_app.cfg
        jws: JsonWebSignature = current_app.jws
        user: str = ''
        if 'user_token' in token_info:
            user = token_info['user_token']['user']
        elif 'user_credentials' in token_info:
            user = token_info['user_credentials']['user']
        token: bytes = jws.serialize_compact(
            {'alg': 'HS256'},
            bytes(json.dumps({
                'user': user,
                'sub': user,
                'exp': (time.time() + cfg.get_jws_ttl())
            }), 'UTF-8'),
            bytes(cfg.get_jws_secret(), 'UTF-8')
        )
        return (token.decode('ascii'), HTTPStatus.OK.value)

def get_token_owner(token_info: Dict) -> Tuple[Dict, Optional[int]]:
    """Gets the user associated to a given token.

    Returns:
        - Tuple[Dict, Optional[int]]: A tuple with the user info and code 200 OK.
    """
    username: str = token_info['user_token']['user']
    return ({'username': username}, HTTPStatus.OK.value)
