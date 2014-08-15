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
	post = {"action":act, "public_key":pub, "encrypted":payload, "nonce":nonce}
	rs = urllib2.Request('https://{}/api'.format(domain),data=json.dumps(post))

	return json.loads(_psh2srv(rs))

def _toxme_err(data):
	code = int(data['c'])
	if code == 0:
		return data
	else:
		raise err.toxme(data['c'])

def getpub(domain='toxme.se'):
	rs = urllib2.Request('https://{}/pk'.format(domain))
	data = _psh2srv(rs)
	try:
		return json.loads(data)['key']
	except:
		raise err.srv('unable to find public key')


def lookup(name,domain='toxme.se'):
	post = {"action":3, "name":name}
	rs = urllib2.Request('https://{}/api'.format(domain),data=json.dumps(post))
	data = _psh2srv(rs)
	return _toxme_err(json.loads(data))

def getauth(secret=''):
	if secret != '':
		try:
			return nacl.public.PrivateKey(secret,encoder=nacl.encoding.HexEncoder)
		except:
			raise err.api('invalid secret')
	else:
		return PrivateKey.generate()

def getnonce():
	return nacl.utils.random(Box.NONCE_SIZE)

def getbox(auth,key):
	try:
		key_raw = nacl.public.PublicKey(key, encoder=nacl.encoding.HexEncoder)
		try:
			return Box(auth,key_raw)
		except:
			raise err.api('invalid auth object')
	except:
		raise err.api('invalid server key')

def payload_push(box,auth,nonce,tox_id,name,privacy=1,bio=''):
	payload = {"tox_id": tox_id, "name":name, "privacy":privacy,"bio":bio,"timestamp":int(time.time())}
	try:
		return box.encrypt(json.dumps(payload),nonce,encoder=nacl.encoding.Base64Encoder).ciphertext
	except:
		raise err.api('Error encrypting payload.')

def payload_delete(box,auth,nonce,tox_id):
	payload = {"public_key": tox_id[0:64],"timestamp":int(time.time())}
	try:
		return box.encrypt(json.dumps(payload),nonce,encoder=nacl.encoding.Base64Encoder).ciphertext
	except:
		raise err.api('Error encrypting payload.')


def push(domain,payload,auth,nonce):
	return _toxme_err(_pushauth(1,domain,payload,auth,nonce))

def delete(domain,payload,auth,r_nonce):
	return _toxme_err(_pushauth(2,domain,payload,auth,nonce))

def simple_push(domain,name,toxid,secret='',privacy=1,bio=''):
	nonce = getnonce()
	pk = getpub(domain) 
	auth = getauth(secret)
	crypto = getbox(auth,pk)
	payload = payload_push(crypto,auth,nonce,toxid,name,privacy,bio)
	return push(domain,payload,auth,nonce)

def simple_delete(domain,toxid,secret):
	nonce = getnonce()
	pk = getpub(domain) 
	auth = getauth(secret)
	crypto = getbox(auth,pk)
	payload = payload_delete(crypto,auth,nonce,toxid)
	return delete(domain,payload,auth,nonce)