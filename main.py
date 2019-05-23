from hess import *
import sys

if __name__ == "__main__":
    print("Please input your ID:")
    ID = input().strip()

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
