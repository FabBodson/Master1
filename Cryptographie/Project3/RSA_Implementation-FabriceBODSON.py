import random
import math
# To calculate time of execution
import time


def get_gcd(nb1, nb2):
    """
    Using the Euclidian algorithm, it computes the GCD of 2 numbers
    :param nb1: first number
    :param nb2: second number
    :return: the GCD, x that will be used in the modinv() and y
    """
    s = 0
    x = 1
    t = 1
    y = 0
    r = nb2
    gcd = nb1

    while r != 0:
        quotient = gcd // r
        gcd, r = r, gcd - quotient * r
        x, s = s, x - quotient * s
        y, t = t, y - quotient * t

    return gcd, x, y


def modinv(nb1, nb2):
    """
    Reurns the modular invert
    :param nb1: public key
    :param nb2: phi(n)
    :return: private key
    """
    gcd, x, y = get_gcd(nb1, nb2)

    if x < 0:
        x += nb2

    return x


def is_coprime(p, q):
    """
    Checks if 2 primes numbers are coprime
    :param p: first prime number
    :param q: second prime number
    :return: True or False
    """
    # Return True if math.gcd(p, q) == 1
    if math.gcd(p, q) == 1:
        return True
    else:
        return False


def modexp(message, key, n):
    """
    Computes the modular exponentiation used in the encrypt and decrypt methods of RSA
    :param message: The ascii value that has to be elevated
    :param key: The exponent value
    :param n: The modulus
    :return: The result of this function
    """
    # Initializing the result
    result = 1

    # I update the message if it is <= n
    message = message % n

    # If base is 0 then result will be 0
    if message == 0:
        return 0

    # if exp is 0 then result is 0
    if key == 0:
        return 1

    while key > 1:

        if key % 2 == 1:
            result = (result * message) % n

        message = message ** 2 % n
        key = key // 2

    return (message * result) % n


def rsa_enc(pub_key, n, message):
    """
    Applies the RSA encryption method
    :param priv_key: public key to use
    :param n: modulus to use
    :param message: plaintext to encrypt
    :return: an encrypted string
    """
    ciphertext = ""

    # Iterating on each character
    for char in message:
        # Get ascii code for each character
        ascii_code = ord(char)
        ciphertext += str(modexp(ascii_code, pub_key, n)) + " "

    return ciphertext


def rsa_dec(priv_key, n, ciphertext):
    """
    Applies the RSA decryption method
    :param priv_key: private key to use
    :param n: modulus to use
    :param ciphertext: ciphertext to decrypt
    :return: a decrypted string
    """
    decryption = ""

    # Split on the whitespaces and keep the ascii codes
    parts = ciphertext.split()

    for code in parts:
        if code:
            # Converting str to int to compute it
            cipher_value = int(code)
            # Converting into char to concatenate to decrypted string
            decryption += chr(modexp(cipher_value, priv_key, n))

    return decryption


def generate_keys():
    """
    Generates a public and a private key based on great prime numbers
    :return: e = public key, d = private key, n = modulus to use
    """
    # Prime numbers given in primes.txt
    p = 147513732454791286855894116408250922648769471923036927880790753919871952672308331279550605377807291710348597515184859660202801025967131853934063539004405289481737363292768134297535316056328161832744772210538303782101006513784097226420866643633546813327763529407492394840771466569824419814700456992846334731281
    q = 150735041362626454417511646300711556141544472374851217978606636468341071806150452400352225218785400357093050355924724149364822513948644422533623676488140164031920481113890696128286021327454231109796167684696885749396571704094576432688322687991081472100194231663588044246927950986278951923846041547982212150073

    # RSA modulus
    n = p * q

    # Totient
    phi_n = (p - 1) * (q - 1)

    # Choose e
    # e has to be coprime with phi_n AND be 1 < e <= phi_n
    while True:
        # Choosing a random int and checking if it is prime with totient. If it is, then stop loop.
        e = random.randrange(2 ** (1024 - 1), 2 ** 1024 - 1)
        if is_coprime(e, phi_n):
            break

    # Choose d
    # d is the inverted modulus of e with phi_n : e*d (mod phi_n) = 1
    d = modinv(e, phi_n)

    return e, d, n


def attack(ciphertext, n, pub_key):
    """
    First step of the Chosen Cipher text attack
    :param ciphertext: Encrypted text to compute
    :param n: modulus value
    :param pub_key: public key to use
    :return: 2 lists: 1 for the computed result and 1 for the random values
    """
    result = []
    random_values = []

    # Split on the whitespaces and keep the ascii codes
    parts = ciphertext.split()

    for code in parts:
        if code:
            # Converting str to int to compute it
            cipher_value = int(code)
            # Choosing a random value
            random_value = random.randint(0, 200)
            # Converting into char to concatenate to decrypted string
            result.append(str((cipher_value * modexp(random_value, pub_key, n) % n)))
            random_values.append(random_value)

    # Return also a list of the random values so I can reuse them later
    return result, random_values


def main():
    # Start time
    start_time = time.time()

    message = "Hello world!"
    print(f"Message: '{message}'\n")

    ### Key generation ###

    pub_key, priv_key, n = generate_keys()
    print(f"Public key: {pub_key}")
    print(f"Private key: {priv_key}")
    print(f"n: {n}\n")


    ### Encryption ###

    # Start encryption time
    start_enc_time = time.time()

    # Encryption
    ciphertext = rsa_enc(pub_key, n, message)

    # End encryption time
    end_enc_time = time.time()
    # Delta time
    execution_time = end_enc_time - start_enc_time
    print(f"Encryption: {ciphertext}")
    print(f"Encryption time: {execution_time} second\n")


    ### Decryption ###
    # Start decryption time
    start_dec_time = time.time()

    # Decryption
    decryption = rsa_dec(priv_key, n, ciphertext)

    # End decryption time
    end_dec_time = time.time()
    # Delta time
    execution_time = end_dec_time - start_dec_time
    print(f"Decryption: '{decryption}'")
    print(f"Decryption time: {execution_time} second\n")


    ### Chosen ciphertext attack ###

    # 1st step: getting C'
    cipher_attack, random_values = attack(ciphertext, n, pub_key)
    # Making it a list so it can pass my rsa_dec function
    cipher_attack = ' '.join(cipher_attack)
    # Getting the result that has used the priv_key
    attack_decryption = rsa_dec(priv_key, n, cipher_attack)

    result = ""
    for i in range(len(attack_decryption)):
        random_value = random_values[i]
        # based on the result with priv_key, I apply the modinv() to get the initial message
        result += chr((ord(attack_decryption[i]) * modinv(random_value, n)) % n)

    print(f"Chosen Cipher text attack result: '{result}'")


    # End time
    end_time = time.time()
    # Delta time
    execution_time = end_time - start_time
    print('\nProgram execution time:', execution_time, 'second')


if __name__ == '__main__':
    main()
