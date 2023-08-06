import os
import shutil
from pathlib import Path
import re

from cloud.model.entry import CloudListResponse, CloudListContext, CloudEntry
from cloud.service.path_manipulation import strip_local_root


class Cloud:
    def __init__(self, root_path):
        self.root_path = Path(root_path)

    def list(self, path) -> CloudListResponse:
        try:
            local_path = self.resolve_path(path)
        except Exception as e:
            print(e)
            raise e

        if not local_path.exists():
            raise FileNotFoundError()

        if local_path.is_file():
            return CloudListResponse(
                entries=[CloudEntry(
                    path=strip_local_root(self.root_path, local_path),
                    name=local_path.name,
                    is_directory=False,
                    size=local_path.stat().st_size
                )],
                context=CloudListContext(path=strip_local_root(self.root_path, local_path), current_page=0, total_pages=1, page_size=1)
            )

        if local_path.is_dir():
            dirs = sorted([p for p in local_path.iterdir() if p.is_dir()])
            files = sorted([p for p in local_path.iterdir() if p.is_file()])

            entries = []

            for d in dirs:
                entries.append(
                    CloudEntry(
                        path=strip_local_root(self.root_path, d),
                        name=d.name,
                        is_directory=True,
                        size=0
                    )
                )

            for f in files:
                entries.append(
                    CloudEntry(
                        path=strip_local_root(self.root_path, f),
                        name=f.name,
                        is_directory=False,
                        size=f.stat().st_size
                    )
                )

            return CloudListResponse(entries=entries, context=CloudListContext(path=strip_local_root(self.root_path, local_path), current_page=0, total_pages=1, page_size=len(entries)))

        raise RuntimeError("Something very strange happened.")

    def read(self, path):
        local_path = self.resolve_path(path)

        if not local_path.exists():
            raise FileNotFoundError()

        if local_path.is_dir():
            raise ValueError(f"{path} is a directory. Can't read a directory as if it were a file.")

        with open(local_path, "rb") as f:
            bytes = f.read()
            return bytes

    def write(self, path, data):
        local_path = self.resolve_path(path)

        os.makedirs(local_path.parent, exist_ok=True)
        with open(local_path, "wb") as f:
            f.write(data)

    def remove(self, path, recursive=False):
        local_path = self.resolve_path(path)

        if local_path == self.root_path:
            raise Exception("You can't delete your root directory.")

        if not local_path.exists():
            raise FileNotFoundError()

        if local_path.is_file():
            os.remove(str(local_path))
        elif local_path.is_dir():
            if recursive:
                shutil.rmtree(str(local_path))
            else:
                raise Exception("Can't remove directory if 'recursive' is false.")


    def clean_path(self, path):
        while path.startswith("/") or path.startswith("\\"):
            path = path[1:]

        return path

    def resolve_path(self, path: str) -> Path:
        to_return = self.root_path.joinpath(str(self.clean_path(path))).resolve()

        if not (self.root_path in to_return.parents or to_return == self.root_path):
            raise FileNotFoundError("that path resolved outside of the root dir.")

        return to_return



if __name__ == '__main__':
    cloud = Cloud(r"C:\Users\Garrett\Documents\BYU\2022_fall\sandbox\storage")
    print(cloud.read("/test.txt"))