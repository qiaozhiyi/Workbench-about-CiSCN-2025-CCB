from Crypto.Util.number import *
from tqdm import tqdm
import os

flag=open("./flag.txt","rb").read()
flag=bytes_to_long(flag+os.urandom(2048//8-len(flag)))
e=65537

def get_smooth_prime(bits, smoothness, max_prime=None):
    assert bits - 2 * smoothness > 0
    p = 2
    if max_prime!=None:
        assert max_prime>smoothness
        p*=max_prime
        
    while p.bit_length() < bits - 2 * smoothness:
        factor = getPrime(smoothness)
        p *= factor

    bitcnt = (bits - p.bit_length()) // 2
    while True:
        prime1 = getPrime(bitcnt)
        prime2 = getPrime(bitcnt)
        tmpp = p * prime1 * prime2
        if tmpp.bit_length() < bits:
            bitcnt += 1
            continue
        if tmpp.bit_length() > bits:
            bitcnt -= 1
            continue
        if isPrime(tmpp + 1):
            p = tmpp + 1
            break
    return p

p1=getPrime(512)
q1=getPrime(512)
r1=getPrime(512)
s1=getPrime(512)
n1=p1*q1*r1*s1
assert n1>flag

p=get_smooth_prime(1024,20,p1)
q=get_smooth_prime(1024,20,q1)
r=get_smooth_prime(1024,20,r1)
s=get_smooth_prime(1024,20,s1)
n=p*q*r*s

print(f"[+] inner RSA modulus = {n1}")
print(f"[+] outer RSA modulus = {n}")
print(f"[+] Ciphertext = {pow(flag,e,n1)}")