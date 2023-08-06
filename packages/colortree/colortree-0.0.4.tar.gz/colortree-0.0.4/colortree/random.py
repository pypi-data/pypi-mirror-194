from random import randrange as rr
from colors import fRGB as _f, bRGB as _b
def fore():
    return _f(rr(0,256),rr(0,256),rr(0,256))
def back():
    return _b(rr(0,256),rr(0,256),rr(0,256))