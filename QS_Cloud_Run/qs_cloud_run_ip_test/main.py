from flask import Flask, jsonify
import urllib.request


app = Flask(__name__)


@app.route("/")
def main():
    end_point = 'https://4hsinyili-ufc.xyz/test_ip'
    urllib.request.urlopen(end_point)
    return jsonify({"data": 'success'})
