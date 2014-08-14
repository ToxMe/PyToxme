class psh2srv(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class api(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class toxme(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
