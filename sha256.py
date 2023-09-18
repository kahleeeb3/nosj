import hashlib # perform a hash
import binascii
import random
import string
import time


def main():
    email = "cmp0132@auburn.edu" # initial input
    expected_collision = get_expected_digest(email) # store the expected collision

    start_time = time.time()
    while True:
        random_string_len = 32 - len(email)
        random_string = get_random_input(random_string_len) # generate random string
        random_string = email + random_string # append random string to email
        # print(random_string) # print every value
        sha_value = get_sha_value(random_string) # get the sha value
        if sha_value[:8] == expected_collision: # if the first 4 bytes match what they should
            print(random_string)
            break

    # evaluate runtime    
    end_time = time.time()
    runtime = end_time - start_time
    print(f"Runtime: {runtime} seconds")


def get_random_input(length):
    """
    generate a random string of a set lenth from a set of ascii chars
    """
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def get_expected_digest(input_string):
    """
    The leading 3 bytes of the digest must be the letters of your
    auburn email address followed by a null byte when encoded in hex.
    """
    input_string = input_string[:3] # get the first 3 letters of the input string
    input_bytes = input_string.encode('utf-8') # encode input as bytes
    hex_value = binascii.hexlify(input_bytes).decode('utf-8') # get the hex value
    hex_value += '00' # append null byte
    return hex_value

def get_sha_value(input_string):
    """
    Converts input string to a sha256 digest
    """
    sha256_hash = hashlib.sha256() # Create a SHA-256 hash object
    input_bytes = input_string.encode('utf-8') # encode input as bytes
    sha256_hash.update(input_bytes) # find the hash value
    digest = sha256_hash.hexdigest() # hash to hex
    return digest


if __name__=="__main__":
    main()