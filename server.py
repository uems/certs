# encoding: utf-8

import sys
import traceback

from lib.certs import Certificate
from lib.auth import requires_auth

from flask import Flask, jsonify, request, abort
app = Flask(__name__)

@app.route('/certificate', methods=['POST'])
@requires_auth
def certificate():
  return print_with(Certificate)

def print_with(*klasses):
  try:
    xid        = request.form['xid']
    name       = request.form['name']
    cert_type  = request.form['type']
    language   = request.form.get('language')
    activities = request.form.get('activities')

    for klass in klasses:
      obj = klass(xid, name, cert_type, language, activities, request.url_root)
      object_type = klass.__name__.split('.')[-1]
      ret = {}
      if obj.url is not None:
        ret.update({"url": obj.url});
      else:
        ret.update({"error": obj.error})

    return jsonify(ret)

  except Exception, e:
    response = jsonify({ 'error': e.args, 'stack': traceback.format_exc() })
    response.status_code = 500
    return response

@app.route('/')
def index():
  return jsonify({
    'links': [
      { 'rel': 'certs',    'href': '/certs/',    'method': 'POST' },
    ]
  })

if __name__ == '__main__':
  if len(sys.argv) < 1:
    print "USAGE: python server.py <PORT> <ENV>"
  else:
    app.run(host  = "0.0.0.0",
            port  = int(sys.argv[1]),
            debug = sys.argv[2] == 'debug')

