# Copyright (c) 2021, Ethan Henderson
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import json
import logging
import os
from urllib import request
from urllib.error import HTTPError

from nusex import CONFIG_DIR

from ..errors import InitFailure

REPO_URL = "https://github.com/nusex/downloads"
RAW_URL = "https://raw.githubusercontent.com"
TEMPLATE_SUFFIX = "tree/main/templates0x"


def _find_templates():
    files = []
    try:
        with request.urlopen(f"{REPO_URL}/{TEMPLATE_SUFFIX}") as r:
            data = r.readlines()
    except HTTPError as exc:
        raise InitFailure(
            f"unable to locate templates (GitHub returned {exc.code})"
        )

    for i, line in enumerate(data):
        if b'role="rowheader"' in line:
            logging.debug(f"Parsing line {i + 1}: {data[i + 1].decode()}")
            path = data[i + 1].split(b'"')[-2].decode()
            if path.endswith(".nsx"):
                files.append("".join(path.split("blob/")))

    return files


def _get_user_details():
    print(
        "🔔 Welcome to nusex! Some info is needed in order to properly "
        "create templates."
    )
    author = input("🎤 Author name: ")
    email = input("🎤 Author email: ")
    repo_user_url = input("🎤 Git repository user URL: ")
    return author, email, repo_user_url.strip("/")


def _create_config_files(author, email, repo_user_url):
    print("⌛ Creating user config files...", end="")
    os.makedirs(CONFIG_DIR, exist_ok=True)

    config = {
        "default_version": "0.1.0",
        "default_description": "My project, created using nusex",
        "repo_user_url": repo_user_url,
        "author": author,
        "author_email": email,
        "default_license": "BSD 3-Clause",
    }
    with open(CONFIG_DIR / "user.nsc", "w") as f:
        json.dump(config, f, ensure_ascii=False)

    print(" done")


def _download_templates():
    print("⌛ Downloading templates... 0%", end="\r")
    files = _find_templates()
    step = 100 / len(files)

    try:
        for i, f in enumerate(files):
            with request.urlopen(f"{RAW_URL}/{f}") as r:
                with open(CONFIG_DIR / f.split("/")[-1], "w") as f:
                    f.write(r.read().decode())

            print(
                f"⌛ Downloading templates... {step * (i + 1):.0f}%", end="\r"
            )
    except HTTPError as exc:
        raise InitFailure(
            f"unable to download templates (GitHub returned {exc.code})"
        )


def run():
    if not os.path.isdir(CONFIG_DIR):
        details = _get_user_details()
        _create_config_files(*details)
    else:
        print(
            "🔔 Skipping user config. To find out how to update your config, "
            "run `nsx config -h`."
        )

    _download_templates()
    print(
        "\n🎉 Initialisation complete! You can run this command any time to "
        "get the latest premade templates."
    )


def setup(subparsers):
    subparsers.add_parser("init", description="Initialise nusex.")
    return subparsers
