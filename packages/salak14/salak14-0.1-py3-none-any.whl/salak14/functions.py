import ctypes
import time
import webbrowser
import base64
from sys import platform
import os


def encode(s):
    newstr = s
    newstr_bytes = newstr.encode("ascii")
    coded = str(base64.standard_b64encode(newstr_bytes))
    coded2 = coded.replace("==", "")
    coded3 = coded2.replace("'", "")

    return (coded3[1:])


def decode(s):
    newstr = s
    newstr_bytes = str(newstr + '==').encode("ascii")
    coded = str(base64.standard_b64decode(newstr_bytes))
    coded2 = coded.replace("'", "")
    return (coded2[1:])


def przegladarka():
    webbrowser.open("google.com")


def opencd(a):
    if platform == "linux" or platform == "linux2":
        os.system("eject cdrom")
    elif platform == "win32":
        ctypes.windll.WINMM.mciSendStringW(u"open "+a+": type cdaudio alias "+a.lower+"_drive", None, 0, None)
        ctypes.windll.WINMM.mciSendStringW(u"set "+a.lower+"_drive door open", None, 0, None)


def closecd(a):
    if platform == "linux" or platform == "linux2":
        os.system("inject cdrom")
    elif platform == "win32":
        ctypes.windll.WINMM.mciSendStringW(u"open "+a+": type cdaudio alias "+a.lower+"_drive", None, 0, None)
        ctypes.windll.WINMM.mciSendStringW(u"set "+a.lower+"_drive door closed", None, 0, None)


def Papiez():
    while True:
        time.sleep(1)
        ctypes.windll.WINMM.mciSendStringW(u"open I: type cdaudio alias i_drive", None, 0, None)
        ctypes.windll.WINMM.mciSendStringW(u"set i_drive door open", None, 0, None)
        time.sleep(1)
        ctypes.windll.WINMM.mciSendStringW(u"open I: type cdaudio alias i_drive", None, 0, None)
        ctypes.windll.WINMM.mciSendStringW(u"set i_drive door closed", None, 0, None)