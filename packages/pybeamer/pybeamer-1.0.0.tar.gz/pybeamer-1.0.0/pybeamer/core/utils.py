
__all__ = ['retrieve_kw', 'checkForUnusedVars', 'ensureExtension', 'Holder']


def retrieve_kw( kw, key, default = None ):
  if not key in kw or kw[key] is None:
    kw[key] = default
  return kw.pop(key)


def checkForUnusedVars(d, fcn = None):
  """
    Checks if dict @d has unused properties and print them as warnings
  """
  for key in d.keys():
    if d[key] is None: continue
    msg = 'Obtained not needed parameter: %s' % key
    if fcn:
      fcn(msg)
    else:
      print('WARNING:%s' % msg)

def ensureExtension( filename, extension ):
    return (filename + '.' + extension) if not filename.endswith(extension) else filename



class Holder( object ):
  """
  A simple object holder
  """
  def __init__(self, obj = None, replaceable = True):
    self._obj = obj
    self._replaceable = replaceable
  def __call__(self):
    return self._obj
  def isValid(self):
    return self._obj not in (None, NotSet)
  def set(self, value):
    if self._replaceable or not self.isValid():
      self._obj = value
    else:
      raise RuntimeError("Cannot replace held object.")