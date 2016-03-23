# standard library
import json
import logging
import ssl
import urllib
import urllib2

# 3rd party libraries
import libs.xmltodict as xmltodict

# project libraries

class CoreApi(object):
  def __init__(self):
    self.API_TYPE_REST = 'REST'
    self.API_TYPE_SOAP = 'SOAP'
    self.rest_api_endpoint = ''
    self.soap_api_endpoint = ''
    self.ignore_ssl_validation = False
    self._log_at_level = logging.WARNING
    self.logger = self._set_logging()

  # *******************************************************************
  # properties
  # *******************************************************************
  @property
  def log_at_level(self): return self._log_at_level
  
  @log_at_level.setter
  def log_at_level(self, value):
    """
    Make sure logging is always set at a valid level
    """
    if value in [
      logging.CRITICAL,
      logging.DEBUG,
      logging.ERROR,
      logging.FATAL,
      logging.INFO,
      logging.WARNING,
      ]:
      self._log_at_level = value
      self._set_logging()
    else:
      if not self._log_at_level:
        self._log_at_level = logging.WARNING
        self._set_logging()

  # *******************************************************************
  # methods
  # *******************************************************************
  def _set_logging(self):
    """
    Setup the overall logging environment
    """
    # Based on tips from http://www.blog.pythonlibrary.org/2012/08/02/python-101-an-intro-to-logging/
    logging.basicConfig(level=self.log_at_level)

    # setup module logging
    logger = logging.getLogger("DeepSecurity.API")
    logger.setLevel(self.log_at_level)

    # reset any existing handlers
    logging.root.handlers = [] # @TODO evaluate impact to other modules
    logger.handlers = []

    # add the desired handler
    formatter = logging.Formatter('[%(asctime)s]\t%(message)s', '%Y-%m-%d %H:%M:%S')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

  def _request(self, request):
    """
    Make an HTTP(S) request to an API endpoint based on what's specified in the 
    request object passed

    ## Input

    Required request keys:
      api
        Either REST or SOAP

      call
        Name of the SOAP method or relative path of the REST URL 

    Optional keys:
      query
        Contents of the query string passed as a dict

      data
        Data to post. For SOAP API calls this will be the SOAP envelope. For
        REST API calls this will be a dict converted to JSON automatically 
        by this method

    ## Output

    Returns a dict:
      status
        Number HTTP status code returned by the response, if any

      raw
        The raw contents of the response, if any

      data
        A python dict representing the data contained in the response, if any
    """
    for required_key in [
      'api',
      'call'
      ]:
      if not request.has_key(required_key) and request[required_key]:
        self.log("All requests are required to have a key [{}] with a value".format(required_key), level="critical")
        return None

    url = None
    if request['api'] == self.API_TYPE_REST:
      url = "{}/{}".format(self.rest_api_endpoint, request['call'].lstrip('/'))
    else:
      url = self.soap_api_endpoint

    # prep the query string
    if request.has_key('query') and request['query']:
      # get with query string
      qs = {}
      for k, v in request['query'].items(): # strip out null entries
        if v: qs[k] = v

      url += '?%s' % urllib.urlencode(qs)

    self.log("URL to request is: {}".format(url))

    # Prep the SSL context
    ssl_context = ssl.create_default_context()
    if self.ignore_ssl_validation:
      ssl_context.check_hostname = False
      ssl_context.verify_mode = ssl.CERT_NONE
      self.log("SSL certificate validation has been disabled for this call", level='warning')

    # Prep the URL opener
    url_opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ssl_context))
  
    # Prep the request
    request_type = 'GET'
    headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      }

    # authentication calls don't accept the Accept header
    if request['call'].startswith('authentication'): del(headers['Accept'])

    if request['api'] == self.API_TYPE_SOAP:
      # always a POST
      headers = {
        'SOAPAction': '',
        'content-type': 'application/soap+xml'
        }
      url_request = urllib2.Request(url, data=request['data'], headers=headers)
      request_type = 'POST'
    elif request['call'] == 'authentication/logout':
      url_request = urllib2.Request(url, headers=headers)
      setattr(url_request, 'get_method', lambda: 'DELETE') # make this request use the DELETE HTTP verb
      request_type = 'DELETE'
    elif request.has_key('data') and request['data']:
      # POST
      url_request = urllib2.Request(url, data=json.dumps(request['data']), headers=headers)
      request_type = 'POST'
    else:
      # GET
      url_request = urllib2.Request(url, headers=headers)

    # Make the request
    response = None
    try:
      response = url_opener.open(url_request)
    except Exception, url_err:
      self.log("Failed to make {} {} call [{}]".format(request['api'].upper(), request_type, call['method'].lstrip('/')), err=url_err)

    # Convert the request from JSON
    result = {
      'status': response.getcode() if response else None,
      'raw': response.read() if response else None,
      'data': None
    }

    if response:
      if request['api'] == self.API_TYPE_SOAP:
        # XML response
        try:
          if result['raw']:
            result['data'] = xmltodict.parse(result['raw'])
        except Exception, xmltodict_err:
          self.log("Could not convert response from call {}".format(request['call']), err=xmltodict_err)
      else:
        # JSON response
        try:
          if result['raw']:
            result['data'] = json.loads(result['raw'])
        except Exception, json_err:
          self.log("Could not convert response from call {} to JSON".format(request['call']), err=json_err)

    return result

  def _prefix_keys(self, prefix, d):
    """
    Add a namespace prefix to all keys in a dict data type
    """
    if not type(d) == type({}): return d
    new_d = d.copy()
    for k,v in d.items():
      new_key = "{}:{}".format(prefix, k)
      new_v = v
      if type(v) == type({}): new_v = self._prefix_keys(prefix, v)
      new_d[new_key] = new_v 
      del(new_d[k])

    return new_d    

  def _prep_data_for_soap(self, call, details):
    """
    Prepare the complete XML SOAP envelope
    """
    data = xmltodict.unparse(self._prefix_keys('ns1', { call: details }), pretty=False, full_document=False)
    soap_xml = """
    <?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="urn:Manager" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
      <SOAP-ENV:Header/>
        <ns0:Body>
          {}
        </ns0:Body>
    </SOAP-ENV:Envelope>
    """.format(data).strip()

    return soap_xml

  def log(self, message='', err=None, level='info'):
    if not level.lower() in [
      'critical',
      'debug',
      'error',
      'fatal',
      'info',
      'warning'
      ]: level = 'info'

    if err:
      level = 'error'
      message += ' Threw exception:\n\t{}'.format(err)

    try:
      func = getattr(self.logger, level.lower())
      func(message)
    except Exception, log_err:
      self.logger.critical("Could not write to log. Threw exception:\n\t{}".format(log_err))