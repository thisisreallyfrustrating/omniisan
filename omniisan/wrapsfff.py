import os
import subprocess
import json


def download(url, output_directory):
    args = [
        "fanficfare",
        "-j",  # output json
        "-c",
        "../fanficfare_config.ini",
        url,
    ]

    old_cwd = os.getcwd()
    os.chdir(output_directory)
    try:
        process = subprocess.run(args, timeout=120, capture_output=True)
    finally:
        os.chdir(old_cwd)

    if process.returncode == 0:
        return True, json.loads(process.stdout)["output_filename"]
    else:
        return False, {}
