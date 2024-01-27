import tkinter as tk
from tkinter import messagebox
from classes.buscaminas import Buscaminas

def configurar_juego(dificultad):
    if dificultad == "Fácil":
        return 8, 8, 10, 5
    elif dificultad == "Media":
        return 12, 12, 20, 10
    elif dificultad == "Difícil":
        return 16, 16, 40, 15
    else:
        raise ValueError("Dificultad no válida")

class MenuPrincipal(tk.Frame):
    def __init__(self, master, icono_bomba = "※",icono_seleccion = "✖︎"):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.title("Buscaminas")
        self.master.geometry("800x600")
        self.icono_bomba = icono_bomba
        self.icono_seleccion = icono_seleccion

        self.mostrar_menu()

    def mostrar_menu(self):
        self.frame_menu = tk.Frame(self.master)
        self.frame_menu.pack()
        titulo_label = tk.Label(self.frame_menu, text="Buscaminas", font=("Helvetica", 20))
        titulo_label.pack(pady=50)

        opciones = ["Jugar", "Ver Puntajes", "Instrucciones", "Configuración", "Salir"]
        for opcion in opciones:
            boton = tk.Button(self.frame_menu, text=opcion, width=15, height=2, command=lambda o=opcion: self.ir_a_opcion(o))
            boton.pack(pady=10)
            boton.config(relief=tk.RAISED)

    def ir_a_opcion(self, opcion):
        if opcion == "Jugar":
            self.mostrar_opciones_juego()
        elif opcion == "Ver Puntajes":
            self.mostrar_puntajes()
        elif opcion == "Instrucciones":
            self.mostrar_instrucciones()
        elif opcion == "Configuración":
            self.mostrar_configuracion()
        elif opcion == "Salir":
            self.salir()

    def mostrar_opciones_juego(self):
        self.frame_menu.destroy()
        self.juego_frame = tk.Frame(self.master)
        self.juego_frame.pack()
        titulo_label = tk.Label(self.juego_frame, text="Buscaminas", font=("Helvetica", 20))
        titulo_label.pack(pady=50)
        opciones_juego = ["Fácil", "Media", "Difícil"]
        for opcion in opciones_juego:
            boton = tk.Button(self.juego_frame, text=opcion, width=15, height=2, command=lambda o=opcion: self.iniciar_juego(o))
            boton.pack(pady=10)
            boton.config(relief=tk.RAISED)

        boton_volver = tk.Button(self.juego_frame, text="Volver", width=15, height=2, command=self.volver_al_menu_principal)
        boton_volver.pack(pady=10)
        boton_volver.config(relief=tk.RAISED)

    def iniciar_juego(self, dificultad):
        self.juego_frame.destroy()
        filas, columnas, minas,nivel = configurar_juego(dificultad)
        Buscaminas(self.master, filas, columnas, minas,nivel, self,self.icono_bomba,self.icono_seleccion)

    def mostrar_puntajes(self):
        puntajes_window = tk.Toplevel(self.master)
        puntajes_window.title("Tabla de Puntajes")
        puntajes_window.geometry("400x300")
        puntajes_window.protocol("WM_DELETE_WINDOW", puntajes_window.destroy)  # Cerrar solo la toplevel, no la aplicación principal

        label_titulo = tk.Label(puntajes_window, text="Top Scores", font=("Helvetica", 12))
        label_titulo.pack(pady=20)

        try:
            with open("puntajes.txt", "r") as file:
                puntajes = [line.strip().split(",") for line in file.readlines()]
                puntajes.sort(key=lambda x: int(x[1]), reverse=True)  # Ordenar por puntaje descendente

                for i, (nombre, score) in enumerate(puntajes[:10], start=1):
                    label_puntaje = tk.Label(puntajes_window, text=f"{i}. {nombre}: {score}")
                    label_puntaje.pack()
        except FileNotFoundError:
            messagebox.showinfo("Error", "No se encontró el archivo de puntajes.")

    def mostrar_instrucciones(self):
        instrucciones_texto = (
            "Instrucciones del Juego:\n\n"
            "1. El objetivo del juego es descubrir todas las casillas sin bombas.\n"
            "2. Al hacer clic izquierdo en una casilla, revelas su contenido.\n"
            "3. Si revelas una bomba, pierdes una vida. Pierdes el juego si te quedas sin vidas.\n"
            "4. Si revelas una casilla sin bomba, aparecerá un número que indica cuántas bombas hay alrededor.\n"
            "5. Puedes marcar casillas sospechosas con clic derecho.\n"
            "6. El juego termina cuando todas las casillas sin bombas han sido reveladas o pierdes todas las vidas.\n\n"
            "¡Buena suerte!"
        )

        messagebox.showinfo("Instrucciones", instrucciones_texto)

    def mostrar_configuracion(self):
        self.frame_menu.destroy()
        self.juego_frame = tk.Frame(self.master)
        self.juego_frame.pack()
        titulo_label = tk.Label(self.juego_frame, text="Configuración", font=("Helvetica", 20))
        titulo_label.pack(pady=50)
        # Frame para la selección de icono de bomba
        frame_bomba = tk.LabelFrame(self.juego_frame, text="Seleccionar icono de la bomba:")
        frame_bomba.pack(pady=10)

        # Botones de opciones de icono de bomba
        for opcion in ["※", "☢︎", "☠︎","⊗︎"]:
            boton_opcion = tk.Button(frame_bomba, text=opcion, width=4, height=2,
                                     command=lambda o=opcion: self.seleccionar_icono_bomba(o))
            boton_opcion.pack(side=tk.LEFT, padx=5)

        # Frame para la selección de icono de sospecha
        frame_sospecha = tk.LabelFrame(self.juego_frame, text="Seleccionar icono de la sospecha:")
        frame_sospecha.pack(pady=10)

        # Botones de opciones de icono de sospecha
        for opcion in ["✖︎", "♣︎", "❀︎","♛︎"]:
            boton_opcion = tk.Button(frame_sospecha, text=opcion, width=4, height=2,
                                     command=lambda o=opcion: self.seleccionar_icono_sospecha(o))
            boton_opcion.pack(side=tk.LEFT, padx=5)

        boton_volver = tk.Button(self.juego_frame, text="Volver", width=15, height=2,
                                 command=self.volver_al_menu_principal)
        boton_volver.pack(pady=10)
        boton_volver.config(relief=tk.RAISED)

    def seleccionar_icono_bomba(self,bomba):
        self.icono_bomba = bomba
        messagebox.showinfo("Configuración", f"Icono {bomba} establecido")

    def seleccionar_icono_sospecha(self,seleccion):
        self.icono_seleccion = seleccion
        messagebox.showinfo("Configuración", f"Icono {seleccion} establecido")
    

    def volver_al_menu_principal(self):
        self.juego_frame.destroy()
        self.mostrar_menu()

    def salir(self):
        self.master.destroy()