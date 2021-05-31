import numpy as np
import random
from math import gcd

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# RSA
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def is_prime(n) :
    """Returns True if prime and False if not prime"""
    for i in range(2, int(n**0.5)+1) :
        if n%i == 0 :
            return False
    return True


def find_primes() :
    """
    Chooses 2 end points randomly and find 2 random prime numbers between the range
    """
    start, end = np.random.randint(20, 70), np.random.randint(100, 150)
    
    lst = [num for num in range(start, end+1) if is_prime(num)]
    return (random.choice(lst), random.choice(lst))


def find_coprime(n) :
    return random.choice([i for i in range(1, n+1) if gcd(i, n) == 1])


def find_private_key(e, phi_n) :
    '''
    Generates private key from a given public key
    INPUT : e --> first element of the public key
            phi_n --> Euler-Tolient function value of n which is the second element of the public key
    OUTPUT : d --> first element of the private key. Second element is n only
    '''
    i = 1
    while True :
        d = ((phi_n * i) + 1)/e
        if (d*10)%10 == 0 :    #if d is an integer and not a decimal, the loop breaks
            return int(d)
        i += 1


def generate_keys() :
    p, q = find_primes()  #finds 2 prime numbers
    n = p*q

    #euler's totient function 
    phi_n = (p-1) * (q-1)   #since p and q are prime, phi_n(p) = p-1 and since phi_n(p*q) = phi_n(p) * phi_n(q)

    #public key 
    e = find_coprime(phi_n)
    public_key = (e, n)

    #private key generation
    d = find_private_key(e, phi_n)
    private_key = (d, n)

    return (public_key, private_key)


def ascii_convert(lst, toAscii=True) :
    if toAscii :
        return [ord(i) for i in lst] # returns a numpy array of ASCII characters from the text provided
    return "".join([chr(i) for i in lst])  # returns the text string from a list of ASCII characters


def RSA(text, public_key=None, private_key = None, decrypt = False) :
    '''
    Performs RSA encryption and decryption
    INPUT : text --> text to be ciphered or deciphered
            public --> public key in the format of tuple (e, n) can be provided for encryption
            private --> private key in the format of a tuple (d,n) for performing decryption
            decrypt --> flag for indicating that decryption needs to be performed
    '''
    if decrypt :
        #getting ASCII characters from string
        ascii_val = ascii_convert(text, toAscii=True)

        #key
        d, n = private_key
        #getting real Ascii characters
        decipher = [(num**d)%n for num in ascii_val]

        return {"decipher" : ascii_convert(decipher, toAscii=False), "private key" : private_key}

    else :
        ascii_val = ascii_convert(text, toAscii=True)
        
        # if a public key is not provided, generate a pair
        if public_key is None :
            public_key, private_key = generate_keys()
        
        e, n = public_key
        #encrypting
        cipher = [(num**e)%n for num in ascii_val]
        
        return {'cipher' : ascii_convert(cipher, toAscii=False), 'public_key' : public_key, 'private_key' : private_key}
