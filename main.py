from hess import *
import sys

dict_user = {'admin': 'me', 'tester': 'tester'}
dict_msg = dict((user, {}) for user in dict_user.keys())


if __name__ == "__main__":
    (t, Q_TA) = setup_hess(P, l)

    dict_S_ID = dict((user, {}) for user in dict_user.keys())
    for each_id in dict_S_ID.keys():
        dict_S_ID[each_id] = extract_hess(t, each_id)

    while(True):
        print("\nPlease choose the option:\n"
              "[s] -> Sign\n"
              "[v] -> Verify\n"
              "[q] -> Quit")
        option = input().strip("[]")

        if (option == 'q'):
            sys.exit("\nQuit")

        elif (option == 's'):

            print("\nPlease input sign ID:")
            ID = input().strip()
            if (ID not in dict_user):
                print("\nInvalid user, please contact admin.")
                continue

            print("\nPlease input your password:")
            pwd = input()
            if(pwd != dict_user[ID]):
                print("\nWrong password, please restart.")
                continue

            print("\nPlease input the message:")
            msg = input()

            while(msg in dict_msg[ID]):
                print("\nThis message already has signiture, "
                      "replace it? [y/n]")
                while(is_replace != 'y' and is_replace != 'n'):
                    print(
                        "\nThis message already has signiture, replace it? [y/n]")
                    is_replace = input()
                    if (is_replace == 'y' or is_replace == 'Y'):
                        break
                    elif (is_replace == 'n' or is_replace == 'N'):
                        print("\nPlease input the message:")
                        msg = input()

            sig = sign_hess(msg, dict_S_ID[ID], sP)
            dict_msg[ID][msg] = sig
            # print("\nThe signiture is:\n%s\n" % sig[0])
            continue

        elif (option == 'v'):
            print("\nPlease input verify ID:")
            ID = input().strip()
            if (ID not in dict_user):
                print("\nInvalid user, please contact admin.")
                continue

            print("\nPlease input the message:")
            msg = input()
            if (msg not in dict_msg[ID]):
                print("\nNo signiture for this user and message.")
                continue

            if(verify(msg, dict_msg[ID][msg], Q_TA, ID)):
                print("\nVerify: Passed.")
            else:
                print("\nVerify: Invalid signiture.")
            continue

        else:
            print("\nInvalid option, please check.\n")
            continue
