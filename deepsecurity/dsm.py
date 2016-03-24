# standard library

# 3rd party libraries

# project libraries
import core

class Manager(core.CoreApi):
  def __init__(self,
      hostname='app.deepsecurity.trendmicro.com',
      port='4119',
      tenant=None,
      username=None,
      password=None,
      ignore_ssl_validation=False
      ):
    core.CoreApi.__init__(self)
    self._hostname = None
    self._port = port
    self._tenant = tenant
    self._username = username
    self._password = password
    self.ignore_ssl_validation = ignore_ssl_validation
    self.hostname = hostname

  # *******************************************************************
  # properties
  # *******************************************************************
  @property
  def hostname(self): return self._hostname
  
  @hostname.setter
  def hostname(self, value):
    if value = 'app.deepsecurity.trendmicro.com': # Deep Security as a Service
      self.port = 443
    self._hostname = value
  
  @property
  def port(self): return self._port

  @port.setter
  def port(self, value): self._port = int(value)

  @property
  def tenant(self): return self._tenant

  @tenant.setter
  def tenant(self, value):
    self._tenant = value
    self._reset_session()

  @property
  def username(self): return self._username
  
  @username.setter
  def username(self, value):
    self._username = value
    self._reset_session()

  @property
  def password(self): return self._password

  @password.setter
  def password(self, value):
    self._password = value
    self._reset_session()

  # *******************************************************************
  # methods
  # *******************************************************************  
  def _reset_session(self):
    pass
  
  
  