# Source Generated with Decompyle++
# File: obf_secsy_ctf.pyc (Python 3.10)

import base64
import sys
FLAG = b'VmcgRiBnVXIgamViYXQgc3ludCBudG52YSE='
FLAGGG = b'TGJoIHVuaXIgc2JoYVEgZ3VyIGplQmF0IHNZbnQh'

def f1(input):
    O00OOO00OO0O00O00 = str.maketrans('NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm', 'ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz')
    if input.decode('UTF-8').translate(O00OOO00OO0O00O00) == base64.b64decode('WmwgRmFueHIgdmYgRXJueXlsIFBiYnkh').decode('UTF-8').translate(O00OOO00OO0O00O00).replace(' ', '_'):
        print(base64.b64decode('UGJhdGVuZ2YgOiA=').decode('UTF-8').translate(O00OOO00OO0O00O00) + base64.b64decode('WmwgRmFueHIgdmYgRXJueXlsIFBiYnkh').decode('UTF-8').translate(O00OOO00OO0O00O00).replace(' ', '_'))
        return None
    None(base64.b64decode(FLAG).decode('UTF-8').translate(O00OOO00OO0O00O00).lower())

# Flag : My_Snake_is_Really_Cool!

def junk(OO0OOO000000O0000):
    OO0O0O00OOOOO0OO0 = 7
    OO00000O000OO0O0O = OO0OOO000000O0000.upper().format('UTF-8')
    return OO0OOO000000O0000


def to_b64(user_input):
    if base64.b64encode(user_input) == FLAGGG:
        print(base64.b64decode(FLAG))
    OOO000000OOO00OOO = str.maketrans('NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm', 'ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz')
    if user_input.decode('UTF-8').translate(OOO000000OOO00OOO) == base64.b64decode(FLAG).decode('UTF-8').translate(OOO000000OOO00OOO).replace(' ', '_'):
        print(base64.b64decode(FLAG).decode('UTF-8').translate(OOO000000OOO00OOO).replace(' ', '_').lower())
    f1(user_input)


def main():
    print('Reverse Me :\n------------')
    if len(sys.argv) > 1:
        ROT13_1 = str.maketrans('ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz', 'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm')
        to_b64(bytes(sys.argv[1].translate(ROT13_1), 'UTF-8'))
        return None
    None('Usage : python3 ctf.py password')

main()
