import random
from math import gcd
from sympy import isprime


def modinv(a, m):
    g, x, _ = extended_gcd(a, m)
    if g!= 1:
        raise ValueError("modular inverse does not exist")
    return x % m

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x


def generate_prime(bits):
    while True:
        p = random.getrandbits(bits) | (1 << (bits -1)) | 1
        if isprime(p):
            return p

def rsa_keypair(bits):
    e = 65537
    half_bits = bits // 2
    while True:
        p = generate_prime(half_bits)
        q = generate_prime(half_bits)
        if p == q:
            continue
        N = p * q
        phi = (p-1) * (q-1)
        if gcd(e, phi) == 1:
            d = modinv(e, phi)
            return N, e, d

def mitm_attack(c, N, e, m1, m2):
    mask = (1 << (2* max(m1, m2))) - 1

    table = {}
    for M1 in range(2 ** m1):
        table[ pow(M1, e, N) & mask] = M1

    for M2 in range(1,2**m2 +1):
        l = (c * modinv(pow(M2, e, N), N))% N
        if l & mask in table:
            M1 = table[l & mask]
            M = M1 * M2
            if pow(M, e, N) == c:
                return M
    return None

if __name__ == "__main__":
    m1, m2 = 10, 10
    bits = 256
    N, e, d = rsa_keypair(bits)

    M1 = random.randint(1, 2**m1 -1)
    M2 = random.randint(1, 2**m2 -1)
    M = M1 * M2
    while M >= N:
        M1 = random.randint(1, 2**m1 -1)
        M2 - random.randint(1, 2**m2 -1)
        M = M1 * M2
    
    c = pow(M, e, N)
    print(f"Plaintext: {M} (M1 ={M1}, M2={M2}\n)")
    print(f"Ciphertext: {c}\n")

    result = mitm_attack(c, N, e, m1, m2)
    if result:
        print("\nFound M =", result)
        print("Success" if result == M else "MisMatch error")
    else:
        print("\nAttack Failed")