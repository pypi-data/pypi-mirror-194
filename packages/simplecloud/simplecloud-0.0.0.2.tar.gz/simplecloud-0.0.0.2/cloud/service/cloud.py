import os
import shutil
from pathlib import Path


class Cloud:
    def __init__(self, root_path):
        self.root_path = Path(root_path)

    def list(self, path):
        local_path = self.resolve_path(path)

        if not local_path.exists():
            raise FileNotFoundError()

        if local_path.is_file():
            return local_path.name + f"\t({self.get_file_size_string(local_path.stat().st_size)})"

        if local_path.is_dir():
            dir_header = f"DIRECTORY LISTING FOR /{path}:"
            dirs = [p for p in local_path.iterdir() if p.is_dir()]
            files = [p for p in local_path.iterdir() if p.is_file()]

            dir_lines = "\n".join([f"{p.name}/" for p in dirs])
            file_tuples = [(p.name, self.get_file_size_string(p.stat().st_size)) for p in files]

            max_file_size_len = max([0] + [len(t[0]) for t in file_tuples])
            w = max_file_size_len

            print(w)

            file_lines = [f"{t[0].ljust(w, ' ')}  ({t[1]})" for t in file_tuples]

            return dir_header + "\n\n" + dir_lines + "\n\n" + "\n".join(file_lines)

        return ""

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

    def get_file_size_string(self, size_bytes):
        KB = 1024
        MB = KB * 1024
        GB = MB * 1024
        if size_bytes < KB:
            return f"{size_bytes} bytes"
        elif size_bytes < MB:
            return f"{round(size_bytes / KB, 2)} KB"
        elif size_bytes < GB:
            return f"{round(size_bytes / MB, 2)} MB"
        else:
            return f"{round(size_bytes / GB, 2)} GB"



if __name__ == '__main__':
    cloud = Cloud(r"C:\Users\Garrett\Documents\BYU\2022_fall\sandbox\storage")
    print(cloud.read("/test.txt"))