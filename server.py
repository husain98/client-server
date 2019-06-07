import socket
import random
import textwrap
'''
Euclid's algorithm for determining the greatest common divisor
Use iteration to make it faster for larger integers
'''
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

'''
Euclid's extended algorithm for finding the multiplicative inverse of two numbers
'''
def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2- temp1* x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi

'''
Tests to see if a number is prime.
'''
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    #n = pq
    n = p * q

    #Phi is the totient of n
    phi = (p-1) * (q-1)

    #Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    #Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    #Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    #Return public and private keypair
    #Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))
p = 59;q = 73
public, private = generate_keypair(p, q)
key = str(public[0])
n = str(public[1])

def encrypt(pk, plaintext):
    #Unpack the key into it's components
    key, n = pk
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m
    
    cipher=[pow(ord(char),key,n) for char in plaintext]

    #Return the array of bytes
    return cipher

def encrypt1(pk, plaintext):
    #Unpack the key into it's components
    key, n = pk
    x=''
    cipher=[]
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m
    for char in plaintext:
        if(char!=','):
            x=x+str(pow(ord(char),key,n))
        else:
         cipher.append(x)
         x=''
         

    #Return the array of bytes
    return cipher

def decrypt(pk, ciphertext):
    #Unpack the key into its components
    key, n = pk
    #Generate the plaintext based on the ciphertext and key using a^b mod m

    plain=[(chr(pow(char,key,n))) for char in ciphertext]
    #Return the array of bytes as a string
    return plain



# get the hostname
host = socket.gethostname()
port = 5000  # initiate port no above 1024

server_socket = socket.socket()  # get instance
# look closely. The bind() function takes tuple as argument
server_socket.bind((host, port))  # bind host address and port together

# configure how many client the server can listen simultaneously
server_socket.listen(2)
conn, address = server_socket.accept()  # accept new connection
print("Connection from: " + str(address))

conn.send(key.encode())
conn.send(n.encode())

data=(conn.recv(1024).decode())
publicr=data.split(',')
key = int(publicr[0])#generate keys from client
n = int(publicr[1])#generate keys from client
publicr = (key, n)



while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        ch=int(input('enter 1 to decrypt Encrypted Key->\nenter 2 to Validate Digital Signature'))
        if(ch==1):
           decry=data.split(',')
           decry=list(map(int,decry))
           print('Decrypting....')
           print(''.join(decrypt(private, decry)))
        if(ch==2):
         decry=data.split(',')
         decry=list(map(int,decry))
         print('Decrypting....')
         data=''.join(decrypt(publicr, decry))
         data1=textwrap.wrap(data,4)
         decry1=list(map(int,data1))
         print(decry1)
         print(''.join(decrypt(private,decry1)))

        print('''Select from the following
                 1.Encryption
                 2.Add Digital Signature->''')
        ch=int(input())
        if(ch==1):
            data=input('Enter message to be encrypted ->')
            encrypted_msg = encrypt(publicr, data)
            print ("Your encrypted message is: ")
            print (''.join(map(lambda x: str(x), encrypted_msg)))
            conn.send(','.join(map(lambda x: str(x), encrypted_msg)).encode())  # send data to the client
        if(ch==2):
         message = input("Enter a message to encrypt ->")# take input
         encrypted_msg = encrypt(publicr, message)
         message1=''.join(map(lambda x: str(x), encrypted_msg))
         encrypted_msg=encrypt(private,message1)
         print ("Your encrypted message is: ")
         print (''.join(map(lambda x: str(x), encrypted_msg))) # again take input
         conn.send(','.join(map(lambda x: str(x), encrypted_msg)).encode())
conn.close()  # close the connection


