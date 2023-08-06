import re
from pathlib import Path

CLOUD_PROTOCOL = "sc://"


def is_cloud_path(path: str) -> bool:
    return path.startswith(CLOUD_PROTOCOL)


def is_cloud_file(path: str) -> bool:
    return is_cloud_path(path) and not path.endswith("/")


def is_cloud_dir(path: str) -> bool:
    return is_cloud_path(path) and path.endswith("/")


def strip_cloud_protocol(path: str) -> str:
    if not is_cloud_path(path):
        raise ValueError(f"{path} is not a cloud path.")

    cloudpath = re.sub(CLOUD_PROTOCOL, "", path)

    while cloudpath.startswith("/"):
        cloudpath = cloudpath[1:]

    return cloudpath

def strip_local_root(local_root: Path, path: Path) -> str:

    parts = list(path.parts)

    for p in local_root.parts:
        if p == parts[0]:
            parts.pop(0)
        else:
            raise RuntimeError(f"Tried to remove the root from a path that was outside the root.\n\tRoot: {local_root}\n\tPath: {path}")

    return "/" + "/".join(parts)
