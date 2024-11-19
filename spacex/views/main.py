from flask import Flask, send_from_directory

app = Flask(__name__)



@app.route("/<path:file_path>")
def serve_file2(file_path):
    try:
        return send_from_directory("", file_path)
    except FileNotFoundError:
        return "File not found", 404


@app.route("/")
def serve_file3():
    try:
        return send_from_directory("", "index.html")
    except FileNotFoundError:
        return "File not found", 404


if __name__ == '__main__':
    app.run(host='localhost', port=5000)

