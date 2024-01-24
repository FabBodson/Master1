###
# This is the code using the CTR mode of AES encrypting
###


from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64decode, b64encode
# To calculate time of execution
import time

# Sizes of the blocks and the key
BLOCK_SIZE = 16
KEY_SIZE = 32

# Generating a random unique key and IV
KEY = get_random_bytes(KEY_SIZE)
IV = get_random_bytes(BLOCK_SIZE)


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


def xor(actual_block, previous_block):
    """
    Applies a XOR between the actual block and the previoussly ciphered block to return a new block of bytes
    :param actual_block: Block that is actually computed
    :param previous_block: the block tha was previously encrypted
    :return: bytes
    """
    return bytes(block1 ^ block2 for block1, block2 in zip(actual_block, previous_block))


def encrypt(plaintext):
    """
    Encryption using the AES ECB mode on a padded plaintext
    :param plaintext: string
    :return: base 64 encoded bytes
    """
    ciphertext = b""
    cipher = AES.new(KEY, mode=AES.MODE_ECB)
    blocks = pad(plaintext)
    number_blocks = int(len(plaintext) / BLOCK_SIZE)
    # Initialising counter to IV so I can increment it later
    counter = IV

    for block_number in range(number_blocks):
        end_of_actual_block = (block_number + 1) * BLOCK_SIZE
        start_of_actual_block = end_of_actual_block - BLOCK_SIZE

        block_as_bytes = blocks.encode('ascii')

        # If 1st block, I use the IV
        if block_number == 0:
            xor_block = xor(block_as_bytes[start_of_actual_block:end_of_actual_block], IV)
        # else I use the counter that is incremented each iteration
        else:
            counter = int.from_bytes(counter, "big") + 1
            counter = counter.to_bytes(BLOCK_SIZE, "big")
            xor_block = xor(block_as_bytes[start_of_actual_block:end_of_actual_block], counter)

        encrypted_block = cipher.encrypt(xor_block)
        ciphertext += encrypted_block

    return b64encode(ciphertext)


def decrypt(ciphertext):
    """
    Decryption using the AES ECB mode on bytes
    :param ciphertext: bytes
    :return: string
    """
    plaintext = b""
    cipher = AES.new(KEY, mode=AES.MODE_ECB)
    ciphertext = b64decode(ciphertext)
    number_blocks = int(len(ciphertext) / BLOCK_SIZE)
    counter = IV

    for block_number in range(number_blocks):
        end_of_actual_block = (block_number + 1) * BLOCK_SIZE
        start_of_actual_block = end_of_actual_block - BLOCK_SIZE

        if block_number == 0:
            block_as_bytes = cipher.decrypt(ciphertext[start_of_actual_block:end_of_actual_block])
            xor_block = xor(block_as_bytes[start_of_actual_block:end_of_actual_block], IV)

        else:
            counter = int.from_bytes(counter, "big") + 1
            counter = counter.to_bytes(BLOCK_SIZE, "big")
            block_as_bytes = cipher.decrypt(ciphertext[start_of_actual_block:end_of_actual_block])
            xor_block = xor(block_as_bytes, counter)

        plaintext += xor_block

    plaintext = unpad(plaintext)

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

    with open('./Personal-Ciphertext-CTR.txt', 'w') as cipherfile:
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
