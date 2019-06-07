from ecpy import ExtendedFiniteField, MapToPoint
from ecpy import EllipticCurveRepository, EllipticCurve
from ecpy import symmetric_weil_pairing
import hashlib
import _pickle as cPickle
import random
import gmpy2
import time

# Parameter taken from Cryptography and Elliptic Curves by TSUJII et al.
p = gmpy2.mpz("501794446334189957604282155189438160845433783392772743395579628"
              "617109929160215221425142482928909270259580854362463493326988807"
              "45359574857376419559953437557")

l = gmpy2.mpz((p + 1) // 6)

F = ExtendedFiniteField(p, "x^2+x+1")
E = EllipticCurve(F, 0, 1)  # y^2 = x^3 + 1

P = E(3, gmpy2.mpz("1418077311270457886139292292020587683642898636677353664354"
                   "1011717684401801069777797699258667061922178009879315047772"
                   "033936311133535564812495329881887557081"))


sP = E(gmpy2.mpz("129862491850266001914601437161941818413833907050695770313188"
                 "660767152646233571458109764766382285470424230719843324368007"
                 "92537535129539576510740045312772012"),
       gmpy2.mpz("452543250979361708074026409576755302296698208397782707067096"
                 "515523033579018123253402743775747767548650767928190884624134"
                 "82786913791124188897792458334596297"))


# Hash map to point
def H(ID):
    hash_ID = gmpy2.mpz(hashlib.sha512(ID.encode("utf-8")).hexdigest(), 16)
    res = MapToPoint(E, E.field(hash_ID))
    return res


# Hash to number
def h(m, r):
    def pairing_to_int(x):
        return x.x * x.field.p + x.y
    hash_m = gmpy2.mpz(hashlib.sha512(m.encode("utf-8")).hexdigest(), 16)
    res = pairing_to_int(E.field(hash_m * r))
    return res


# Generate public and private parameters
def setup_hess(P, l):
    t = gmpy2.mpz(random.randint(l // 2, l))
    Q_TA = t * P
    return (t, Q_TA)


# Generate ID secret key
def extract_hess(t, ID):
    hash_ID = H(ID)
    S_ID = t * hash_ID
    return S_ID


# Sign message with sercet key
def sign_hess(m, S_ID):

    k = gmpy2.mpz(random.randint(1, l))
    P1 = gmpy2.mpz(random.randint(1, l)) * P
    r = pow((symmetric_weil_pairing(E, P, P1, l)), k)

    v = h(m, r)

    u = v * S_ID + k * P1
    return (u, v)


# Verify with public parameter
def verify(m, sig, Q_TA, ID):
    left = symmetric_weil_pairing(E, sig[0], P, l)
    hash_ID = H(ID)
    right = pow(symmetric_weil_pairing(E, hash_ID, -Q_TA, l), sig[1])
    r = left * right
    if (sig[1] == h(m, r)):
        return True
    else:
        return False
