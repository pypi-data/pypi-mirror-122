from LTO.Accounts.AccountFactoryECDSA import AccountECDSA
from LTO.Accounts.AccountFactoryED25519 import AccountED25519
from LTO.PublicNode import PublicNode
from LTO.Transactions.Transfer import Transfer

seed = 'cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy'
seed3 = 'fkljdf ewkfjhwe ewfkjwek ewkjhwer'

account2 = AccountED25519('T').createFromSeed(seed)
account = AccountECDSA('T').createFromSeed(seed)
account3 = AccountECDSA('T').createFromSeed(seed3)
node = PublicNode('https://testnet.lto.network')
address = '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'
addressNew = '3N9jYinodoqXqHhcj6vXgYjbTub4XegvDGn'
transaction = Transfer(recipient=address, amount=20000000)
#print(account.publicKey.to_string())
#print(account.privateKey.to_string())
transaction.signWith(account)
#transaction.broadcastTo(node)

PublicNode('https://testnet.lto.network').broadcast(transaction)
import json
#print(json.dumps(transaction.toJson()))

#node = PublicNode('https://testnet.lto.network')
#print(node.wrapper(api='/addresses/balance/{}'.format(addressNew)))

print(account.address)
print(account2.address)
print(type(account.address))
print(type(account2.address))
import base58
import crypto


print(account.publicKey.to_string(), 'this')
print(account2.publicKey.__bytes__(), 'that')

print(len(account.publicKey.to_string()), 'this')
print(len(account2.publicKey.__bytes__()), 'that')

print(type(account.publicKey.to_string()), 'this')
print(type(account2.publicKey.__bytes__()), 'that')

print(account.publicKey)

pub = b'\x020\x01\xfd\xed\xc5W\xfb\xc8\x04D\x8at:\xe6\xf1\\\x7f\xe59f\x1b\xb5G\x1b\n\xb1\xe4\xfcr\xbc\x1dd'
print(base58.b58encode(pub))