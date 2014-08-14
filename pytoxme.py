import nacl.utils, json, urllib2, time
from nacl.public import PrivateKey, Box

import err #local files are special

def _psh2srv(rs):
	try:
		get = urllib2.urlopen(rs)
		stream = get.read()
		try:
			return stream
		except:
			raise err.srv('unknown error')
	except urllib2.HTTPError, err:
		stream = err.read()
		try:
			return stream
		except:
			raise err.srv('unknown error')
	except:
		import err
		raise err.srv('invalid domain')

def _pushauth(act,domain,payload,auth,r_nonce):
	nonce = nacl.encoding.Base64Encoder.encode(r_nonce).decode("utf8")
	pub = auth.public_key.encode(encoder=nacl.encoding.HexEncoder)
	post = '{{"action":{}, "public_key":"{}", "encrypted":"{}", "nonce":"{}"}}'.format(act,pub,payload,nonce)
	rs = urllib2.Request('https://' + domain + '/api',data=post)

	data = _psh2srv(rs)
	try:
		return json.loads(data)
	except:
		return data

def _toxme_err(data):
	if data['c'] == 0:
		return data
	else:
		raise err.toxme(data['c'])

def getpub(domain):
	rs = urllib2.Request('https://' + domain + '/pk')
	data = _psh2srv(rs)
	try:
		return json.loads(data)['key']
	except:
		raise err.psh2srv('unable to find public key')


def lookup(domain,name):
	post = '{{"action":3, "name":"{}" }}'.format(name)
	rs = urllib2.Request('https://' + domain + '/api',data=post)
	data = _psh2srv(rs)
	_toxme_err(json.loads(data))

def getauth(secret=''):
	if secret != '':
		try:
			return nacl.public.PrivateKey(secret,encoder=nacl.encoding.HexEncoder)
		except:
			raise err.api('invalid secret')
	else:
		return PrivateKey.generate()

def nonce():
	return nacl.utils.random(Box.NONCE_SIZE)

def getbox(auth,key):
	key_raw = nacl.public.PublicKey(key, encoder=nacl.encoding.HexEncoder)
	return Box(auth,key_raw)

def payload_push(box,auth,nonce,tox_id,name,privacy=1,bio=''):
	payload = '{{"tox_id": "{}", "name":"{}", "privacy":{},"bio":"{}","timestamp":{}}}'.format(tox_id,name,privacy,bio,int(time.time()))
	return box.encrypt(payload,nonce,encoder=nacl.encoding.Base64Encoder).ciphertext

def payload_delete(box,auth,nonce,tox_id):
	payload = '{{"public_key": "{}","timestamp":{}}}'.format(tox_id[0:64],int(time.time()))
	return box.encrypt(payload,nonce,encoder=nacl.encoding.Base64Encoder).ciphertext

def push(domain,payload,auth,r_nonce):
	return _toxme_err(_pushauth(1,domain,payload,auth,r_nonce))

def delete(domain,payload,auth,r_nonce):
	return _toxme_err(_pushauth(2,domain,payload,auth,r_nonce))