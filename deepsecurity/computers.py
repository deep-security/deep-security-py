# standard library
import datetime

# 3rd party libraries

# project libraries
import core

class Computers(core.CoreDict):
  def __init__(self):
    core.CoreDict.__init__(self)
    self._exempt_from_find.append('groups')

  def get(self):
    # get with no arguments = hostRetrieve() with ALL_HOSTS
    pass

class Computer(object):
  def __init__(self): pass