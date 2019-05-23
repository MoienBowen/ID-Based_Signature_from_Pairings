from ecpy import ExtendedFiniteField, EllipticCurve, MapToPoint
from ecpy import symmetric_weil_pairing
import hashlib
import _pickle as cPickle
import random


p = int("501794446334189957604282155189438160845433783392772743395579628617109"
        "929160215221425142482928909270259580854362463493326988807453595748573"
        "76419559953437557")

l = (p + 1) // 6

F = ExtendedFiniteField(p, "x^2+x+1")
E = EllipticCurve(F, 0, 1)

P = E(3, int("1418077311270457886139292292020587683642898636677353664354101171"
             "7684401801069777797699258667061922178009879315047772033936311133"
             "535564812495329881887557081"))
sP = E(int("129862491850266001914601437161941818413833907050695770313188660767"
           "152646233571458109764766382285470424230719843324368007925375351295"
           "39576510740045312772012"),
       int("452543250979361708074026409576755302296698208397782707067096515523"
           "033579018123253402743775747767548650767928190884624134827869137911"
           "24188897792458334596297"))


def H(ID):
    hash_ID = int(hashlib.sha512(ID.encode("utf-8")).hexdigest(), 16)
    res = MapToPoint(E, E.field(hash_ID))
    return res


def h(m, r):
    def pairing_to_int(x):
        return x.x * x.field.p + x.y
    hash_m = int(hashlib.sha512(m.encode("utf-8")).hexdigest(), 16)

    return pairing_to_int(E.field(hash_m * r))

    # return (hash_m * r)


def setup_hess(P, l):
    t = random.randint(l / 2, l)
    Q_TA = t * P
    return (t, Q_TA)


def extract_hess(t, ID):
    hash_ID = H(ID)
    S_ID = t * hash_ID
    return S_ID


def sign_hess(m, S_ID, P1):
    # r
    k = random.randint(l // 2, l)
    r = pow((symmetric_weil_pairing(E, P1, P, l)), k)
    # v
    v = h(m, r)
    # u
    u = v * S_ID + k * P1
    return (u, v)


def verify(m, sig, Q_TA, ID):
    left = symmetric_weil_pairing(E, sig[0], P, l)
    hash_ID = H(ID)
    right = pow(symmetric_weil_pairing(E, hash_ID, -Q_TA, l), sig[1])
    r = left * right
    if (sig[1] == h(m, r)):
        return True
    else:
        return False
