from hess import *
import sys

dict_user = {'admin': 'me'}


if __name__ == "__main__":
    while(True):
        print("\nPlease input your ID:")
        ID = input().strip()
        if (ID not in dict_user):
            print("\nInvalid user, please contact admin.")
            continue
        else:
            break

    (t, Q_TA) = setup_hess(P, l)
    S_ID = extract_hess(t, ID)

    while(True):
        print("\nPlease choose the option:\n"
              "[s] -> Sign\n"
              "[v] -> Verify\n"
              "[q] -> Quit")
        option = input().strip("[]")

        if (option == 'q'):
            sys.exit("\nQuit")

        elif (option == 's'):
            print("\nPlease input your password:")
            pwd = input()
            if(pwd != dict_user[ID]):
                print("\nWrong password, please restart.")
                continue

            print("\nPlease input the message:")
            msg = input()
            sig = sign_hess(msg, S_ID, sP)
            # print("\nThe signiture is:\n%s\n" % sig[0])
            continue

        elif (option == 'v'):
            print("\nPlease input the message:")
            msg = input()

            if(sig == None):
                print("\nPlease firstly sign the message.")
                continue

            if(verify(msg, sig, Q_TA, ID)):
                print("\nVerify: Passed.")
            else:
                print("\nVerify: Invalid signiture.")
            continue

        else:
            print("\nInvalid option, please check.\n")
            continue
