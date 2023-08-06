import logging
from flask import jsonify, make_response
from platform import node
from binascii import hexlify
from os import urandom
import binascii

from Crypto.PublicKey import ECC
from Crypto.Signature import eddsa


from jumonc.helpers.generateToken import generateToken
from jumonc.authentication import tokens

logger = logging.getLogger(__name__)

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
        data = {"Error": "No message found. Can only verify after a \"v1/llview/retrieveToken?getMessage=1\" call"}
        return make_response(jsonify(data), 401)
    message = lastMessage + node()
    
    lastMessage = None
    
    verifier = eddsa.new(key, 'rfc8032')
    sig = binascii.unhexlify(verifiedMessage.encode('utf-8'))
    try:
        logger.debug(str(sig))
        verifier.verify(message.encode("utf-8"), sig)
        data = {"Token": token}
        return make_response(jsonify(data), 200)
    except:
        logger.debug("key retrival error:", exc_info=True)
        data = {"Error": "Could not verify message"}
        return make_response(jsonify(data), 401)


def readKey(path, level):
    global key
    global token
    
    with open(path, 'r') as f:
        key = ECC.import_key(f.read())
        token = generateToken()
        logger.info("Creating access token for llview")
        tokens.addToken(token, level)