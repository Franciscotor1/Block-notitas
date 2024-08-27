from tkinter import Tk, ttk, Frame
from tkinter import Button, Entry, Label, Menu, Scrollbar, Text
from tkinter import messagebox, filedialog, Toplevel, colorchooser
from tkinter import font, BooleanVar

class Ventana(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title('Bloc de Notas')
        # Se eliminó la línea que cargaba el icono
        # self.master.iconbitmap('icono.ico')
        self.master.geometry('700x500+380+20')
        self.master.protocol("WM_DELETE_WINDOW", self.salir)
        self.señal_ajustes = BooleanVar()
        self.info_estado = BooleanVar()
        self.info_estado.set(False)
        self.señal_ajustes.set(True)
        self.clik_aceptar = False
        self.x = 0
        self.y = 0
        self.n = 12
        self.f = 'Arial'
        self.widgets()
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

    def widgets(self):
        menu = Menu(self.master)
        self.master.config(menu=menu)
        archivo = Menu(menu, tearoff=0)
        archivo.add_command(label="Nuevo", command=self.nueva_ventana)
        archivo.add_command(label="Ventana Nueva", command=self.segunda_ventana)
        archivo.add_command(label="Abrir...", command=self.abrir_archivo)
        archivo.add_command(label="Guardar", command=self.guardar_archivo)
        archivo.add_separator()
        archivo.add_command(label="Salir", command=self.master.quit)
        edicion = Menu(menu, tearoff=0)
        edicion.add_command(label="Deshacer", command=lambda: self.texto.edit_undo())
        edicion.add_separator()

        edicion.add_command(label="Cortar", accelerator='Ctrl+X',
                            command=lambda: self.master.focus_get().event_generate("<<Cut>>"))
        edicion.add_command(label="Copiar", accelerator='Ctrl+C',
                            command=lambda: self.master.focus_get().event_generate("<<Copy>>"))
        edicion.add_command(label="Pegar", accelerator='Ctrl+V',
                            command=lambda: self.master.focus_get().event_generate("<<Paste>>"))
        edicion.add_command(label="Eliminar", accelerator='Supr',
                            command=lambda: self.master.focus_get().event_generate("<<Clear>>"))
        formato = Menu(menu, tearoff=0)
        formato.add_checkbutton(label="Ajustes de linea", variable=self.señal_ajustes, command=self.ajustes_de_linea)
        formato.add_command(label="Fuente", command=self.formato_fuente)
        formato.add_command(label="Color de texto", command=self.elegir_color_texto)
        formato.add_command(label="Color de fondo", command=self.elegir_color_fondo)
        ver = Menu(menu, tearoff=0)
        submenu = Menu(menu, tearoff=0)
        submenu.add_command(label="Acercar", command=self.zoom_mas)
        submenu.add_command(label="Alejar", command=self.zoom_menos)
        submenu.add_command(label="Restaurar Zoom", command=lambda: self.texto.config(font=(self.f, 12)))
        ver.add_cascade(label="Zoom", menu=submenu)
        ver.add_checkbutton(label="Barra de estado", variable=self.info_estado, command=self.barra_de_estado)
        ayuda = Menu(menu, tearoff=0)
        ayuda.add_command(label="Ver la ayuda")
        ayuda.add_separator()
        ayuda.add_command(label="Acerca del Bloc de notas", command=self.acerca_de)
        menu.add_cascade(label="Archivo", menu=archivo)
        menu.add_cascade(label="Edicion", menu=edicion)
        menu.add_cascade(label="Formato", menu=formato)
        menu.add_cascade(label="Ver", menu=ver)
        menu.add_cascade(label="Ayuda", menu=ayuda)
        self.texto = Text(self.master, font=('Arial', 12), undo=True, insertbackground='red')
        self.texto.grid(column=0, row=0, sticky='nsew')
        ladox = Scrollbar(self.master, orient='horizontal', command=self.texto.xview)
        ladox.grid(column=0, row=1, sticky='ew')
        ladoy = Scrollbar(self.master, orient='vertical', command=self.texto.yview)
        ladoy.grid(column=1, row=0, sticky='ns')
        self.texto.configure(xscrollcommand=ladox.set, yscrollcommand=ladoy.set)
        self.barra_estado = Label(self.master, font=('Segoe UI Symbol', 10))
        # eventos
        self.master.bind('<Shift-KeyPress-S>', self.salir)

    def ajustes_de_linea(self):
        if self.señal_ajustes.get():
            self.texto.config(wrap='word')
        else:
            self.texto.config(wrap='none')

    def barra_de_estado(self):
        if self.info_estado.get():
            n = len(self.texto.get('1.0', 'end'))

            self.barra_estado.grid(column=0, row=2, sticky='ew')
            self.barra_estado.config(text=f'Numero de letras: {n}')

        x = self.barra_estado.after(10, self.barra_de_estado)

        if not self.info_estado.get():
            self.barra_estado.after_cancel(x)
            self.barra_estado.grid_forget()

    def zoom_mas(self):
        if self.n < 90:
            self.n += 2
            self.texto.config(font=(self.f, self.n))
        else:
            self.n = 12

    def zoom_menos(self):
        if self.n > 6:
            self.n -= 2
            self.texto.config(font=(self.f, self.n))
        else:
            self.n = 12

    def salir(self, *args):
        valor = messagebox.askyesno('Salir', '¿Desea Salir?', parent=self.master)
        if valor:
            self.master.destroy()
            self.master.quit()

    def abrir_archivo(self):
        direccion = filedialog.askopenfilename(initialdir='/',
                                               title='Archivo',
                                               filetype=(('txt files', '*.txt*'), ('All files', '*.*')))
        if direccion != '':
            archivo = open(direccion, 'r')
            contenido = archivo.read()
            self.texto.delete('1.0', 'end')
            self.texto.insert('1.0', contenido)
            self.master.title(direccion)

    def guardar_archivo(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension='.txt')
            archivo = open(filename, 'w')
            archivo.write(self.texto.get('1.0', 'end'))
            archivo.close()

            messagebox.showinfo('Guardar Archivo', 'Archivo guardado en: ' + str(filename))
        except:
            messagebox.showerror('Guardar Archivo', 'Archivo no guardado\n Error')

    def nueva_ventana(self):
        if self.texto.get != '':
            valor = messagebox.askyesno('Bloc de Notas', '¿Desea guardar el archivo?', parent=self.master)
            if valor:
                self.guardar_archivo()
            else:
                self.texto.delete('1.0', 'end')

    def segunda_ventana(self):
        segunda_ventana = Toplevel(self.master)
        segunda_ventana = Ventana(segunda_ventana)

    def acerca_de(self):
        vent_info = Toplevel(self.master)
        vent_info.config(bg='white')
        vent_info.title('')
        vent_info.resizable(0, 0)
        # Se eliminó la línea que cargaba el icono
        # vent_info.iconbitmap('icono.ico')
        vent_info.geometry('350x200+200+200')
        Label(vent_info, bg='white',
              text='Programa realizado en Python \n con la liberia de Tkinter \n\n Autor: Francisco Torres').pack(expand=True)

    def formato_fuente(self):
        self.vent_tipo_fuente = Toplevel(self.master)
        self.vent_tipo_fuente.overrideredirect(1)
        self.vent_tipo_fuente.geometry('390x290+400+200')
        self.vent_tipo_fuente.config(bg='SeaGreen1', relief='raised', bd=3)
        self.vent_tipo_fuente.bind("<B1-Motion>", self.mover)
        self.vent_tipo_fuente.bind("<ButtonPress-1>", self.start)

        fuente = list(font.families())
        tamaño = []
        for i in range(8, 73): tamaño.append(i)

        Label(self.vent_tipo_fuente, text='Fuente:', fg='black', bg='SeaGreen1',
              font=('Segoe UI Symbol', 12)).grid(row=0, column=0, padx=5, ipady=6)

        Label(self.vent_tipo_fuente, text='Tamaño:', fg='black', bg='SeaGreen1',
              font=('Segoe UI Symbol', 12)).grid(row=0, column=1, padx=5, ipady=6)

        self.combobox_fuente = ttk.Combobox(self.vent_tipo_fuente, values=fuente,
                                            justify='center', width='15', font='Arial')
        self.combobox_fuente.grid(row=1, column=0, padx=25, pady=5)  # state="readonly"
        self.combobox_fuente.set(self.f)

        self.combobox_tamaño = ttk.Combobox(self.vent_tipo_fuente, values=tamaño,
                                            justify='center', width='7', font='Arial')
        self.combobox_tamaño.grid(row=1, column=1, pady=5)  # state="readonly"
        self.combobox_tamaño.set(12)

        self.muestra_fuente = Text(self.vent_tipo_fuente, height=5, width=35, state='normal',
                                   font=('Arial', 12), fg='black', bg='white')
        self.muestra_fuente.grid(row=2, columnspan=2, padx=10, pady=10)
        self.muestra_fuente.insert('insert', 'Python 3.9.1\nFuente Arial, tamaño 12')
        self.muestra_fuente.configure(state='disabled')

        Button(self.vent_tipo_fuente, text='Aceptar', relief='flat', fg='black',
               bg='white', font=('Arial', 12), width=9, height=1,
               command=self.aceptar_fuente).grid(row=3, column=0, pady=10)
        Button(self.vent_tipo_fuente, text='Cancelar', relief='flat', fg='black',
               bg='white', font=('Arial', 12), width=9, height=1,
               command=self.vent_tipo_fuente.destroy).grid(row=3, column=1, pady=10)

    def mover(self, event):
        x = (event.x_root - self.x - self.vent_tipo_fuente.winfo_rootx() + self.vent_tipo_fuente.winfo_rootx())
        y = (event.y_root - self.y - self.vent_tipo_fuente.winfo_rooty() + self.vent_tipo_fuente.winfo_rooty())
        nueva_geom = "+%s+%s" % (self.vent_tipo_fuente.winfo_x() + x, self.vent_tipo_fuente.winfo_y() + y)
        self.vent_tipo_fuente.geometry(nueva_geom)

    def start(self, event):
        self.x = event.x
        self.y = event.y

    def aceptar_fuente(self):
        self.clik_aceptar = True
        self.f = self.combobox_fuente.get()
        self.n = int(self.combobox_tamaño.get())
        self.texto.config(font=(self.f, self.n))
        self.muestra_fuente.config(font=(self.f, self.n))
        self.vent_tipo_fuente.destroy()

    def elegir_color_texto(self):
        color = colorchooser.askcolor(title="Elige un color de texto")
        self.texto.config(fg=color[1])

    def elegir_color_fondo(self):
        color = colorchooser.askcolor(title="Elige un color de fondo")
        self.texto.config(bg=color[1])

if __name__ == '__main__':
    root = Tk()
    ventana = Ventana(root)
    ventana.mainloop()
