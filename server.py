# first of all import the socket library
import socket
from hess import *
import time

##########
# User and signature database
##########

dict_user = {}  # User_name: {password, pub_key, pri_key}
dict_msg = {}  # User_name: {msg: {signature}}


##########
# Connection
##########

# next create a socket object
s = socket.socket()
print ("Socket successfully created")

# reserve a port on your computer in our
port = 65532

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))
print ("socket binded to %s" % (port))

# put the socket into listening mode
s.listen(5)
print ("socket is listening")

# a forever loop until we interrupt it or
# an error occurs
while True:
    # Establish connection with client.
    c, addr = s.accept()
    print ('\nGot connection from', addr)

    while(True):
        option = c.recv(1024).decode()

        ######################
        if (option == "Sign"):
            ID = c.recv(1024).decode()

            if (ID in dict_user):
                c.send("ID_yes".encode())

                while(True):
                    pwd = c.recv(1024).decode()
                    if (pwd == dict_user[ID][0]):
                        c.send("pwd_right_yes".encode())
                        break
                    else:
                        c.send("pwd_right_no".encode())

            else:
                c.send("ID_no".encode())
                is_register = c.recv(1024).decode()
                if (is_register == "is_register_no"):
                    break
                else:
                    password = c.recv(1024).decode()
                    (t, Q_TA) = setup_hess(P, l)
                    S_ID = extract_hess(t, ID)
                    dict_user[ID] = [password, Q_TA, S_ID]
                    dict_msg[ID] = {}

            c.send(str(dict_user[ID][1]).encode())
            c.send(str(dict_user[ID][2]).encode())

            msg = c.recv(1024).decode()
            if (msg in dict_msg[ID]):
                c.send("is_msg_in_dict_yes".encode())
                is_replace = c.recv(1024).decode()
                if (is_replace == "is_replace_no"):
                    break

            else:
                c.send("is_msg_in_dict_no".encode())

            sig = sign_hess(msg, dict_user[ID][2], sP)
            dict_msg[ID][msg] = sig
            c.send(str(sig[0]).encode())
            time.sleep(1)
            c.send(str(sig[1]).encode())

        ##########################
        elif (option == "Verify"):
            ID = c.recv(1024).decode()
            if (ID in dict_user):
                c.send("ID_yes".encode())

            else:
                c.send("ID_no".encode())
                c.close()
                break

            msg = c.recv(1024).decode()

            if (msg in dict_msg[ID]):
                c.send("msg_exist_yes".encode())
            else:
                c.send("msg_exist_no".encode())
                c.close()
                break

            if(verify(msg, dict_msg[ID][msg], dict_user[ID][1], ID)):
                c.send("verify_yes".encode())
            else:
                c.send("verify_no".encode())

            break

        elif (option == "Quit"):
            break

        else:
            # print("\nIllegal message, disconnected.")
            break

    # send a thank you message to the client.
    # c.send("\nThank you for connecting".encode())

    # Close the connection with the client
    c.close()
