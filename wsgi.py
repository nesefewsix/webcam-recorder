import calendar
import os
from datetime import datetime

import requests
from flask import Flask, send_from_directory, request

from webcam_recorder import WebcamRecorder

app = Flask(__name__)
wcd_rec = WebcamRecorder(users=["ohbabyy_"])


@app.route("/usernames")
def get_users():
    return wcd_rec.get_users()


@app.route("/downloads")
def get_recordings():
    return wcd_rec.get_files()


@app.route("/delete")
def delete_file():
    args = request.args

    if args.get("path"):
        wcd_rec.delete_file(args.get("path"))
        return {"message": "success"}

    return {"message": "fail"}


@app.route('/download')
def download_file():
    args = request.args

    directory = args.get("dir")
    name = args.get("name")

    if directory and name:
        try:
            return send_from_directory(directory=directory, path=name, as_attachment=True)
        except Exception as e:
            return {"message": f"{e}"}

    return {"message": "missing parameters"}


@app.route('/double_ping')
def keep_me_alive():
    args = request.args

    url1 = args.get("a")
    url2 = args.get("b")

    if url1 and url2:
        now = datetime.now()
        url = url1 if calendar.monthrange(now.year, now.month)[1] // 2 > now.day else url2

        try:
            requests.head(url)
            return {"message": "success", "url": url}
        except Exception as e:
            return {"message": str(e), "url": url}

    return {"message": "missing parameters"}


@app.route("/")
def index():
    return f"webcam-recorder is working"


if __name__ == "__main__":
    app.run()
