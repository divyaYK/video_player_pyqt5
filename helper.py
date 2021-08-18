import re
def atoi(text):
  if text.isnumeric():
    return int(text)
  else:
    return text

def natural_keys(text):
  return [ atoi(c) for c in re.split('(\d+)',text) ]