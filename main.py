import argparse
import hashlib
import os
from DES import DES, TripleDES
from RSA import RSA

# Parse command line arguments
parser = argparse.ArgumentParser(description='Encrypt or decrypt a file using DES, 3DES, or RSA')
parser.add_argument('-a', dest='algorithm', choices=['DES', '3DES', 'RSA'], required=True,
                    help='Encryption algorithm. Can be "DES", "3DES", or "RSA"')
parser.add_argument('-k', dest='keyfile', type=str, required=True,
                    help='Path to key file. If it doesn\'t exist, the program will generate a new key in said file.')
parser.add_argument('-m', dest='mode', choices=['enc', 'dec'], required=True,
                    help='Running mode. Can be "enc" or "dec".')
parser.add_argument('-f', dest='filename', type=str, required=True, help='Path to file to encrypt or decrypt')
args = parser.parse_args()


def GetKey(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            key = f.read()
    else:
        password = input("Enter a password to generate a key: ")
        key = hashlib.sha256(password.encode()).hexdigest()
        key = key.encode()
        with open(filename, 'wb') as f:
            f.write(key)

    return key.decode("ascii")


def binary_to_ascii(binary_key):
    ascii_key = ''.join([chr(b) for b in binary_key])
    return ascii_key


if __name__ == "__main__":
    key = ''
    if args.algorithm != 'RSA':
        # Get/Generate key
        key = GetKey(args.keyfile)

    # Determine running mode
    runningMode = 'null'
    if args.mode == "enc" or args.mode == 'dec':
        runningMode = args.mode

    # Check if file exists
    path = "./" + args.filename
    if not os.path.isfile(path):
        print("ERROR: Filename for enc/dec is invalid!")
        pass

    # Run algorithm based on arguments
    if args.algorithm == "DES":
        DES(key, args.filename, runningMode)
    elif args.algorithm == "3DES":
        TripleDES(key, args.filename, runningMode)
    elif args.algorithm == "RSA":
        RSA(args.keyfile, args.filename, runningMode)
