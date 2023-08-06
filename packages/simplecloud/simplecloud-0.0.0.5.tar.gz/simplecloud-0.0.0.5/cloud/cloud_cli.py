import sys
from argparse import ArgumentParser

from cloud.client import CloudClient


class CloudCLI:
    def __init__(self):
        self.client = CloudClient()

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
            list_response = self.client.ls(args.path)

            dir_count = 0
            file_count = 0
            total_file_size = 0

            entry_lines = []

            for entry in list_response["entries"]:
                if entry["is_directory"]:
                    entry_lines.append(entry["name"] + "/")
                    dir_count += 1
                else:
                    entry_lines.append(f"{entry['name'].ljust(40, ' ')} ({self.get_file_size_string(entry['size'])})")
                    file_count += 1
                    total_file_size += entry['size']

            print("\n-----summary-----")
            print(f"\n\tls {list_response['context']['path']}:")
            print(f"\n\t{dir_count} directories\n\t{file_count} files ({self.get_file_size_string(total_file_size)})")

            print("\n-----entries-----")
            print("\n".join(entry_lines))

        elif args.command == "cp":
            print(self.client.cp(args.src, args.dest))
        elif args.command == "rm":
            print(self.client.rm(args.path, recursive=args.recursive))
        else:
            raise Exception("Bad params.")

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


def main():
    CloudCLI().execute(sys.argv)


if __name__ == '__main__':
    main()
