# encoding: utf-8

from subprocess import Popen, PIPE
from hashids import Hashids
from lib.remove_accents import decode_utf8, remove_accents
import shutil
import codecs
import json

class Certificate:
  def __init__(self, xid, name, cert_type, language=None, speeches=None):
    self.url = ""
    
    if cert_type == "participant":
      str_language = ""
    else:
      str_language = "_" + language

    hash_xid = self.generate_hash(xid)
    
    url = "http://certs.softwarelivre.org/" + hash_xid + ".pdf"
      
    filename = "certificate_" + cert_type + str_language
      
    svg_filename = filename + ".svg"
    
    #create and open the temp svg file
    svg_file = codecs.open("svg/" + svg_filename, "rb", "utf8")
    #substitute the strings with %%
    content = svg_file.read()
    content = content.replace("%%NOME%%", name)
    content = content.replace("%%URL%%", url)
    if cert_type == "speaker":
      str_txt_speeches, str_speeches = self.getSpeeches(speeches, language)      
      content = content.replace("%%PALESTRAS%%", str_speeches)
      content = content.replace("%%TXT_PALESTRAS%%", decode_utf8(str_txt_speeches))
    #save the temp file
    in_file = "/tmp/" + svg_filename
    tmp_file = codecs.open(in_file, "w", "utf8")
    tmp_file.write(content)
    tmp_file.close()
    
    out_file = "pdf/" + hash_xid + ".pdf"
    #convert the temp file to pdf
    pdf_file = self._svg_to_pdf(in_file, out_file)
    self.url = url

  def _svg_to_pdf(self, in_file, out_file=None):
    inkscape = '/usr/bin/inkscape';
    if not out_file:
      out_file = os.path.join(os.path.dirname(in_file), os.path.splitext(os.path.basename(in_file))[0]) + ".pdf";
    p = Popen([inkscape, '-z', '-f', in_file, '-A', out_file], stdin=PIPE, stdout=PIPE);
    p.wait();
    return out_file

  def generate_hash(self, xid):
    hashids = Hashids(min_length=8, salt='asl.org.br')
    ret = hashids.encrypt(int(xid))
    return ret

  def getSpeeches(self, speeches, language):
    items = json.loads(speeches)
    
    if len(items) > 1:
      plural_mode = True
    else:
      plural_mode = False
    
    if language == "BR":
      if plural_mode:
        str_speeches = "as seguintes palestras: "
      else:
        str_speeches = "a seguinte palestra: "
    
    if language == "US":
      if plural_mode:
        str_speeches = "the following speeches: "
      else:
        str_speeches = "the following speech: "
    
    if language == "ES":
      if plural_mode:
        str_speeches = "las siguientes presentaciones: "
      else:
        str_speeches = "la siguiente presentación: "
    
    return [str_speeches, ", ".join(['"' + i + '"' for i in items])]
