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
p = 31;q = 53
public, private = generate_keypair(p, q)
key=str(public[0])
n=str(','+str(public[1]))

def encrypt(pk, plaintext):
    #Unpack the key into it's components
    key, n = pk
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m

    cipher=[pow(ord(char),key,n) for char in plaintext]

    #Return the array of bytes
    return cipher

def decrypt(pk, ciphertext):
    #Unpack the key into its components
    key, n = pk
    #Generate the plaintext based on the ciphertext and key using a^b mod m

    plain=[(chr(pow(char,key,n))) for char in ciphertext]
    #Return the array of bytes as a string
    return plain

host = socket.gethostname()  # as both code is running on same pc
port = 5000  # socket server port number

client_socket = socket.socket()  # instantiate
client_socket.connect((host, port))  # connect to the server
client_socket.send(key.encode())# sending public key to server
client_socket.send(n.encode())# sending public key to server

data = client_socket.recv(1024).decode()
data1 = client_socket.recv(1024).decode()
publicr=[data, data1]
key = int(publicr[0])#generate keys from client
n = int(publicr[1])#generate keys from client
publicr = (key, n)


print('''Select from the following
         1.Encrypt Message
         2.Add digital signature->''')
choice = int(input())
if (choice == 1):
 message = input("Enter a message to encrypt ->")# take input
 encrypted_msg = encrypt(publicr, message)
 print ("Your encrypted message is: ")
 print (''.join(map(lambda x: str(x), encrypted_msg)))

if(choice==2):
    message = input("Enter a message to encrypt ->")# take input
    encrypted_msg = encrypt(publicr, message)
    message1=''.join(map(lambda x: str(x), encrypted_msg))
    print(','.join(map(lambda x: str(x), encrypted_msg)))
    encrypted_msg=encrypt(private,message1)
    print ("Your encrypted message is: ")
    print (''.join(map(lambda x: str(x), encrypted_msg))) # again take input

while message.lower().strip() != 'bye':

        client_socket.send(','.join(map(lambda x: str(x), encrypted_msg)).encode())  # send message

        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal
        ch=int(input('Enter 1 to decrypt encrpyted message ->\n'
                     'Enter 2 to decrypt digital signature ->'))
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
                 1.Encrypt Message
                 2.Add digital signature->''')
        choice = int(input())
        if (choice == 1):
         message = input("Enter a message to encrypt ->")# take input
         encrypted_msg = encrypt(publicr, message)
         print ("Your encrypted message is: ")
         print (''.join(map(lambda x: str(x), encrypted_msg))) # again take input
        if(choice==2):
            message = input("Enter a message to encrypt ->")# take input
            encrypted_msg = encrypt(publicr, message)
            message1=''.join(map(lambda x: str(x), encrypted_msg))
            print(','.join(map(lambda x: str(x), encrypted_msg)))
            encrypted_msg=encrypt(private,message1)
            print ("Your encrypted message is: ")
            print (','.join(map(lambda x: str(x), encrypted_msg))) # again take input


client_socket.close()  # close the connection


