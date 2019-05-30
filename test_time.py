from hess import *
from time import time

ID = "admin"
msg = "plaintext"


if __name__ == "__main__":

    (t, Q_TA) = setup_hess(P, l)
    S_ID = extract_hess(t, ID)
    sig = sign_hess(msg, S_ID, sP)
    verify(msg, sig, Q_TA, ID)

# For time using test
