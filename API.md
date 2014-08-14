The PyToxme API is simple.

==anonymous lookups:==
=====getpub(domain):=====
This returns the public key for a domain
``pk = getpub('toxme.se')``

=====lookup(domain,user):=====
This looks up an entry, both user and user@domain are suported. Note that it returns a json object.
``mykey = lookup('toxme.se','sean')['public_key']``
The json object looks like ``{u'public_key': u'1076A72D9BEDFF6CCC8D2E9A69E0EF6FED9968AC6DCAC84A908E9F65B4E2E321AB8E3BB05FE1', u'c': 0, u'regdomain': u'toxme.se', u'name': u'sean', u'url': u'tox://sean@toxme.se', u'verify': {u'status': 1, u'detail': u'Good (signed by local authority)'}, u'source': 1, u'version': u'Tox V1 (local)'}``

==authenticated API:==
