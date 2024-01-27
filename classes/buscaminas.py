import tkinter as tk
from tkinter import messagebox, simpledialog
import random

def generar_tablero(filas, columnas, minas):
    tablero = [[0] * columnas for _ in range(filas)]
    for _ in range(minas):
        fila, columna = random.randint(0, filas-1), random.randint(0, columnas-1)
        while tablero[fila][columna] == -1:
            fila, columna = random.randint(0, filas-1), random.randint(0, columnas-1)
        tablero[fila][columna] = -1
        for i in range(fila-1, fila+2):
            for j in range(columna-1, columna+2):
                if 0 <= i < filas and 0 <= j < columnas and tablero[i][j] != -1:
                    tablero[i][j] += 1
    return tablero

class Buscaminas():
    def __init__(self, master, filas, columnas, minas,nivel, menu,icono_bomba = "※",icono_seleccion = "✖︎" ):
        self.master = master
        self.filas = filas
        self.columnas = columnas
        self.minas = minas
        self.menu = menu
        self.nivel = nivel
        self.vidas = 3
        self.puntaje = 0
        self.liberadas= 0
        self.icono_bomba = icono_bomba
        self.icono_seleccion = icono_seleccion
        self.tablero = generar_tablero(filas, columnas, minas)
        self.casillas_descubiertas = set()
    
        self.frame_juego = tk.Frame(master)
        self.frame_juego.pack(expand=True)

        self.label_vidas = tk.Label(self.frame_juego, text=f"Vidas: {self.vidas}", font=("Helvetica", 12))
        self.label_vidas.grid(row=0, column=0, columnspan=columnas // 2, sticky="w")

        self.label_puntaje = tk.Label(self.frame_juego, text=f"Puntaje: {self.puntaje}", font=("Helvetica", 12))
        self.label_puntaje.grid(row=0, column=columnas // 2, columnspan=columnas // 2, sticky="e")

        self.botones = [[None] * columnas for _ in range(filas)]
        for fila in range(filas):
            for columna in range(columnas):
                boton = tk.Button(self.frame_juego, width=2, height=1, command=lambda f=fila, c=columna: self.clic(f, c))
                boton.grid(row=fila + 1, column=columna)
                boton.bind('<Button-3>', lambda event, f=fila, c=columna: self.marcar_casilla(event, f, c))
                self.botones[fila][columna] = boton

        self.frame_botones = tk.Frame(master)
        self.frame_botones.pack()

        boton_reiniciar = tk.Button(self.frame_botones, text="Reiniciar", command=self.reiniciar_partida)
        boton_reiniciar.pack(side=tk.LEFT, padx=10,pady=10)

        boton_volver = tk.Button(self.frame_botones, text="Volver al Menú Principal", command=self.volver_al_menu_principal)
        boton_volver.pack(side=tk.LEFT, padx=10)

        self.actualizar_contadores()

    def ha_ganado(self):
        return self.liberadas == (self.filas * self.columnas) - self.minas 

    def clic(self, fila, columna):
        if self.tablero[fila][columna] == -1:
            if (fila, columna) not in self.casillas_descubiertas:
                self.vidas -= 1
                self.actualizar_contadores()

                if self.vidas == 0:
                    messagebox.showinfo("¡Boom!", "Perdiste")
                    self.mostrar_todo()
                else:
                    messagebox.showinfo("¡Oh no!", f"Te quedan {self.vidas} vidas")
                    self.botones[fila][columna].config(text=self.icono_bomba, bg="#E82426")
                self.casillas_descubiertas.add((fila, columna))
        else:
            self.descubrir_casilla(fila, columna)
            if self.ha_ganado():
                self.gano()

    def descubrir_casilla(self, fila, columna):
        if (fila, columna) not in self.casillas_descubiertas:
            self.liberadas += 1
            valor = self.tablero[fila][columna]
            self.botones[fila][columna].config(text=str(valor))
            self.casillas_descubiertas.add((fila, columna))
            self.actualizar_puntaje(valor)

            if valor == 0:
                for i in range(fila-1, fila+2):
                    for j in range(columna-1, columna+2):
                        if 0 <= i < self.filas and 0 <= j < self.columnas:
                            self.descubrir_casilla(i, j)

    def mostrar_todo(self):
        for fila in range(self.filas):
            for columna in range(self.columnas):
                valor = self.tablero[fila][columna]
                if valor == -1:
                    self.botones[fila][columna].config(text=self.icono_bomba,bg="#E82426")
                else:
                    self.botones[fila][columna].config(text=str(valor))

    def gano(self):
        nombre_jugador = simpledialog.askstring("¡Felicidades!", "Has ganado. Ingresa tu nombre:")
        if nombre_jugador:
            self.guardar_puntaje(nombre_jugador)
            self.volver_al_menu_principal()
       

    def reiniciar_partida(self):
        self.frame_juego.destroy()
        self.frame_botones.destroy()
        self.__init__(self.master, self.filas, self.columnas, self.minas,self.nivel, self.menu,self.icono_bomba,self.icono_seleccion)

    def volver_al_menu_principal(self):
        self.frame_juego.destroy()
        self.frame_botones.destroy()
        self.menu.mostrar_menu()

    def actualizar_contadores(self):
        self.label_vidas.config(text=f"Vidas: {self.vidas}")
        self.label_puntaje.config(text=f"Puntaje: {self.puntaje}")

    def actualizar_puntaje(self, valor_casilla):
        if valor_casilla != -1:
            self.puntaje = self.obtener_puntaje()
            self.actualizar_contadores()
    
    def obtener_puntaje(self):
        return (self.liberadas * self.nivel) - (50 * (3 - self.vidas))

    def marcar_casilla(self, event, fila, columna):
        if (fila, columna) not in self.casillas_descubiertas:
            if self.botones[fila][columna]["text"] == self.icono_seleccion:
                self.botones[fila][columna].config(text="")
            else:
                self.botones[fila][columna].config(text=self.icono_seleccion) 

    def guardar_puntaje(self, nombre):
        puntaje = self.obtener_puntaje()
        with open("puntajes.txt", "a") as file:
            file.write(f"{nombre},{puntaje}\n")

