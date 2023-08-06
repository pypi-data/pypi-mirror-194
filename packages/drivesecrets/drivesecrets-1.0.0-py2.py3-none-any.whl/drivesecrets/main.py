#!/usr/bin/env python3

import logging
import os
from typing import Iterable

from google.colab import drive

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

GDRIVE_MOUNT_POINT = "/content/gdrive"
DEFAULT_BASE_DIRECTORY_CANDIDATES = (
    "/content/gdrive/MyDrive",
    "/content/gdrive/My Drive",
)


def get_secret(
    filename: str,
    base_directory_candidates: Iterable[str] = DEFAULT_BASE_DIRECTORY_CANDIDATES,
    gdrive_mount_point: str = GDRIVE_MOUNT_POINT,
) -> str:
    drive.mount(gdrive_mount_point)

    for base_directory_candidate in base_directory_candidates:
        assert base_directory_candidate.startswith(
            GDRIVE_MOUNT_POINT
        ), "Base directory candidates must be subdirectories of the gdrive mount point."
        assert isinstance(base_directory_candidate, str)

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
        print(f"Found secret at {secret_path}.")
        with open(secret_path, "r") as f:
            return f.read()

    print("Secret not found. Creating one now.")

    secret_to_store = input(
        "Insert the secret you'd like to save and press Enter to continue...\n"
    )

    with open(secret_path, "w") as f:
        f.write(secret_to_store)
        print("Secret saved.")
        for color in ("\033[91m", "\033[92m", "\033[94m"):
            print(
                color + "\x1B[1m" + "Please delete the output of this cell." + "\x1b[0m"
            )

    return secret_to_store
