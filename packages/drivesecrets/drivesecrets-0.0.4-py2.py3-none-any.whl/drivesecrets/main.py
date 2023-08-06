#!/usr/bin/env python3

import logging
import os
from typing import Iterable

from google.colab import drive

log = logging.getLogger(__name__)

GDRIVE_MOUNT_POINT = "/content/gdrive"
DEFAULT_BASE_DIRECTORY_CANDIDATES = (
    "/content/gdrive/MyDrive",
    "/content/gdrive/My Drive",
)


def get_secret(
    filename: str,
    base_directory_candidates: Iterable[str] = DEFAULT_BASE_DIRECTORY_CANDIDATES,
) -> str:
    drive.mount(GDRIVE_MOUNT_POINT)

    for base_directory_candidate in base_directory_candidates:
        log.debug(f"Checking for Google Drive directory: {base_directory_candidate}")
        if os.path.isdir(base_directory_candidate):
            log.debug(f"Found Google Drive directory: {base_directory_candidate}")
            google_drive_base = base_directory_candidate
            break
    else:
        raise FileNotFoundError(
            "Could not find a valid Google Drive directory. Tried {base_directory_candidates}"
        )

    secret_path = os.path.join(google_drive_base, filename)

    if os.path.exists(secret_path):
        log.info(f"Found secret at {secret_path}. Returning it now.")
        with open(secret_path, "r") as f:
            return f.read()

    log.info("Secret not found. Creating one now.")

    secret_to_store = input(
        "Insert the secret you'd like to save and press Enter to continue...\n"
    )

    with open(secret_path, "w") as f:
        f.write(secret_to_store)
        log.info("Secret saved.")

    return secret_to_store
