from Aplicacion import Aplicacion #Se importa la clase Aplicacion

import string
import tkinter
import random

global Nivel
#Nivel = int(input("Digite el nivel "))

def main():
    windows = tkinter.Tk()#Nombre del windows
    Aplicacion(windows)#Envia por parametro el windows
    windows.mainloop()#Inicia el ciclo


if __name__ == '__main__':
    main()