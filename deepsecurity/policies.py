# standard library
import datetime

# 3rd party libraries

# project libraries
import core

class Policies(core.CoreDict):
  def __init__(self, manager=None):
    core.CoreDict.__init__(self)
    self.manager = manager
    self.log = self.manager.log if self.manager else None

  def get(self):
    """
    Get all of the policies from Deep Security
    """
    call = self.manager._get_request_format(call='securityProfileRetrieveAll')
    response = self.manager._request(call)
    
    if response and response['status'] == 200:
      if not type(response['data']) == type([]): response['data'] = [response['data']]
      for policy in response['data']:
        policy_obj = Policy(self.manager, policy, self.log)
        if policy_obj:
          self[policy_obj.ID] = policy_obj
          
    return len(self)

class Policy(core.CoreObject):
  def __init__(self, manager=None, api_response=None, log_func=None):
    self.manager = manager
    if api_response: self._set_properties(api_response, log_func)