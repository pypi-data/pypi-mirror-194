from flask import jsonify, make_response
from platform import node
from binascii import hexlify
from os import urandom
import binascii

from base64 import b64encode
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


from jumonc.helpers.generateToken import generateToken
from jumonc.authentication import tokens

lastMessage = None
key = None
token = ""


def generateMessage() -> str:
    global lastMessage
    
    lastMessage = hexlify(urandom(32)).decode('ascii')
    
    return lastMessage


def getMessage():
    nodename = node()
    message = generateMessage()
    data = {"Node": nodename, "Message": message}
    return make_response(jsonify(data), 200)

def testMessage(verifiedMessage):
    global lastMessage
    
    if lastMessage is None:
        data {"Error": "No message found. Can only verify after a \"v1/llview/retrieveToken?getMessage=1\" call"}
        return make_response(jsonify(data), 401)
    message = lastMessage + node()
    
    lastMessage = None
    
    digest = SHA256.new(message.encode("ascii"))
    bin_message = binascii.unhexlify(verifiedMessage.encode('utf-8'))
    try:
        pkcs1_15.new(key).verify(digest, bin_message)
        data = {"Token": token}
        return make_response(jsonify(data), 200)
    except:
        data = {"Error": "Could not verify message"}
        return make_response(jsonify(data), 401)


def readKey(path, level):
    global key
    global token
    
    with open(path, 'r') as f:
        key = key = RSA.import_key(f.read())
        token = generateToken()
        tokens.addToken(token, level)