import os
import sys
from argparse import ArgumentParser
import requests
from pathlib import Path

from cloud.service.path_manipulation import CLOUD_PROTOCOL, is_cloud_path, is_cloud_file, is_cloud_dir, strip_cloud_protocol


class CloudCLI:
    def __init__(self):
        self.api_url = os.getenv("CLOUD_API_URL")
        if self.api_url is None:
            raise EnvironmentError(
                "CLOUD_API_URL is not set. Please set this environment variable to the URL where your cloud is running.")

        while self.api_url.endswith("/"):
            self.api_url = self.api_url[:-1]

    def ls(self, path):
        if len(path) > 0 and not is_cloud_path(path):
                raise SyntaxError(f"Path does not start with {CLOUD_PROTOCOL}")

        cloudpath = path if len(path) < len(CLOUD_PROTOCOL) else strip_cloud_protocol(path)

        try:
            res = requests.get(f"{self.api_url}/list/{cloudpath}")
            print(res.content.decode("utf-8"))
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

        print(f"Copied {source} to {dest}")

    def rm(self, path, recursive=False):
        if not is_cloud_path(path):
            raise ValueError(f"{path} is not a cloud path. Can't remove non-(cloud://) paths")

        cloudpath = strip_cloud_protocol(path)

        try:
            res = requests.delete(f"{self.api_url}/remove/{cloudpath}", headers={"recursive": "true" if recursive else ""})
            print(res.status_code, res.text)
        except Exception as e:
            raise e

    def read_file(self, path: str) -> bytes:
        if is_cloud_path(path):

            if not is_cloud_file(path):
                raise ValueError(f"{path} is a cloud path, but not a cloud file. Can't read non-file cloud paths")

            # download
            cloudpath = strip_cloud_protocol(path)
            res = requests.get(f"{self.api_url}/read/{cloudpath}")

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
            print(res.text)
        else:
            # write to local
            local_path = Path(path).resolve()

            os.makedirs(local_path.parent, exist_ok=True)

            with open(local_path, "wb") as f:
                f.write(file)



    def execute(self, argv):
        parser = ArgumentParser(prog="cloud", add_help=False)

        parser.add_argument("command", type=str)

        subparsers = parser.add_subparsers(help="commands", dest="command")

        ls_parser = subparsers.add_parser("ls", help="ls help")
        ls_parser.add_argument("path", nargs="?", default="", type=str)

        cp_parser = subparsers.add_parser("cp", help="cp help")
        cp_parser.add_argument("src", type=str, help="source file path")
        cp_parser.add_argument("dest", type=str, help="destination file path")

        rm_parser = subparsers.add_parser("rm", help="rm help")
        rm_parser.add_argument("path", type=str)
        rm_parser.add_argument("-r", "--recursive", action="store_true")

        args = parser.parse_args(argv)

        if args.command == "ls":
            self.ls(args.path)
        elif args.command == "cp":
            self.cp(args.src, args.dest)
        elif args.command == "rm":
            self.rm(args.path, recursive=args.recursive)
        else:
            raise Exception("Bad params.")

def main():
    CloudCLI().execute(sys.argv)

if __name__ == '__main__':
    main()