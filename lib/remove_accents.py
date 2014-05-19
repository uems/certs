import unicodedata

def remove_accents(value):
  if not isinstance(value,unicode):
    value = decode_utf8(value)
  nkfd_form = unicodedata.normalize('NFKD', value);
  only_ascii = nkfd_form.encode('ASCII', 'ignore')
  return only_ascii

def decode_utf8(string):
   if isinstance(string, str):
       for encoding in (('utf-8',), ('windows-1252',), ('utf-8', 'ignore')):
           try:
               return string.decode(*encoding)
           except:
               pass
       return string # Don't know how to handle it...
   return unicode(string, 'utf-8')
