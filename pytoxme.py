import nacl.utils, json, urllib2, time, err
from nacl.public import PrivateKey, Box

def _psh2srv(rs):
	try:
		get = urllib2.urlopen(rs)
		stream = get.read()
		try:
			return stream
		except:
			raise err.psh2sev('unknown error')
	except urllib2.HTTPError, err:
		stream = err.read()
		try:
			return stream
		except:
			raise err.psh2sev('unknown error')
	except:
		raise err.psh2sev('invalid domain')

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

def getpub(domain):
	rs = urllib2.Request('https://' + domain + '/pk')
	data = _psh2srv(rs)
	try:
		return json.loads(data)['key']
	except:
		return data

def lookup(domain,name):
	post = '{{"action":3, "name":"{}" }}'.format(name)
	rs = urllib2.Request('https://' + domain + '/api',data=post)
	data = _psh2srv(rs)
	try:
		return json.loads(data)
	except:
		return data

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
	return _pushauth(1,domain,payload,auth,r_nonce)

def delete(domain,payload,auth,r_nonce):
	return _pushauth(2,domain,payload,auth,r_nonce)

domain = 'toxme.se'
toxme_pk = getpub(domain) 
auth = getauth()
crypto = getbox(auth,toxme_pk)
nonce = nonce();
payload = payload_push(crypto,auth,nonce,"8719E62D498152B3CD53CAB6FB8853E2C3023FBBA2F9FF6906B331FFDAE1EB5219B6C764AC8D", "test_sean")
record = push(domain,payload,auth,nonce)
print record
print lookup(domain,'sean')['public_key']
