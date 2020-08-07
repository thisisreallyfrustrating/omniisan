import os
import subprocess
import json


def download(url, output_directory, fanficfare_location="fanficfare"):
    args = [
        fanficfare_location,
        "-j",  # output json
        "-c",
        "../fanficfare_config.ini",
        url,
    ]

    old_cwd = os.getcwd()
    os.chdir(output_directory)
    try:
        process = subprocess.run(args, timeout=480, capture_output=True)
    except subprocess.TimeoutExpired:
        return False, {"message": "Your request took too long and was abandoned."}
    finally:
        os.chdir(old_cwd)

    if process.returncode == 0:
        return True, json.loads(process.stdout)["output_filename"]
    else:
        return False, {"message": "Mystery fanficfare error."}
