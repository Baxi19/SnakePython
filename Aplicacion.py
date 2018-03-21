#Importa Librerias
import tkinter
import random
import string
#Globales


#Variables
Cabeza = '☺' #Cabeza de la serpiente
Comida = "◉" #Comida
Obstaculos = "▬"#Imagen obstaculo
Vidas = "♥"
#Listas


listaBonus = ["✪", "✪", "✪", "✪", "✪"]

listaBonusEspecial=["☪", "☪", "☪", "☪", "☪"]

Columnas = 250 # columnas de la matriz principal
Filas = 250 #filas de la matriz principal


class Aplicacion():#Clase del juego

    Titulo = 'SNAKE'#titulo del juego
    Tamaño = Columnas, Filas #Establece el tamaño de la matriz

    def __init__(self, windows):#Constructor
        self.puntuacion = 0
        self.validacion1 = False
        self.nivel = 4#Recibirlo por parametro
        self.nivelSelecionado = None
        self.ListaObstaculos = []
        self.windows = windows#Crea el windows
        self.cabeza = None#Cabeza
        self.posicionCabeza = None#Posicion de cabeza
        self.segmentos = []#Cola
        self.posicionSegmento = []#Posicion de cola
        self.alimento = None#Comida
        self.posicionComida = None#Posicion de comida
        self.obstaculo = None
        self.posicionObstaculo = None
        self.vida = 3#Vida hay que cambiar el diseño para llevarlo con un contador
        self.posicionVida = None#Posicion de vida
        self.ListaCorazones = []
        self.ListaCorazones2 = []
        self.vidanivel = None
        self.posicionvidanivel = None
        self.bonus = None#Bonus
        self.posicionBonus = None#Posicion de Bonus
        self.bonusEspecial = None#Bonus Especial
        self.posicionBonusEspecial =None#Posicion Bonus Especial
        self.direccion = None#Direcion
        self.movimiento = True#Movimiento
        self.correr = False#Movimiento de la serpiente por si sola
        self.init()#Llama la funcion

    def init(self):
        self.windows.title(self.Titulo)#Establece el titulo del windows

        self.canvas = tkinter.Canvas(self.windows)
        self.canvas.grid(sticky=tkinter.NSEW)

        self.botonInicio = tkinter.Button(self.windows, text='INICIO', command=self.on_start,fg='White',background="Green")#Crea el botton de inicio
        self.botonInicio.grid(sticky=tkinter.EW)#Posicion del botton de inicio


        pantallaVidas = tkinter.Label(self.windows,text ="VIDAS",fg='Red',background="black")#Crea el mensaje vidas
        pantallaVidas.grid(columnspan=2, rowspan=1, sticky=tkinter.NSEW)#Establece la posicion

        self.pantallaVida = tkinter.Button(self.windows, text=self.vida, fg='Red',background="black")#crea la cantidad de vidas
        self.pantallaVida.grid(columnspan=2, rowspan=2, sticky=tkinter.NSEW)#Establece la posicion

        pantallaNivel = tkinter.Label(self.windows, text="NIVEL", fg='Yellow',background="black")#Crea el msj nivel
        pantallaNivel.grid(columnspan=2, rowspan=1, sticky=tkinter.NSEW)#Establece la posicion

        self.nivelSelecionado = tkinter.Button(self.windows, text=self.nivel, fg='Yellow',background="black")#Establece el nivel
        self.nivelSelecionado.grid(columnspan=2, rowspan=2, sticky=tkinter.NSEW)#Estalece la posicion

        self.windows.bind('8', self.on_up)#Establece los botones para el movimiento
        self.windows.bind('4', self.on_left)#Establece los botones para el movimiento
        self.windows.bind('2', self.on_down)#Establece los botones para el movimiento
        self.windows.bind('6', self.on_right)#Establece los botones para el movimiento

        self.windows.columnconfigure(0, weight=1)#Brinda los limites del windows para jugar(Columnas)
        self.windows.rowconfigure(0, weight=1)#Brinda los limites del windows para jugar(Filas)
        self.windows.resizable(width=True, height=True)#Permite ampliar el windows
        self.windows.geometry('%dx%d' % self.Tamaño)#Tamaño de la matriz

    def on_start(self):
        self.reset()
        if self.correr:
            self.correr = False
            self.botonInicio.configure(text='INICIO')
            self.ListaObstaculos = []
            self.validacion1 = False

        else:

            self.correr = True#Da comienzo al movimiento
            self.botonInicio.configure(text='DETENER Y SALIR',fg= "White",background="Blue")#Actualiza el nombre del boton
            #Aqui hay que guardar los archivos antes de salir
            self.start()

    def reset(self):#Reinicia
        self.segmentos.clear()
        self.posicionSegmento.clear()
        self.canvas.delete(tkinter.ALL)#Destruye el windows

    def start(self):
        ancho = self.canvas.winfo_width()#Metodo
        altura = self.canvas.winfo_height()#Metodo
        print("Tamaño de la pantalla: ")
        print("Base",ancho)
        print("Altura",altura)

        self.canvas.create_rectangle(10, 10, ancho-10, altura-10)#Crea una linea para mostrar al usuario el limite que puede llegar el snake

        self.direccion = random.choice('wasd')#Esto hace que la serpiente no empiece a caminar al momento de iniciar

        posicionCabeza = [round(ancho // 2, -1), round(altura // 2, -1)]#Establece la posicion de la cabeza

        self.cabeza = self.canvas.create_text(tuple(posicionCabeza), text=Cabeza)#Guarda en la posicion que se establecio anteriormente la imagen de la cabeza
        self.posicionCabeza = posicionCabeza#Establece la posicion de la cabez y se imprime el string
        self.spawn_vida()
        self.spawn_bonus()
        self.spawn_food()
        self.produccionObstaculos()
        self.tick()


    def produccionObstaculos(self):
        ancho = self.canvas.winfo_width()
        altura = self.canvas.winfo_height()
        posicionSerpiente = [tuple(self.posicionCabeza), self.posicionComida] + self.posicionSegmento
        #posicionObstaculo = (round(random.randint(20, ancho - 20), -1), round(random.randint(20, altura - 20), -1))

        cabeza = self.cabeza

        posicionObstaculo = (round(random.randint(20, ancho - 20), -1), round(random.randint(20, altura - 20), -1))

        caracterObtaculo = Obstaculos#Establece la imagen
        self.obstaculo = self.canvas.create_text(posicionObstaculo,text=caracterObtaculo)#se carga la imagen al objeto
        self.posicionObstaculo = posicionObstaculo#Establece la posicion
        self.ListaObstaculos.append(self.posicionObstaculo)#Guarda las posiciones de los obstaculos

    # Crea a vida aletoria cada nivel de la serpiente
    def spawn_vida(self):
        if len(self.segmentos) % 5 == 0 and self.validacion1 == True:
            ancho = self.canvas.winfo_width()
            altura = self.canvas.winfo_height()
            posiciones = [tuple(self.posicionCabeza), self.posicionComida] + self.posicionSegmento
            posicion = (round(random.randint(20, ancho - 20), -1), round(random.randint(20, altura - 20), -1))
            self.posicion = posicion
            posicionCabeza = [round(ancho // 2, -1),
                              round(altura // 2, -1)]  # Establece la posicdion de la cabeza para iniciar
            cabeza = self.cabeza

            while ((posicion in posiciones) and (posicion != cabeza)):
                lista = self.ListaObstaculos
                for x in lista:
                    if x == posicion:
                        self.spawn_food()
                        # posicion = (round(random.randint(20, ancho-20), -1), round(random.randint(20, altura-20), -1))
            caracter = Vidas  # se define la imagen de la bonus
            self.vidanivel = self.canvas.create_text(posicion, text=caracter)  # se carga la imagen al objeto
            self.posicionvidanivel = posicion  # Establece la pocicion de la bonus
            # se establece el objeto bonus


    def spawn_bonus(self):
        if len(self.segmentos) % 2 == 0 and self.validacion1 == True:
            ancho = self.canvas.winfo_width()
            altura = self.canvas.winfo_height()

            posiciones = [tuple(self.posicionCabeza), self.posicionComida] + self.posicionSegmento
            posicion = (round(random.randint(20, ancho - 20), -1), round(random.randint(20, altura - 20), -1))
            self.posicion = posicion

            posicionCabeza = [round(ancho // 2, -1),
                              round(altura // 2, -1)]  # Establece la posicdion de la cabeza para iniciar
            cabeza = self.cabeza

            while ((posicion in posiciones) and (posicion != cabeza)):
                lista = self.ListaObstaculos
                for x in lista:
                    if x == posicion:
                        self.spawn_vida()
                        self.spawn_bonus()
                        self.spawn_food()
                        # posicion = (round(random.randint(20, ancho-20), -1), round(random.randint(20, altura-20), -1))
            caracter = Vidas  # se define la imagen de la bonus

            self.bonus = self.canvas.create_text(posicion, text=caracter)  # se carga la imagen al objeto
            self.posicionBonus = posicion  # Establece la pocicion de la bonus
            # se establece el objeto bonus
        self.validacion1 = True

    #Crea la comida para la serpiente
    def spawn_food(self):
        ancho = self.canvas.winfo_width()
        altura = self.canvas.winfo_height()

        posiciones = [tuple(self.posicionCabeza), self.posicionComida] + self.posicionSegmento
        posicion = (round(random.randint(20, ancho-20), -1), round(random.randint(20, altura-20), -1))

        posicionCabeza = [round(ancho // 2, -1), round(altura // 2, -1)]# Establece la posicion de la cabeza para iniciar
        cabeza = self.cabeza

        while ((posicion in posiciones) and (posicion != cabeza)):
            lista = self.ListaObstaculos
            for x in lista:
                if x == posicion:
                    self.spawn_vida()
                    self.spawn_bonus()
                    self.spawn_food()
            #posicion = (round(random.randint(20, ancho-20), -1), round(random.randint(20, altura-20), -1))
        caracter = Comida#se define la imagen de la comida

        self.alimento = self.canvas.create_text(posicion, text=caracter)#se carga la imagen al objeto
        self.posicionComida = posicion#Establece la pocicion de la comida
        self.comida = caracter#se establece el objeto comida


    def tick(self):
        ancho = self.canvas.winfo_width()
        altura = self.canvas.winfo_height()
        posicionAnteriorCabeza = tuple(self.posicionCabeza)


        if self.direccion == '8':
            self.posicionCabeza[1] -= 10
        elif self.direccion == '4':
            self.posicionCabeza[0] -= 10
        elif self.direccion == '2':
            self.posicionCabeza[1] += 10
        elif self.direccion == '6':
            self.posicionCabeza[0] += 10

        posicionCabeza = tuple(self.posicionCabeza)

        if (self.posicionCabeza[0] < 10 or self.posicionCabeza[0] >= ancho-10 or
            self.posicionCabeza[1] < 10 or self.posicionCabeza[1] >= altura-10 or
            any(posicionSegmento == posicionCabeza for posicionSegmento in self.posicionSegmento)):
            self.game_over()
            return

        # Elimina la imagen de vida de la pantalla y la agrega en dado caso
        if posicionCabeza == self.posicionvidanivel:
            self.posicionvidanivel = None
            if self.vida < 3:
                self.vida = self.vida + 1
            self.canvas.delete(self.vidanivel)


        if posicionCabeza == self.posicionBonus:
            self.posicionBonus = None
            if self.vida < 3:
                self.vida = self.vida + 1
                self.pantallaVida.configure(text=self.vida)
                print(self.vida)
            self.canvas.delete(self.bonus)


        #Aumenta el tamaño de la serpiente
        if posicionCabeza == self.posicionComida:
            self.canvas.coords(self.alimento, posicionAnteriorCabeza)
            self.segmentos.append(self.alimento)
            self.posicionSegmento.append(posicionAnteriorCabeza)

            # Aumenta Nivel
            if self.segmentos:
                cuerpo = len(self.segmentos)
                if (cuerpo) % 5 == 0:
                    velocidad = self.nivel
                    print("Velocidad :", velocidad)
                    velocidad += 1
                    self.nivel = velocidad
                    print("Velocidad :", velocidad)
                    self.nivelSelecionado.configure(text=self.nivel)  # Actualiza el nombre del boton
                    self.spawn_vida()
                    self.spawn_bonus()
                    self.spawn_food()

                self.produccionObstaculos()
                self.spawn_vida()
                self.spawn_bonus()
                self.spawn_food()

        # calcula los obstaculos
        if posicionCabeza:
            lista = self.ListaObstaculos #Auxiliar para recorrer los valores
            for x in lista:
                if posicionCabeza == x:
                    self.game_over()
                    return

        #Calcula los corazones
        if posicionCabeza:
            corazon = self.posicionVida
            if posicionCabeza == corazon:
                calculoVida = self.vida
                if calculoVida < 3:
                    calculoVida += 1
                    self.vida = calculoVida
                    print("Vida: ", self.vida)
                    #self.produccionVidas()

                print("Vida :",self.vida)

        if self.segmentos:
            posicionAnterior = posicionAnteriorCabeza
            for index, (segmentos, posicion) in enumerate(zip(self.segmentos, self.posicionSegmento)):
                self.canvas.coords(segmentos, posicionAnterior)
                self.posicionSegmento[index] = posicionAnterior
                posicionAnterior = posicion
        self.canvas.coords(self.cabeza, posicionCabeza)
        self.movimiento = True

        #Se encarga de brindar la velocidad dependiendo del dato del nivel
        if self.correr:
            aux = 1001
            nivel = (self.nivel) * 150
            velocidad = aux - nivel
            self.canvas.after(velocidad, self.tick)#Actualiza la velocidad de la serpiente

    def game_over(self):
        vida = self.vida
        vida -= 1
        self.vida = vida
        ancho = self.canvas.winfo_width()
        altura = self.canvas.winfo_height()
        self.correr = False
        self.pantallaVida.configure(text=self.vida)
        self.botonInicio.configure(text='INICIO', command=self.on_start,fg='White',background="Green")
        self.ListaObstaculos = []
        if self.vida > 0:

            puntuacion = len(self.segmentos)
            resultado = puntuacion * 10
            calculo = puntuacion + resultado
            aux = self.puntuacion
            calculo2 = calculo + aux
            self.puntuacion = calculo2
            self.canvas.create_text((round(ancho // 2, -1), round(altura // 2, -1)),
                                    text=("Perdio una Vida!!\n", "Su puntuacion es de: \n", self.puntuacion))
            self.start()

        else:

            puntuacion = len(self.segmentos)
            resultado = puntuacion * 10
            calculo = puntuacion + resultado
            aux = self.puntuacion
            calculo2 = calculo + aux
            self.puntuacion = calculo2
            self.canvas.create_text((round(ancho // 2, -1), round(altura // 2, -1)),
                                text =("JUEGO TERMINADO!!\n","Su puntuacion es de: \n",puntuacion))
            return 0
    #Funcion de movimiento y restricciones
    def on_up(self, event):
        if self.movimiento and not self.direccion == '2':#Restricciones de movimientos
            self.direccion = '8'
            self.movimiento = False

    # Funcion de movimiento y restricciones
    def on_down(self, event):
        if self.movimiento and not self.direccion == '8':#Restricciones de movimientos
            self.direccion = '2'
            self.movimiento = False

    # Funcion de movimiento y restricciones
    def on_left(self, event):
        if self.movimiento and not self.direccion == '6':#Restricciones de movimientos
            self.direccion = '4'
            self.movimiento = False

    # Funcion de movimiento y restricciones
    def on_right(self, event):
        if self.movimiento and not self.direccion == '4':#Restricciones de movimientos
            self.direccion = '6'
            self.movimiento = False
