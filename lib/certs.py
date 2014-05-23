# encoding: utf-8

from subprocess import Popen, PIPE
from lib.remove_accents import decode_utf8, remove_accents
import shutil
import hashlib
import codecs
import json
import config
import os.path
import urlparse

class Certificate:
  def __init__(self, xid, name, cert_type, language=None, activities=None, url_root=None):
    self.url = None
    self.error = None

    if cert_type == "participant":
      str_language = ""
    else:
      str_language = "_" + language

    hash_xid = self.generate_hash(xid)

    parsed = urlparse.urlparse(url_root)
    url = parsed.scheme + "://" + parsed.hostname + "/" + hash_xid + ".pdf"

    filename = "certificate_" + cert_type + str_language

    svg_filename = filename + ".svg"

    template_path = os.path.join(config.svg_path, svg_filename)
    svg_file = codecs.open(template_path, "rb", "utf8")

    content = svg_file.read()
    content = content.replace("%%NOME%%", name)
    content = content.replace("%%URL%%", url)
    if cert_type == "speaker":
      str_txt_activities, str_activities = self.getActivities(activities, language)
      content = content.replace("%%PALESTRAS%%", str_activities)
      content = content.replace("%%TXT_PALESTRAS%%", decode_utf8(str_txt_activities))

    in_file = os.path.join("/tmp", hash_xid + ".svg")
    tmp_file = codecs.open(in_file, "w", "utf8")
    tmp_file.write(content)
    tmp_file.close()

    out_file = os.path.join(config.output_path, hash_xid + ".pdf")
    pdf_file = self._svg_to_pdf(in_file, out_file)
    if os.path.isfile(out_file):
      self.url = url
    else:
      self.error = "pdf not generated"

  def _svg_to_pdf(self, in_file, out_file):
    inkscape = '/usr/bin/inkscape'
    p = Popen([inkscape, '-z', '-f', in_file, '-A', out_file], stdin=PIPE, stdout=PIPE)
    p.wait()
    return out_file

  def generate_hash(self, xid):
    ret = hashlib.sha224(xid).hexdigest()[:8]
    return ret

  def getActivities(self, activities, language):
    items = json.loads(activities)

    if len(items) > 1:
      plural_mode = True
    else:
      plural_mode = False

    if language == "BR":
      if plural_mode:
        str_activities = "as seguintes palestras: "
      else:
        str_activities = "a seguinte palestra: "

    if language == "US":
      if plural_mode:
        str_activities = "the following talks: "
      else:
        str_activities = "the following talk: "

    if language == "ES":
      if plural_mode:
        str_activities = "las siguientes charlas: "
      else:
        str_activities = "la siguiente charla: "

    return [str_activities, ", ".join(['"' + i + '"' for i in items])]
