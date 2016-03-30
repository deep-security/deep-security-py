# standard library
import datetime

# 3rd party libraries

# project libraries
import core

class CloudAccounts(core.CoreDict):
  def __init__(self, manager=None):
    core.CoreDict.__init__(self)
    self.manager = manager
    self.log = self.manager.log if self.manager else None

  def get(self): pass

  def add(self): pass

class CloudAccount(core.CoreObject):
  def __init__(self, manager=None, api_response=None, log_func=None):
    self.manager = manager
    if api_response: self._set_properties(api_response, log_func)