# standard library
import datetime

# 3rd party libraries

# project libraries
import core

class Computers(core.CoreDict):
  def __init__(self, manager=None):
    core.CoreDict.__init__(self)
    self._exempt_from_find.append('groups')
    self.manager = manager
    self.log = self.manager.log if self.manager else None

  def get(self):
    # get with no arguments = hostRetrieve() with ALL_HOSTS
    call = self.manager._get_request_format(call='hostDetailRetrieve')
    call['data'] = {
        'hostFilter': {
          'hostGroupID': None,
          'hostID': None,
          'securityProfileID': None,
          'type': 'ALL_HOSTS',
        },
        'hostDetailLevel': 'HIGH'
      }
    response = self.manager._request(call)
    
    if response and response['status'] == 200:
      for computer in response['data']:
        computer_obj = Computer(computer, self.log)
        if computer_obj:
          self[computer_obj.ID] = computer_obj
          # add this computer to any appropriate groups on the Manager()
          if 'hostGroupID' in dir(computer_obj) and computer_obj.hostGroupID:
            if self.manager.computer_groups and self.manager.computer_groups.has_key(computer_obj.hostGroupID):
              self.manager.computer_groups[computer_obj.hostGroupID].computers[computer_obj.ID] = computer_obj

    return len(self)

class ComputerGroups(core.CoreDict):
  def __init__(self, manager=None):
    core.CoreDict.__init__(self)
    self.manager = manager
    self.log = self.manager.log if self.manager else None

  def get(self):
    call = self.manager._get_request_format(call='hostGroupRetrieveAll')
    response = self.manager._request(call)
    if response and response['status'] == 200:
      self.clear() # empty the current groups
      for group in response['data']:
        computer_group_obj = ComputerGroup(group, self.log)
        if computer_group_obj:
          self[computer_group_obj.ID] = computer_group_obj

    return len(self)

class Computer(core.CoreObject):
  def __init__(self, api_response=None, log_func=None):
    if api_response: self._set_properties(api_response, log_func)

class ComputerGroup(core.CoreObject):
  def __init__(self, api_response=None, log_func=None):
    if api_response: self._set_properties(api_response, log_func)
    self.computers = core.CoreDict()