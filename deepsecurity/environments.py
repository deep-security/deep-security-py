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

  def get(self):
    """
    Get a list of all of the current configured cloud accounts
    """
    call = self.manager._get_request_format(api=self.manager.API_TYPE_REST, call='cloudaccounts')
    response = self.manager._request(call)
    if response and response['status'] == 200:
      if response['data'] and response['data'].has_key('cloudAccountListing') and response['data']['cloudAccountListing'].has_key('cloudAccounts'):
        for cloud_account in response['data']['cloudAccountListing']['cloudAccounts']:
          cloud_account_obj = CloudAccount(self.manager, cloud_account, self.log)
          self[cloud_account_obj.cloud_account_id] = cloud_account_obj

  def add(self): pass

class CloudAccount(core.CoreObject):
  def __init__(self, manager=None, api_response=None, log_func=None):
    self.manager = manager
    if api_response: self._set_properties(api_response, log_func)