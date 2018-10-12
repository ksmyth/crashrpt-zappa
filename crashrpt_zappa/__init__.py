import re
import zipfile
import xml.etree.ElementTree
import six
import boto3
import botocore
from flask import Flask, Response, abort, send_file, request
import tempfile
from cgi import escape
import shutil

app = Flask(__name__)

s3 = boto3.resource('s3')
s3_bucket = 'gme-crashrpts'


@app.route("/")
def root():
    return "crashrpt"


@app.route("/crashrpt", methods=['POST'])
def crashrpt():
    guid = request.form['crashguid']
    tmpdir = tempfile.mkdtemp()
    try:
        tmpfile = "{}/{}.zip".format(tmpdir, guid)
        request.files['crashrpt'].save(tmpfile)

        with open(tmpfile, 'rb') as data:
            s3.Bucket(s3_bucket).put_object(Key='{}.zip'.format(guid), Body=data)
    finally:
        shutil.rmtree(tmpdir)
    return 'ok'


if __name__ == "__main__":
    # app.run()
    app.run(port=5000, debug=True, host='0.0.0.0', use_reloader=False)
