#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import route, run, request, response, default_app, jinja2_template, TEMPLATE_PATH, static_file, redirect
import requests
import datetime
import jinja2
import json
import os, sys
import re

env = os.environ

DB_HOST = env.get("DB_URL")
API_HOST = env.get("API_HOST", "localhost")
NOTIFY_URI = env.get("NOTIFY_URI")
SLACK_CHANNEL = env.get("SLACK_CHANNEL", "#general")
TEMPLATE_PATH.append("templates")
API_URI = "http://{}/api".format(API_HOST)
TIMEOUT = 5
name = "anonymous"
_VERSION = "BETA"

def _commentapi(comment=None):
    content = "{}"
    if comment:
        data = {"name":name,"comment":comment}
        response = requests.post(API_URI, data=json.dumps(data), timeout=TIMEOUT)
        content = response.content
    else:
        response = requests.get(API_URI, timeout=TIMEOUT)
        content = response.content
    return json.loads(content)

def _slack(comment, channel):
    if not NOTIFY_URI:
        return None
    try:
        data = {"channel":channel, "data":"Posted message({})".format(comment)}
        print json.dumps(data)
        r = requests.post(NOTIFY_URI,data=json.dumps(data))
    except:
        pass

@route('/app', method=['POST','GET'])
def _root():
    response.content_type = 'text/html;charset=UTF-8'
    if request.method == 'POST':
        comment = request.params.get("comment")
        try:
            if re.findall(r'\<.*\>', comment):
                raise ValueError("Your input was INVALID")
            _commentapi(comment)
            _slack(comment, SLACK_CHANNEL)
        except Exception as e:
            sys.stderr.write(str(e) + "\n")
            return "Registering your comment was failure"
        return redirect("/app")
    else:
        try:
            params = []
            params = _commentapi()
            params['version'] = _VERSION
        except Exception as e:
            sys.stderr.write(str(e) + "\n")
            pass
        return jinja2_template("index.j2", params=params)

@route('/files/<filename:path>')
def static(filename):
    return static_file(filename, root="statics")

@route('/test')
def _test():
    response.content_type = 'text/plain'
    return "test ok"

@route('/version')
def _version():
    response.content_type = 'text/plain'
    return _VERSION

app = default_app()

if __name__ == '__main__':
  port = env.get("APP_PORT", 9002)
  run(host='0.0.0.0', port=port, reloader=True, debug=True)

