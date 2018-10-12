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
import requests

app = Flask(__name__)

s3 = boto3.resource('s3')
s3_bucket = 'gme-crashrpts'
SENDGRID_APIKEY = ''

@app.route("/")
def root():
    return "crashrpt"


def email(guid):
    data = {
          "personalizations": [
            {
              "to": [
                {
                  "email": "ksmyth@metamorphsoftware.com"
                }
              ],
              "subject": "GME CrashRpt"
            }
          ],
          "from": {
            "email": "ksmyth@metamorphsoftware.com"
          },
          "content": [
            {
              "type": "text/plain",
              "value": "https://s3.us-east-2.amazonaws.com/{}/{}.zip".format(s3_bucket, guid)
            }
          ]
        }
    response = requests.post('https://api.sendgrid.com/v3/mail/send', json=data,
        headers={'Authorization': 'Bearer {}'.format(SENDGRID_APIKEY)})


@app.route("/crashrpt", methods=['POST'])
def crashrpt():
    guid = request.form['crashguid']
    s3.Bucket(s3_bucket).put_object(Key='{}.zip'.format(guid), Body=request.files['crashrpt'].stream)
    email(guid)
    return 'ok'


if __name__ == "__main__":
    # app.run()
    app.run(port=5000, debug=True, host='0.0.0.0', use_reloader=False)
