# Created by Antoni Marcinek and Kacper Kureń at Collegium Da Vinic

import random
import math

key_size = 16

def get_prime(keysize):
    while True:
        is__not_prime = False
        num = random.randrange(2**(keysize-1), 2**keysize)        
        for i in range(2, round(math.sqrt(num))):
            if (num % i == 0):
                is__not_prime = True
                break
        
        if(not is__not_prime):
            return num

def get_e(euler):
    # NWD(e, euler) = 1
    e = 2
    while True:
        if (math.gcd(e, euler) == 1):
            return e
        e += 1

def get_d(e, euler):
    d = 2
    while True:
        if((d*e)%euler == 1):
            return d
        d += 1 

def generate_keys():
    print("Generating keys...")
    p = get_prime(key_size // 2)
    q = get_prime(key_size // 2)

    n = p*q
    euler = (p-1)*(q-1)

    e = get_e(euler)
    d = get_d(e, euler)
    return e, d, n