class CloudAccount:
	"""
	Represents a Deep Security cloud connection
	"""
	def __init__(self, cloud_account_details, log):
		self.log = log
		self.id = None
		self.description = None
		self.real_time_sync = None
		self.cloud_region = False
		self.last_sync = None
		self.cloudType = None
		self.name = None

		self._parse_details(cloud_account_details)

	def __str__(self):
		if self.id and self.name:
			return "CloudAccount {} <{}>".format(self.id, self.name)
		elif self.id:
			return "CloudAccount {}".format(self.id)
		else:
			return self.__name__

	def _parse_details(self, cloud_account_details):
		for k, v in {
			'cloudAccountId': 'id',
			'description': 'description',
			'name': 'name',
			'realTimeSynchronization': 'real_time_sync',
			'lastTimeSynchronized': 'last_sync',
			'cloudType': 'cloudType',
			'cloudRegion': 'cloud_region',
			}.items():
			try:
				setattr(self, v, getattr(cloud_account_details, k))
			except Exception, err:
				self.log("Could not set attribute [{}] for CloudAccount".format(v), exception=err)