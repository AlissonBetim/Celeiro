from os import system, name
from time import sleep

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def txt_cor(txt,cor):
    if cor == "verde":
        tm = (len(txt) + 8)
        print(f'\033[2;32m{txt}\033[37m')
    if cor == "amarelo":
        tm = (len(txt) + 8)
        print(f'\033[2;33m{txt}\033[37m')

def sublinha(txt, tamanho=40):
        print (f'\033[1;33m_' * tamanho)
        print (f"\n\033[1;33m  {txt} ")
        print ('\033[33m_\033[0;37m' * tamanho)


def txt_negrito (txt,):
        print (f"\033[1;37m {txt}\033[0;37m ")


def erro(txt):
        print (f"\033[1;31m  {txt} !!")
        sleep(1)


def limpa_int (txt):
        txt2 = int(str(txt).strip(")'(,][}{,"))
        return txt2


def limpa_float (txt):
        txt2 = str(txt).strip(")'(,][}{,")
        #txt2 = float(txt2)
        return txt2
