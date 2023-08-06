import re

CLOUD_PROTOCOL = "cloud://"


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
