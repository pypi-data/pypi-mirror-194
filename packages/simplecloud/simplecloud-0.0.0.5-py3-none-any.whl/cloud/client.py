import os
from pathlib import Path

import requests
import json

from cloud.model.entry import CloudListResponse
from cloud.service.path_manipulation import CLOUD_PROTOCOL, is_cloud_path, is_cloud_file, is_cloud_dir, strip_cloud_protocol


class CloudClient:
    def __init__(self):
        self.api_url = os.getenv("CLOUD_API_URL")
        if self.api_url is None:
            raise EnvironmentError(
                "CLOUD_API_URL is not set. Please set this environment variable to the URL where your cloud is running.")

        while self.api_url.endswith("/"):
            self.api_url = self.api_url[:-1]

    def ls(self, path) -> CloudListResponse:
        if len(path) > 0 and not is_cloud_path(path):
                raise SyntaxError(f"Path does not start with {CLOUD_PROTOCOL}")

        cloudpath = path if len(path) < len(CLOUD_PROTOCOL) else strip_cloud_protocol(path)

        try:
            res = requests.get(f"{self.api_url}/list/{cloudpath}")
            res.raise_for_status()

            return json.loads(res.content.decode("utf-8"))
        except Exception as e:
            raise e

    def cp(self, source: str, dest: str):
        dest_is_cloud = is_cloud_path(dest)

        src_file = self.read_file(source)

        if not dest_is_cloud:
            dest_path = Path(dest).resolve()
            if dest_path.exists() and dest_path.is_dir():
                dest_path = dest_path.joinpath(Path(source).name)
                dest = str(dest_path)

        self.write_file(dest, Path(source).name, src_file)

        return f"Copied {source} to {dest}"

    def rm(self, path, recursive=False) -> str:
        if not is_cloud_path(path):
            raise ValueError(f"{path} is not a simplecloud path. Can't remove non-({CLOUD_PROTOCOL}) paths")

        cloudpath = strip_cloud_protocol(path)

        try:
            res = requests.delete(f"{self.api_url}/remove/{cloudpath}", headers={"recursive": "true" if recursive else ""})
            res.raise_for_status()

            return res.text
        except Exception as e:
            raise e

    def read_file(self, path: str) -> bytes:
        if is_cloud_path(path):

            if not is_cloud_file(path):
                raise ValueError(f"{path} is a cloud path, but not a cloud file. Can't read non-file cloud paths")

            # download
            cloudpath = strip_cloud_protocol(path)
            res = requests.get(f"{self.api_url}/read/{cloudpath}")
            res.raise_for_status()

            return res.content
        else:
            # read from local
            resolved_path = Path(path).resolve()

            if resolved_path.exists() and resolved_path.is_file():
                with open(resolved_path, "rb") as f:
                    return f.read()

        raise Exception("Something went wrong")

    def write_file(self, path: str, filename: str, file: bytes) -> None:
        if is_cloud_path(path):
            if is_cloud_dir(path):
                path += filename

            # upload
            cloudpath = strip_cloud_protocol(path)

            res = requests.put(f"{self.api_url}/write/{cloudpath}", data=file)
            res.raise_for_status()
        else:
            # write to local
            local_path = Path(path).resolve()

            os.makedirs(local_path.parent, exist_ok=True)

            with open(local_path, "wb") as f:
                f.write(file)