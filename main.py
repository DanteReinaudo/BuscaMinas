import tkinter as tk
from classes.menu import MenuPrincipal
    
if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipal(root)
    photo = tk.PhotoImage(file = 'logo.png')
    root.wm_iconphoto(False, photo)
    root.mainloop()
