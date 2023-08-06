from devtreeutil import output as _
from random import randrange as rr
class colors:
    def fRGB(R:int, G:int, B:int):
        if (0<=R<=255) and (0<=G<=255) and (0<=B<=255):
            return f"\x1B[38;2;{str(R)};{str(G)};{str(B)}m"
        else:
            _.print.color.text_color.RED("Error: Value out of range")
            return ""
    def RGB(R:int, G:int, B:int):
        if (0<=R<=255) and (0<=G<=255) and (0<=B<=255):
            return f"\x1B[38;2;{str(R)};{str(G)};{str(B)}m"
        else:
            _.print.color.text_color.RED("Error: Value out of range")
            return ""
    def bRGB(R:int, G:int, B:int):
        if (0<=R<=255) and (0<=G<=255) and (0<=B<=255):
            return f"\x1B[48;2;{str(R)};{str(G)};{str(B)}m"
        else:
            _.print.color.text_color.RED("Error: Value out of range")
            return ""
    bold = "\033[1m"
    underline = "\033[4m"
    italic = "\033[3m"
    faint = "\033[2m"
    strikeout = "\033[9m"
    strike = "\033[9m"
    reset = "\033[0m"
    default = "\033[0m"
class random:
    def fore():
        return colors.fRGB(rr(0,256),rr(0,256),rr(0,256))
    def back():
        return colors.bRGB(rr(0,256),rr(0,256),rr(0,256))