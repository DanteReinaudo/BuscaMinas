import tkinter as tk
import random

ANCHO, ALTO = 300, 600
FILAS, COLUMNAS = 20, 10
TAMANO_CELDA = ALTO // FILAS
COLORES = ['cyan', 'blue', 'orange', 'yellow', 'green', 'purple', 'red']
FORMAS = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [1]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1]],
    [[1, 1], [0, 1, 1]],
]

class Tetris:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Tetris")

        self.canvas = tk.Canvas(self.ventana, width=ANCHO, height=ALTO, bg='black')
        self.canvas.pack()

        self.tablero = [[0] * COLUMNAS for _ in range(FILAS)]
        self.pieza_actual = None
        self.generar_pieza()

        self.ventana.bind('<Left>', self.mover_izquierda)
        self.ventana.bind('<Right>', self.mover_derecha)
        self.ventana.bind('<Down>', self.mover_abajo)
        self.ventana.bind('<Up>', self.rotar_pieza)

        self.bucle_principal()

    def generar_pieza(self):
        forma = random.choice(FORMAS)
        color = random.choice(COLORES)
        self.pieza_actual = {
            'forma': forma,
            'color': color,
            'fila': 0,
            'columna': COLUMNAS // 2 - len(forma[0]) // 2,
        }
        self.dibujar_pieza()

    def dibujar_pieza(self):
        self.canvas.delete('pieza')
        for i, fila in enumerate(self.pieza_actual['forma']):
            for j, celda in enumerate(fila):
                if celda:
                    x = (self.pieza_actual['columna'] + j) * TAMANO_CELDA
                    y = (self.pieza_actual['fila'] + i) * TAMANO_CELDA
                    self.canvas.create_rectangle(x, y, x + TAMANO_CELDA, y + TAMANO_CELDA, fill=self.pieza_actual['color'], tags='pieza')

    def mover_izquierda(self, _):
        self.pieza_actual['columna'] -= 1
        if self.colision():
            self.pieza_actual['columna'] += 1

        self.dibujar_pieza()

    def mover_derecha(self, _):
        self.pieza_actual['columna'] += 1
        if self.colision():
            self.pieza_actual['columna'] -= 1

        self.dibujar_pieza()

    def mover_abajo(self, _):
        self.pieza_actual['fila'] += 1
        if self.colision():
            self.pieza_actual['fila'] -= 1
            self.fijar_pieza()

        self.dibujar_pieza()

    def rotar_pieza(self, _):
        forma_original = self.pieza_actual['forma']
        self.pieza_actual['forma'] = list(zip(*reversed(self.pieza_actual['forma'])))
        if self.colision():
            self.pieza_actual['forma'] = forma_original

        self.dibujar_pieza()

    def colision(self):
        for i, fila in enumerate(self.pieza_actual['forma']):
            for j, celda in enumerate(fila):
                if celda:
                    fila_tablero = self.pieza_actual['fila'] + i
                    columna_tablero = self.pieza_actual['columna'] + j

                    if (
                        fila_tablero < 0 or
                        fila_tablero >= FILAS or
                        columna_tablero < 0 or
                        columna_tablero >= COLUMNAS or
                        self.tablero[fila_tablero][columna_tablero]
                    ):
                        return True
        return False

    def fijar_pieza(self):
        for i, fila in enumerate(self.pieza_actual['forma']):
            for j, celda in enumerate(fila):
                if celda:
                    fila_tablero = self.pieza_actual['fila'] + i
                    columna_tablero = self.pieza_actual['columna'] + j
                    self.tablero[fila_tablero][columna_tablero] = 1

        self.eliminar_filas_completas()
        self.generar_pieza()

    def eliminar_filas_completas(self):
        filas_completas = [i for i, fila in enumerate(self.tablero) if all(celda == 1 for celda in fila)]
        for fila_completa in reversed(filas_completas):
            del self.tablero[fila_completa]
            self.tablero.insert(0, [0] * COLUMNAS)

    def bucle_principal(self):
        self.mover_abajo(None)
        self.ventana.after(1000, self.bucle_principal)

if __name__ == "__main__":
    tetris = Tetris()
    tetris.ventana.mainloop()
