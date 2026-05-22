import hashlib # Used for all of the fun scrypt functions for hashing passwords, verifying passwords, etc.
import os # Used for the cryptographically secure RNG, os.urandom

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
# hashPW returns a byte formatted string of salt + the 
def hashPW(password: str) -> bytes:
    s = os.urandom(16) # 16 bytes of salt\
    key = hashlib.scrypt(password.encode('utf-8'), salt=s, n=N_COST, r=BLOCK_SIZE, p=P, dklen=klen)
    return s + key

# Derives the key portion from the attempted password and then compares it to the key stored inside of the database
# Returns true if the password was the same and false if they are not the same, pretty straight forward
def verifyPW(storedHash: bytes, attemptedPW: str) -> bool:
    s = storedHash[:16]#First 16 bytes is the salt
    key = storedHash[16:]#Last 16 bytes is the key

    try:
        derivedKey = hashlib.scrypt(attemptedPW.encode('utf-8'), salt=s, n=N_COST, r=BLOCK_SIZE, p=P, dklen=klen)
        return derivedKey == key
    except ValueError:
        print("Error in values of the derived key, block size, key length, or the salt can all cause this.")
        return False    