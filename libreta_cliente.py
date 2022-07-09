from graphlib import TopologicalSorter
import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from sqlite3 import *
import emoji

root = Tk()
root.title("HOLA MUNDO: CRM")

conn = sqlite3.connect("crm.db")
c = conn.cursor()
c.execute("""
    CREATE TABLE if not exists cliente(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,
        Telefono TEXT NOT NULL,
        Empresa TEXT NOT NULL
    );
    """)

conn.commit()

def insertar(cliente):

    c.execute("""INSERT INTO cliente(Nombre,Telefono,Empresa) 
                    VALUES(?,?,?)""",(cliente["nombre"],cliente["telefono"],cliente["empresa"]))
    conn.commit()
    messagebox.showinfo("",emoji.emojize('Se ha añadido con éxito el registro :check_mark:'))
    render_db()

def eliminar_cl():
    
    id = tree.selection()[0]
    cliente = c.execute("SELECT * FROM cliente WHERE id=?",(id,)).fetchone()
    respuesta = messagebox.askquestion("Popup","Está seguro que desea eliminar a "+cliente[1] + "?")
    if respuesta == "yes":
        c.execute("DELETE FROM cliente WHERE id=?",(id,))
        messagebox.showinfo("",emoji.emojize("Se ha borrado con éxito el registro :check_mark:"))
        conn.commit()
        render_db()
    else:
        pass
    

def nuevo_cl():

    def guarda_cl():
        
        if not campo1.get():
            messagebox.showwarning("Error","El campo nombre es obligatorio")
            return
        if not campo2.get():
            messagebox.showwarning("Error","El campo telefono es obligatorio")
            return

        if not campo3.get():
            messagebox.showwarning("Error","El campo empresa es obligarorio")
            return

        cliente = {
            "nombre": campo1.get(),
            "telefono": campo2.get(),
            "empresa": campo3.get()
        }

        insertar(cliente)
        top.destroy()    

    top = Toplevel()
    top.title("Nuevo cliente")
    l = Label(top, text="Nombre:")
    l2 = Label(top, text="Telefono:")
    l3 = Label(top, text="Empresa:")
    l.grid(row=0, column=0)
    l2.grid(row=1, column=0)
    l3.grid(row=2, column=0)

    campo1 = Entry(top, width=40)
    campo2 = Entry(top, width=40)
    campo3 = Entry(top, width=40)
    campo1.grid(row=0, column=1)
    campo2.grid(row=1, column=1)
    campo3.grid(row=2, column=1)

    btn_guardar = Button(top, text="Guardar", command=guarda_cl)
    btn_guardar.grid(row=3, column=0)

    top.mainloop()

btn_nuevo = Button(root, text="Nuevo cliente", command=nuevo_cl)
btn_nuevo.grid(column=0, row=0)
btn_eliminar = Button(root, text="Eliminar cliente", command=eliminar_cl)
btn_eliminar.grid(column=1, row=0)

tree = ttk.Treeview(root)
tree["columns"]= ("Nombre","Telefono","Empresa")

tree.column('#0', width=0, stretch=NO)
tree.column('Nombre')
tree.column('Telefono')
tree.column('Empresa')

tree.heading("Nombre",text="Nombre")
tree.heading("Telefono",text="Telefono")
tree.heading("Empresa",text="Empresa")

tree.grid(column=0, row=1, columnspan=2)

"""tree.insert('',END,'primera_f',values=('Jose','999999','JOSE SA'), text="ID_1")
tree.insert('primera_f',END,'segunda_f',values=('Juan','999999','JOSE SA'),text='ID_2')
tree.insert('',END,'tercera_f',values=('Andrea','999999','ANDREA SA'),text='ID_3')
tree.insert('tercera_f',END,'cuarta_f',values=('Maria','999999','ANDREA SA'),text='ID_4')"""

def render_db():

    rows = c.execute("SELECT * FROM cliente").fetchall()
    tree.delete(*tree.get_children())
    print(rows)
    for row in rows:
        tree.insert('',END, row[0], values=(row[1], row[2], row[3]))

render_db()
root.mainloop()