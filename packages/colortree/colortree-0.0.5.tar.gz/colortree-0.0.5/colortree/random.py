from random import randrange as rr
def fore():
    return f"\x1B[38;2;{str(rr(0,256))};{str(rr(0,256))};{str(rr(0,256))}m"
def back():
    return f"\x1B[48;2;{str(rr(0,256))};{str(rr(0,256))};{str(rr(0,256))}m"