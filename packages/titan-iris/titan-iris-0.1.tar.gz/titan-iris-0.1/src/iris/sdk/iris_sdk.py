"""
This module will contain all the sdk functions for the iris command sdk, including login, logout, get, post, pull.
"""
import hashlib

# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import io
import json
import logging
import tarfile
from pathlib import Path
from typing import List, Optional
from urllib.parse import urljoin
import os

from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

# for iris pull
import requests
import typer
from rich import print
import wget

# internal imports
from .auth_utils import auth, handle_bad_response
from .conf_manager import conf_mgr
from .exception import (
    BadRequestError,
    DownloadLinkExpiredError,
    DownloadLinkNotFoundError,
    InvalidCommandError,
    ArtefactTypeInvalidError,
    ArtefactNotFoundError,
    UnsafeTensorsError,
)
from .utils import pull_image, tarify, dump

# ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                  IRIS USERS SDK                                                     #
# ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


# ------------------------------------      Setup Logger      ------------------------------------ #
# Logger config
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# --------------------------------------      iris login    -------------------------------------- #
@auth
def login():
    print(f"Welcome {conf_mgr.current_user['name']}!")


# --------------------------------------     iris logout    -------------------------------------- #


def logout():
    print("logging out")
    path = Path.home() / Path(conf_mgr.config.keyfile_name)
    if path.exists():
        path.unlink()
    raise typer.Exit(0)


# --------------------------------------      iris post     -------------------------------------- #


@auth
def post(
    flags: List[str] = typer.Argument(None),
):
    params = dict([x.split("=") for x in flags])
    endpoint = "experiment"
    url = urljoin(conf_mgr.runner_url, f"{endpoint}/")
    headers = {"Authorization": f"Bearer {conf_mgr.access_token}"}

    response = requests.post(url=url, headers=headers, data=params)
    if not response.ok:
        handle_bad_response(response, endpoint)
    else:
        dump(response)


# --------------------------------------       iris get     -------------------------------------- #


@auth
def get():
    endpoint = "experiment"
    url = urljoin(conf_mgr.runner_url, f"{endpoint}/")
    headers = {"Authorization": f"Bearer {conf_mgr.access_token}"}

    response = requests.get(url=url, headers=headers)
    if not response.ok:
        handle_bad_response(response, endpoint)
    else:
        dump(response)


# --------------------------------------      iris pull     -------------------------------------- #


@auth
def pull(experiment_cmd: str):
    logger.info("***Executing pull command***")

    Path("model_storage").mkdir(parents=True, exist_ok=True)

    args = experiment_cmd.split(":")
    if len(args) != 2:
        raise InvalidCommandError

    experiment_id = args[0]
    job_tag = args[1]
    endpoint = "experiment"
    url = urljoin(conf_mgr.runner_url, f"{endpoint}/{experiment_id}")
    headers = {"Authorization": f"Bearer {conf_mgr.access_token}"}

    response = requests.get(url=url, headers=headers)
    response_json = response.json()

    # check if the request was successful
    if response_json["status"] != "success":
        raise BadRequestError
    else:
        jobs_list = response_json["experiment"]["jobs"]
        download_url = None
        # loop through the jobs list and find the job with the same tag
        for i in range(len(jobs_list)):
            if job_tag == jobs_list[i]["name"].split("_")[-1]:
                download_url = jobs_list[i]["download_link"]
                model_name = jobs_list[i]["name"]
                task_name = jobs_list[i]["flags"]["task"]
                baseline_model_name = jobs_list[i]["flags"]["model.teacher"]

                if baseline_model_name is None:
                    baseline_model_name = jobs_list[i]["flags"]["model.student"]

                if task_name == "glue":
                    task_name = "sequence_classification"  # tranlate glue to sequence_classification

                # check if the download link is valid
                if download_url is None:
                    raise DownloadLinkNotFoundError
                else:
                    download_url = download_url["link"]
                break

        logger.info("Downloading model")
        try:
            tarfile_path = wget.download(
                download_url, "model_storage"
            )  # response is the path to the downloaded file
        except Exception as e:
            print(e)
            raise DownloadLinkExpiredError

        logger.info("Extracting model to model_storage folder")
        # Extract the tar file to a folder on the local file system
        with tarfile.open(tarfile_path) as tar:
            tar.extractall(path=f"model_storage/{model_name}")

        # delete the tar file
        Path(tarfile_path).unlink()

    logger.info("Pulling image from the server")
    pull_image(
        model_folder_path=f"model_storage/{model_name}/models",
        container_name=f"iris-triton-{experiment_id}",
        job_tag=job_tag,
        task_name=task_name,
        baseline_model_name=baseline_model_name,
    )
    logger.info("All done!")


# --------------------------------------      iris upload     -------------------------------------- #

TQDM = True


def upload_from_file(src, dst):
    with tqdm(
        desc=f"Uploading",
        total=os.path.getsize(src),
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as t:
        with tarify(src, mode="w:gz") as fd:
            fd.seek(0)
            reader_wrapper = CallbackIOWrapper(t.update, fd, "read")
            response = requests.put(dst, data=reader_wrapper)
            response.raise_for_status()
            k = hashlib.md5(fd.getbuffer()).hexdigest()
            return (k, response)


@auth
def upload(name, src, art_type, description):
    endpoint = "artefact"
    url = urljoin(conf_mgr.runner_url, f"{endpoint}/")
    # logger.info(url)
    headers = {"Authorization": f"Bearer {conf_mgr.access_token}"}

    # todo probably better way to parse filepaths
    # Catches if you accidentally put a tilde in quotes:
    if src[0] == "~":
        src = os.path.expanduser(src)

    if not Path(src).is_dir():  # todo test folder with name fish.folder
        raise ArtefactNotFoundError(details=src)

    ext = ".tar.gz"
    if art_type == "model":
        namelist = os.listdir(src)
        if False and not any(".safetensors" in Path(x).suffixes for x in namelist):
            raise UnsafeTensorsError()

    post_req_data = {
        "name": name,
        "artefact_type": art_type,
        "description": description,
        "ext": ext,
        "src": src,
    }
    post_req_response = requests.post(url=url, headers=headers, data=post_req_data)
    if not post_req_response.ok:
        handle_bad_response(post_req_response, endpoint)
    else:
        # dump(response)
        data = post_req_response.json()["artefact"]
        art_uuid = data["uuid"]
        upl_link = data["upload_link"]["link"]

        # todo this is where further format checking would go (e.g. no uploading 10GB files or jpegs...)
        print("Beginning upload...")

    if TQDM:
        hashval, upload_response = upload_from_file(src, upl_link)
    else:
        with tarify(src, mode="w:gz") as f:
            f.seek(0)
            upload_response = requests.put(upl_link, data=f)
            hashval = hashlib.md5(f.getbuffer()).hexdigest()

    if upload_response is not None and upload_response.status_code == 200:
        print(f"Upload Complete -  Validating {art_type} UUID: {art_uuid} ......")
        url = urljoin(conf_mgr.runner_url, f"{endpoint}/{art_uuid}")
        patch_req_response = requests.patch(
            url=url, headers=headers, data={"hashval": hashval}
        )
        if not patch_req_response.ok:
            handle_bad_response(patch_req_response, endpoint)
        else:
            print("Upload validated")
    else:
        print("Upload failed")
        dump(upload_response)
