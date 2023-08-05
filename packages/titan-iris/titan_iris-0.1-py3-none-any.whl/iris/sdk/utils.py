"""
This file contains the helper functions for the Iris package
"""
import hashlib

# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import io
import tarfile
import docker
import json
from rich.progress import Progress
from .conf_manager import conf_mgr


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                         Utils                                                        #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

# --------------------------------  Helper Function for Iris Pull   ------------------------------ #


def tarify(local_folder_path: str, mode="w"):  # use mode="w:gz" for .tar.gz
    # Create a tar archive of the local folder
    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode=mode) as tar:
        tar.add(local_folder_path, arcname=".")
    return tar_buffer


def copy_local_folder_to_image(
    container, local_folder_path: str, image_folder_path: str
) -> None:
    """Helper function to copy a local folder into a container"""
    tar_buffer = tarify(local_folder_path)
    tar_buffer.seek(0)

    # Copy the tar archive into the container
    container.put_archive(image_folder_path, tar_buffer)


def show_progress(line, progress, tasks):  # sourcery skip: avoid-builtin-shadow
    """
    Show task progress for docker pull command (red for download, green for extract)
    """
    if line["status"] == "Downloading":
        id = f'[red][Download {line["id"]}]'
    elif line["status"] == "Extracting":
        id = f'[green][Extract  {line["id"]}]'
    else:
        # skip other statuses
        return

    if id not in tasks.keys():
        tasks[id] = progress.add_task(f"{id}", total=line["progressDetail"]["total"])
    else:
        progress.update(tasks[id], completed=line["progressDetail"]["current"])


def pull_image(
    model_folder_path: str,
    container_name: str,
    job_tag: str,
    task_name: str,
    baseline_model_name: str,
):
    """
    This function handles the logic of pulling the base image and creating a new image with the model files copied into it
    """
    temp_container_name = "temp-iris-triton"

    env_var = {"TASK_NAME": task_name, "BASELINE_MODEL_NAME": baseline_model_name}

    tasks = {}
    with Progress() as progress:
        # docker pull the base image
        client = docker.from_env()
        resp = client.api.pull(conf_mgr.BASE_IMAGE, stream=True, decode=True)
        for line in resp:
            show_progress(line, progress, tasks)

    # Create a new temp container
    container = client.containers.create(
        image=conf_mgr.BASE_IMAGE, name=temp_container_name, environment=env_var
    )

    copy_local_folder_to_image(
        container, model_folder_path, "/usr/local/triton/models/"
    )

    # Commit the container to a new image
    container.commit(repository=container_name)

    client.images.get(container_name).tag(f"{container_name}:{job_tag}")

    # Remove the original tag
    client.images.remove(container_name)
    # Remove the temp container
    container.remove()


# View a json response
def dump(response):
    print(
        json.dumps(
            {"status": response.status_code, "response": json.loads(response.text)},
            indent=4,
        )
    )
