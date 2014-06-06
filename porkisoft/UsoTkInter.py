from Tkinter import *

ventana = Tk()
ventana.geometry('200x200+20+20')


barraMenu = Menu(ventana)
mnuArchivo = Menu(barraMenu)
mnuArchivo.add_command(label ='Abrir')
barraMenu.add_cascade(label='Archivo',menu = mnuArchivo)
ventana.config(menu = barraMenu)

ventana.mainloop()


