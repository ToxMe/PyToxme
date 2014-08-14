The PyToxme API is simple.

##anonmous lookups:
#####getpub(domain):
This returns the public key for a domain

``pk = getpub('toxme.se')``

#####lookup(domain,user):
This looks up an entry, both user and user@domain are suported. Note that it returns a json object.

``mykey = lookup('toxme.se','sean')['public_key']``

The json object looks like

``{u'public_key': u'1076A72D9BEDFF6CCC8D2E9A69E0EF6FED9968AC6DCAC84A908E9F65B4E2E321AB8E3BB05FE1', u'c': 0, u'regdomain': u'toxme.se', u'name': u'sean', u'url': u'tox://sean@toxme.se', u'verify': {u'status': 1, u'detail': u'Good (signed by local authority)'}, u'source': 1, u'version': u'Tox V1 (local)'}``

##authenticated API:
####Warning: editing or deleting your record? use your Tox ID's secret for getauth()
#####getauth(optional= secret):
This creates an authentication object, you'll need to save this for all requests a session. It accepts the optional argument of a hex private key.

``auth = getauth()``

#####getbox(auth,toxme_pk):
This creates an encryption object, it can be saved for the session. It accepts the auth object from ``getauth()`` and the public key from ``getpub()``. Also save this, we'll need to it encrypt our payload.

``crypto = getbox(pk,auth)``

#####nonce():
Nonce generates a nonce, you'll need this for the next two steps. Keep in mind that this can only be used for the next two steps once, and must be regenerated.

``nonce = nonce()``

#####payload_push(crypto,auth,nonce,tox_id,name,optional=privacy,optional=bio):
This generates and encrypts a payload for us to send to a server, this is a payload for adding/editing records. This accepts the ``getbox`` object, the ``getauth`` object, the ``nonce`` generated earlier, a Tox ID, a name, an optional number for being listed or not (0 listed, 1 not), and an optional bio. Save this so we can push it later.

``payload = payload_push(crypto,auth,nonce,"8719E62D498152B3CD53CAB6FB8853E2C3023FBBA2F9FF6906B331FFDAE1EB5219B6C764AC8D", "test_sean")``

#####payload_delete(crypto,auth,nonce,tox_id):
This generates and encrypts a payload for us to send to a server, this is a payload for deleting records. This accepts the ``getbox`` object, the ``getauth`` object, the ``nonce`` generated earlier, and a Tox ID.

``payload = payload_push(crypto,auth,nonce,"8719E62D498152B3CD53CAB6FB8853E2C3023FBBA2F9FF6906B331FFDAE1EB5219B6C764AC8D")``

#####push(domain,payload,auth,nonce):
This pushes a payload with the intent to push data. It accepts the domain from earlier, the payload from ``payload_push``, the auth from ``getauth``, and the ``nonce`` from earlier.

``print push(domain,payload,auth,nonce)``

#####delete(domain,payload,auth,nonce):
This pushes a payload with the intent to delete data. It accepts the domain from earlier, the payload from ``payload_delete``, the auth from ``getauth``, and the ``nonce`` from earlier.

``print delete(domain,payload,auth,nonce)``

##FAQ:
The PyTox API returns the return objects from https://github.com/Tox/toxme.se/blob/master/api.md#return-values in dictionary format for ease of access.

If pushing gives ``An error occured`` you've done something seriously wrong because the data returned isn't correct at all.

If pushing gives you ``Invalid domain`` check your domain
