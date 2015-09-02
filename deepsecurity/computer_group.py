class ComputerGroup:
	"""
	Represents a Deep Security computer group
	"""
	def __init__(self, group_details, log):
		self.log = log
		self.id = None
		self.description = None
		self.name = None
		self.is_external = False
		self.external_id = None
		self.parent_id = None

		self._parse_details(group_details)

	def __str__(self):
		if self.id and self.name:
			return "ComputerGroup {} <{}>".format(self.id, self.name)
		elif self.id:
			return "ComputerGroup {}".format(self.id)
		else:
			return self.__name__

	def _parse_details(self, group_details):
		for k, v in {
			'ID': 'id',
			'description': 'description',
			'name': 'name',
			'external': 'is_external',
			'externalID': 'external_id',
			'parentGroupID': 'parent_id',
			}.items():
			try:
				setattr(self, v, getattr(group_details, k))
			except Exception, err:
				self.log("Could not set attribute [{}] for ComputerGroup".format(v), exception=err)