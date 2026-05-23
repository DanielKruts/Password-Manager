import os # Used for the cryptographically secure RNG, os.urandom
import hashlib # Used for the creation of the cryptographically secure keys, then input into the HKDF for key derivation
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from typing import Optional, Tuple

#-----------------------------------------------------------------------#
# Parameters                                                            #
# N(n): Computational cost(CPU)/Memory cost factor. Must be power of 2  #
# r: Block size (Typically 8)                                           #
# p: Parallelization factor(Typically 1)                                #
# klen: Desired Key Length (e.g. 32 for a 256-bit key)                  #
#-----------------------------------------------------------------------#
N_COST = 2 ** 14 # 2 ^ 14
BLOCK_SIZE = 8
P = 1
klen = 32

# Takes a desired password and converts it into a byte formatting for hashlib.scrypt to properly handle
# keyDerviation returns two keys, one for encryption of the passwords in the file, and the other for verification of the user
def keyDerivation(password: str) -> Tuple[bytes, bytes]:
    s = os.urandom(16) # 16 bytes of salt
    key = hashlib.scrypt(password.encode('utf-8'), salt=s, n=N_COST, r=BLOCK_SIZE, p=P, dklen=klen)
    
    verify = HKDF(algorithm=hashes.SHA256(), length=klen, salt=s, info=bytes("Verification", 'utf-8'))
    encrypt = HKDF(algorithm=hashes.SHA256(), length=klen, salt=s, info=bytes("Encryption", 'utf-8'))

    verificationKey = verify.derive(key)
    encryptionKey = encrypt.derive(key)

    return (s+verificationKey, s+encryptionKey)

# Derives the key portion from the attempted password and then compares it to the key stored inside of the database
# Returns the derivedKey if it's correct, else returns None, which indicates that password input was incorrect
def verifyPW(storedHash: bytes, attemptedPW: str) -> Optional[bytes]:
    s = storedHash[:16]#First 16 bytes is the salt
    key = storedHash[16:]#Last 32 bytes is the verification key
    try:
        derivedKey = hashlib.scrypt(attemptedPW.encode('utf-8'), salt=s, n=N_COST, r=BLOCK_SIZE, p=P, dklen=klen)

        verification = HKDF(algorithm=hashes.SHA256(), length=klen, salt=s, info=bytes("Verification", 'utf-8'))

        #For some reason, the verification function returns false when the keys are the same, or at least something that looks like false
        # to the computer. So I've used not to get around this after confirming it will 100% raise an exception when the function finds
        # the key being derived is different from the key, or .derive(derivedKey) is not the same as key(Original verification key stored)
        if not (verification.verify(derivedKey, key)):
            encrypt = HKDF(algorithm=hashes.SHA256(), length=klen, salt=s, info=bytes("Encryption", 'utf-8'))
            derivedEncryption = encrypt.derive(derivedKey)
            return s+derivedEncryption
        return
    
    except ValueError:
        print("Error in the sizes of the parameters or the parameters themselves")
        return