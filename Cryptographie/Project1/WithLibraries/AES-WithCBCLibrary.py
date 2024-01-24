from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64decode, b64encode
# To calculate time of execution
import time

# Sizes of the blocks and the key
BLOCK_SIZE = 16
KEY_SIZE = 32

# Generating a random unique key and IV
KEY = get_random_bytes(KEY_SIZE)
IV = get_random_bytes(BLOCK_SIZE)


def encrypt(plaintext):
    """
    This function encrypts data using the CBC library of PyCryptpdome package.
    :param plaintext: A string to encrypt
    :return: Base 64 encoded byte string.
    """
    # Converting plaintext in bytes
    data_bytes = plaintext.encode('ascii')

    # Applying the padding
    padding = pad(data_bytes, AES.block_size)

    # AES object creation with the key and the IV
    cipher = AES.new(KEY, AES.MODE_CBC, IV)

    # cipher.encrypt() returns bytes
    ciphertext = cipher.encrypt(padding)

    return b64encode(ciphertext)


def decrypt(ciphertext):
    """
    This function decrypts data using the CBC library of PyCryptpdome package.
    :param ciphertext: An encrypted text
    :return: decrypted string
    """
    # AES object creation
    cipher = AES.new(KEY, AES.MODE_CBC, IV)

    # Decryption's result is in bytes
    decryption = cipher.decrypt(b64decode(ciphertext))

    # Removing the padding to get the original bytes
    decryption = unpad(decryption, AES.block_size)

    # Returning the decoded decryption
    return decryption.decode('ascii')


def main():
    # Start time
    start_time = time.time()

    with open("./plaintext.txt") as file:
        # Read file, creates list with each line
        plaintext_content = file.readlines()

        # Empty list that will contain the encrypted lines
        encrypted_list = []

        # Iterating on each line to encrypt it when it is not a \n
        for line in plaintext_content:
            if line is "\n":
                print("\n")
                encrypted_list.append(line)
            else:
                # Encrypting the plaintext line
                encrypted_msg = encrypt(line)
                print(f'Plaintext is encrypted : {encrypted_msg}\n')

                # Appending encrypted msg to list to write it to file later
                encrypted_list.append(encrypted_msg)

                # Decrypting the newly encrypted message
                decrypted_msg = decrypt(encrypted_msg)
                print(f'Ciphertext is decrypted : {decrypted_msg}')

                # Printing so that we can compare the decryption vs the original plaintext
                print(f'Plaintext was : {line}')

    with open('Ciphertext_CBC.txt', 'w') as cipherfile:
        # Iterating on each line to encrypt it when it is not a \n
        for element in encrypted_list:
            if element is "\n":
                cipherfile.write(element)
            else:
                # Writing encrypted element to file
                cipherfile.write(str(element))

    # End time
    end_time = time.time()
    # Delta time
    execution_time = end_time - start_time
    print('Execution time:', execution_time, 'second')


if __name__ == '__main__':
    main()
