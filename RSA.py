import hashlib
import os
import random
import math

# A set will be the collection of prime numbers, where we will select 2 random primes, p and q
import sys

prime = set()

RSA_public_key = None
RSA_private_key = None
n = None


def byte_len(i):
    n = len(hex(i)) - 2
    if i == 0:
        n = 1
    if i < 0:
        n -= 1
    return(n)


# We will run this function to fill the set of prime numbers
def primefiller():
    # Method used to fill the primes set is Sieve of Eratosthenes (a method to collect prime numbers)
    seive = [True] * 250
    seive[0] = False
    seive[1] = False
    for i in range(2, 250):
        for j in range(i * 2, 250, i):
            seive[j] = False

    # Filling the prime numbers
    for i in range(len(seive)):
        if seive[i]:
            prime.add(i)


# This function picks a random prime number and erases that prime number from list because p!=q
def pickrandomprime():
    global prime
    k = random.randint(0, len(prime) - 1)
    it = iter(prime)
    for _ in range(k):
        next(it)

    ret = next(it)
    prime.remove(ret)
    return ret


def setkeys():
    global RSA_public_key, RSA_private_key, n
    prime1 = pickrandomprime()  # First prime number
    prime2 = pickrandomprime()  # Second prime number

    n = prime1 * prime2
    fi = (prime1 - 1) * (prime2 - 1)

    e = 2
    while True:
        if math.gcd(e, fi) == 1:
            break
        e += 1

    # d = (k*Φ(n) + 1) / e for some integer k
    RSA_public_key = e

    d = 2
    while True:
        if (d * e) % fi == 1:
            break
        d += 1

    RSA_private_key = d


# Encrypt the given number
def RSA_encrypt(message):
    global RSA_public_key, n
    e = RSA_public_key
    encrypted_text = 1
    while e > 0:
        encrypted_text *= message
        encrypted_text %= n
        e -= 1
    return encrypted_text


# Decrypt the given number
def RSA_decrypt(encrypted_text):
    global RSA_private_key, n
    d = RSA_private_key
    decrypted = 1
    while d > 0:
        decrypted *= encrypted_text
        decrypted %= n
        d -= 1
    return decrypted


# To encode the message, we convert each character to its ASCII value and then  we encode it
def RSA_encoder(filename):
    cipherText = []
    # Calling the encrypting function in encoding function
    plainText = ''

    with open(filename, "r") as inputFile:
        plainText = inputFile.read()

    for letter in plainText:
        cipherText.append(RSA_encrypt(ord(letter)))

    with open("enc_" + filename, "w") as outputFile:
        for number in cipherText:
            outputFile.write(str(number) + "\n")

# To decode the message, we decode the number to get the ASCII and converting it to character
def RSA_decoder(filename):
    plainText = ''
    cipherText = []

    with open(filename, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            cipherText.append(int(line))

    for num in cipherText:
        plainText += chr(RSA_decrypt(num))

    with open("dec_" + filename, "w") as outputFile:
        outputFile.write(plainText)

def RSA(keyfile, filename, mode):
    global RSA_private_key, RSA_public_key, n


    if os.path.exists(keyfile):
        with open(keyfile, 'rb') as f:
            RSA_private_key = int(bytearray(f.readline()).decode("ascii"))
            RSA_public_key = int(bytearray(f.readline()).decode("ascii"))
            n = int(bytearray(f.readline()).decode("ascii"))
    else:
        primefiller()
        setkeys()

        private_key = str(RSA_private_key).encode("ascii")
        public_key = str(RSA_public_key).encode("ascii")
        write_n = str(n).encode("ascii")

        with open(keyfile, 'wb') as f:
            f.write(private_key + b'\n')
            f.write(public_key + b'\n')
            f.write(write_n)


    if mode == 'enc':
        RSA_encoder(filename)
    elif mode == 'dec':
        RSA_decoder(filename)
