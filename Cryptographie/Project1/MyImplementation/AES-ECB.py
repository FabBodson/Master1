###
# This is the code using the ECB mode of AES encrypting
###


from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64decode, b64encode
# To calculate time of execution
import time

# Sizes of the blocks and the key
BLOCK_SIZE = 16
KEY_SIZE = 32

# Generating a random unique key
KEY = get_random_bytes(KEY_SIZE)


def pad(message):
    """
    It applies a padding to a message
    :param message: string to pad
    :return: padded string
    """
    length = BLOCK_SIZE - len(message) % BLOCK_SIZE
    return message + (length * chr(length))


def unpad(message):
    """
    It applies an unpadding to a message by calculating the original string without the padding
    :param message: string to unpad
    :return: unpadded string
    """
    pad_length = len(message)
    last_character = message[pad_length - 1:]
    ascii_value = -ord(last_character)
    return message[:ascii_value]


def encrypt(plaintext):
    """
    Encryption using the AES ECB mode on a padded plaintext
    :param plaintext: string
    :return: base 64 encoded bytes
    """
    blocks = pad(plaintext)
    cipher = AES.new(KEY, mode=AES.MODE_ECB)
    # Converting plaintext in bytes
    data_bytes = blocks.encode('ascii')
    encrypted_string = cipher.encrypt(data_bytes)
    return b64encode(encrypted_string)


def decrypt(ciphertext):
    """
    Decryption using the AES ECB mode on bytes
    :param ciphertext: bytes
    :return: string
    """
    encrypted_msg = b64decode(ciphertext)
    cipher = AES.new(KEY, mode=AES.MODE_ECB)
    decrypted_msg = cipher.decrypt(encrypted_msg)

    plaintext = unpad(decrypted_msg)

    return str(plaintext.decode('ascii'))


def main():
    # Start time
    start_time = time.time()

    with open('./plaintext.txt') as file:
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

    with open('./Personal-Ciphertext-ECB.txt', 'w') as cipherfile:
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
