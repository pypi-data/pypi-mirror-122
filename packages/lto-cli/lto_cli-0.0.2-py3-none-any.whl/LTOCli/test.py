import json

import HandleDefault as handle
transaction = {"type": 4,"version": 2,"sender": "","senderPublicKey": "","fee": 100000000,"timestamp": 0,"amount": 10000000,"recipient": "3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du","attachment": "","proofs": []}

print(handle.prettyPrint(transaction))