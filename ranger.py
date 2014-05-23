# encoding: utf-8

import sys
import requests
import codecs
import config

sys.stdout = codecs.open('/dev/stdout', 'w', 'utf8')
endpoint = config.endpoint
headers = {'Authorization': config.authorization_jwt}

class RangerException(BaseException): pass
class ResetLoginHashFailed(BaseException): pass
class CallForCertificateFailed(BaseException): pass
class PersonNotFound(RangerException): pass

class Process:
  def __init__(self, id, source):
    self.url = "{}/people/{}-{}".format(endpoint, source, id)

    self.locate_person()
    self.reset_login_hash()
    self.call_for_certificate()

  def reset_login_hash(self):
    url = "{}/reset-login-hash".format(self.url)
    print 'hitting POST', url,
    response = requests.post(url, headers=headers)

    if response.status_code >= 400:
        print response.status_code, response.body
        raise ResetLoginHashFailed();
    print "OK"

  def call_for_certificate(self):
    url = "{}/call-for-certificate".format(self.url)
    print 'hitting POST', url,
    response = requests.post(url, headers=headers)

    if response.status_code >= 400:
        print response.status_code, response.body
        raise CallForCertificateFailed();
    print "OK"

  def locate_person(self):
    print "hitting GET", self.url,
    response = requests.get(self.url, headers=headers)

    if response.status_code >= 400:
      print response.status_code, "PERSON NOT FOUND! skipping"
      raise PersonNotFound()
    self.person = response.json()
    print "OK"

if __name__ == "__main__":
  if len(sys.argv) < 4:
    print "USAGE: python ranger.py <SOURCE> <FIRST> <LAST>"
    exit(1)

  source  = sys.argv[1];
  first   = int(sys.argv[2])
  last    = int(sys.argv[3])
  results = { 'OK': 0 }

  for id in range(first, last+1):
    try:
      print "-------------------"
      print "iniciando id", id
      p = Process(id, source);
      results['OK'] += 1
    except RangerException, e:
      name = repr(e).split(".")[-1]
      print "*****", name
      if name not in results:
        results[name] = 0
      results[name] += 1
    except Exception, e:
      name = repr(e).split(".")[-1]
      print "**** ****", name, "**** ****"
      if name not in results:
        results[name] = []
      results[name].append(id)

  print results
