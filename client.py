# Import socket module
import socket
from hess import *
import time
import sys

# Create a socket object
s = socket.socket()
s.settimeout(100)

# Define the port on which you want to connect
port = 65532

try:
    # connect to the server on local computer
    s.connect(('127.0.0.1', port))
except:

    sys.exit("\nPlease check connection parameters.")

print("\nPlease choose the option:\n"
      "[s] -> Sign\n"
      "[v] -> Verify\n"
      "[q] -> Quit")
option = input().strip("[]")

if (option == 'q'):
    s.send("Quit".encode())
    sys.exit("\nBye.")

elif (option == 's'):
    s.send("Sign".encode())

    print("\nPlease input sign ID:")
    ID = input()
    s.send(ID.encode())

    ID_exist = s.recv(1024).decode()
    if (ID_exist == "ID_no"):
        while (True):
            print("\nWelcome, do you want to register? [y/n]")
            is_register = input().strip("[]")
            if (is_register == 'y' or is_register == 'n'):
                break

        if (is_register == 'n'):
            s.send("is_register_no".encode())
            s.close()
            sys.exit("\nBye.")

        else:
            s.send("is_register_yes".encode())
            while(True):
                print("\nPlease input password:")
                password = input()

                print("\nPlease input password again:")
                password_2 = input()

                if (password != password_2):
                    print("\nPlease check your input.")
                else:
                    s.send(password.encode())
                    break

    else:
        while(True):
            print("\nPlease input password:")
            password = input()
            s.send(password.encode())
            pwd_right = s.recv(1024).decode()
            if (pwd_right == "pwd_right_yes"):
                break

    pub_key = s.recv(1024).decode()
    print("\nYour public key is:\n%s" % str(pub_key))

    pri_key = s.recv(1024).decode()
    print("\nYour private key is:\n%s" % str(pri_key))

    print("\nPlease input your message:")
    msg = input()
    s.send(msg.encode())

    is_msg_in_dict = s.recv(1024).decode()
    if (is_msg_in_dict == "is_msg_in_dict_yes"):
        while(True):
            print("\nThis message already has signiture, replace it? [y/n]")
            is_replace = input().strip("[]")
            if (is_replace == 'y'):
                s.send("is_replace_yes".encode())
                break

            elif (is_replace == 'n'):
                s.send("is_replace_no".encode())
                s.close()
                sys.exit("\nBye.")

    u = s.recv(4024).decode()
    v = s.recv(4024).decode()

    print("\nThe signature is:\n%s\n\n%s" % (u, v))


elif (option == 'v'):
    s.send("Verify".encode())

    print("\nPlease input sender ID:")
    ID = input()
    s.send(ID.encode())

    ID_exist = s.recv(1024).decode()
    if (ID_exist == "ID_no"):
        s.close()
        sys.exit("\nUser not exist.")

    print("\nPlease input your message:")
    msg = input()
    s.send(msg.encode())

    msg_exist = s.recv(1024).decode()
    if (msg_exist == "msg_exist_no"):
        s.close()
        sys.exit("\nMessage not exist.")

    verify_res = s.recv(1024).decode()
    if (verify_res == "verify_yes"):
        print("\nVerify: Passed.")
    else:
        print("\nVerify: Invalid signiture.")

else:
    print("\nIllegal message, disconnected.")

# close the connection
s.close()
