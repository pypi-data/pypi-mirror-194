"""
This module implements and instantiates the common configuration class used in the project.
"""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import os
from pathlib import Path
from urllib.parse import urljoin

from omegaconf import OmegaConf

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["ConfManager", "conf_mgr"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                Configuration Manager                                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class ConfManager:
    """Configuration Manager class"""

    base_path = Path(__file__).parent.parent
    config = OmegaConf.load(open(base_path / "config.yaml", "r"))

    # get authentication config from config
    AUTH0_CLIENT_ID = config.auth0_client_id
    AUTH0_DOMAIN = config.auth0_domain
    AUTH0_AUDIENCE = config.auth0_audience
    ALGORITHMS = config.auth0_algorithm
    AUTHENTICATE = config.authenticate
    CREDENTIALS_PATH = Path.home() / config.keyfile_name

    # base image config from config
    BASE_IMAGE = config.base_image

    # pull base url from environment if set, otherwise use the default in the config.
    base = os.environ.get("IRIS_BASE", config.base)
    runner_url = urljoin(base, config.runner_path)

    # current user, and access token globals.
    # these get set by the flow
    current_user = None
    access_token = None


# ─────────────────────────────────────────────── ConfManager instance ─────────────────────────────────────────────── #


conf_mgr: ConfManager = ConfManager()

debug = os.environ.get("IRIS_DEBUG", "False").lower() in ["t", "true"]
conf_mgr.AUTHENTICATE = False if debug else conf_mgr.AUTHENTICATE
