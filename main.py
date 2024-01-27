import tkinter as tk
from tkinter import messagebox, simpledialog
from menu import MenuPrincipal
from buscaminas import Buscaminas
    
if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipal(root)
    root.mainloop()
