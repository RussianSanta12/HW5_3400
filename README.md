to run this file the only dependency needed is 

sympy by running: pip install sympy 

for submision purposes 
m1 and m2 are set 10 and the bits are set to 256 modify them for larger and smaller messages

How this code works is that it RSA encrypts a message M as c = M^e mod N. and the attack exploits messages that are written as M = M1 * M2 with M1 < 2^m1 and M2 < 2^m2 
The first phase is building a table by computing M1^e mod N for all M1 in [0, 2^m1) and storing it in a hash table
the second phase is searching. for each M2 in [1, 2^m2] compute c * (m2^e)^-1 mod N and look for it in the table if hit is given when M = M1 * M2
