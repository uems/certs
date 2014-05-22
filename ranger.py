# encoding: utf-8

import sys
import requests
import codecs

sys.stdout = codecs.open('/dev/stdout', 'w', 'utf8')
endpoint = "http://192.168.33.20:2000"
headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6dHJ1ZSwiaWF0IjoxNDAwMDcyMTg4fQ.UVPYiY8AtIlASXtSNPrEaiHU2Ehu2wDKktI137iQTqc'}

class RangerException(BaseException): pass
class PersonNotFound(RangerException): pass

class Process:
  def __init__(self, id, source):
    self.url = "{}/people/{}-{}".format(endpoint, source, id)

    self.locate_person()
    self.reset_login_hash()
    self.call_for_certificate()

  def reset_login_hash(self):
    print 'hitting post reset-login-hash'
    response = requests.post("{}/reset-login-hash".format(self.url), headers=headers)
    print response.status_code

  def call_for_certificate(self):
    print 'hitting post call-for-certificate'
    response = requests.post("{}/call-for-certificate".format(self.url), headers=headers)
    print response.status_code

  def locate_person(self):
    print "hitting GET", self.url
    response = requests.get(self.url, headers=headers)

    print response.status_code
    if response.status_code >= 400:
      print "PERSON NOT FOUND! skipping"
      raise PersonNotFound()
    self.person = response.json()

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
