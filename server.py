# encoding: utf-8

import sys
import traceback

from lib.certificate import Certificate

from flask import Flask, jsonify, request, abort
app = Flask(__name__)

@app.route('/certificate', methods=['POST'])
def certificate():
  return print_with(Certificate)

def print_with(*klasses):
  try:
    xid       = request.form['xid']
    name      = request.form['name']
    cert_type = request.form['type']
    language  = request.form.get('language')
    speeches  = request.form.get('speeches')

    messages = [];

    for klass in klasses:
      obj = klass(xid, name, cert_type, language, speeches)
      object_type = klass.__name__.split('.')[-1]
      messages.append("{} has been printed".format(object_type));
      messages.append("{}".format(obj.url));

    return jsonify({ 'messages' : messages })

  except Exception, e:
    response = jsonify({ 'error': e.args, 'stack': traceback.format_exc() })
    response.status_code = 500
    return response

@app.route('/')
def index():
  return jsonify({
    'links': [
      { 'rel': 'certificate',    'href': '/certificate/',    'method': 'POST' },
    ]
  })

if __name__ == '__main__':
  if len(sys.argv) < 1:
    print "USAGE: python server.py <PORT> <ENV>"
  else:
    app.run(host  = "0.0.0.0",
            port  = int(sys.argv[1]),
            debug = sys.argv[2] == 'debug')

