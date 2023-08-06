import os

from flask import Flask, request
from cloud.service.cloud import Cloud

app = Flask(__name__)

CLOUD_ROOT_PATH = os.getenv("CLOUD_ROOT_PATH")
if CLOUD_ROOT_PATH is None:
    raise EnvironmentError("CLOUD_ROOT_PATH is not set. Please set this environment variable to the root of your storage directory.")

CLOUD_PORT = os.getenv("CLOUD_PORT")
if CLOUD_PORT is None:
    raise EnvironmentError("CLOUD_PORT is not set. Please set this environment variable to specify which port to run your Cloud.")


cloud = Cloud(CLOUD_ROOT_PATH)

@app.route("/read/<path:path>", methods=['GET'])
def read_file(path):
    print(path)
    return cloud.read(path), 200

@app.route("/write/<path:path>", methods=['PUT'])
def write_file(path):
    print(path)
    cloud.write(path=path, data=request.data)
    return "", 200

@app.route("/remove/<path:path>", methods=['DELETE'])
def remove_file(path):
    headers = request.headers

    recursive = bool(headers.get("recursive"))

    try:
        cloud.remove(path, recursive=recursive)
    except FileNotFoundError:
        return f"/{path} not found", 404
    except Exception as e:
        return str(e), 400

    return "", 200


@app.route("/list", methods=['GET'])
@app.route("/list/", methods=['GET'])
@app.route("/list/<path:path>", methods=['GET'])
def list(path=""):
    print(f"REQUESTED PATH: \"{path}\"")

    try:
        return cloud.list(path=path), 200
    except FileNotFoundError:
        return f"/{path} not found", 404
    except Exception as e:
        return str(e), 400


def main():
    from waitress import serve
    print(f"Server listening on port {CLOUD_PORT}")
    serve(app, port=CLOUD_PORT)


if __name__ == '__main__':
    main()

