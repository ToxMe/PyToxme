class srv(Exception):
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
		return repr(toxme_err(self.value))

def toxme_err(code):
	if code == 0:
		return 'error, valid query flagged as error'
	elif code == -1:
		return 'Client did not POST to /api'
	elif code == -2:
		return 'Client is not using a secure connection'
	elif code == -3:
		return 'Bad encrypted payload (not encrypted with our key)'
	elif code == -4:
		return 'Client is publishing IDs too fast'
	elif code == -25:
		return 'Name is taken.'
	elif code == -26:
		return 'The public key given is bound to a name already.'
	elif code == -30:
		return 'Name not found.'
	elif code == -31:
		return 'Invalid Tox ID passed.'
	elif code == -41:
		return 'Lookup failed because of an error on the other domains side.'
	elif code == -42:
		return 'Lookup failed because that user does not exist on the domain'
	elif code == -43:
		return 'Lookup failed because of an error on our side.'
	else:
		return 'An unknown toxme error occured, additionally it did not return a valid code ({})'.format(code)
