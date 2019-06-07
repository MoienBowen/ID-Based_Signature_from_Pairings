from hess import *
from time import time

ID = "admin"
msg = "plaintext"


if __name__ == "__main__":

    (t, Q_TA) = setup_hess(P, l)
    S_ID = extract_hess(t, ID)
    sig = sign_hess(msg, S_ID)
    res = verify(msg, sig, Q_TA, ID)
    print(res)

# For time using test
