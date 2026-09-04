import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector # IMPORTANTE: Cambiamos sqlite3 por mysql.connector

# ==========================================
# 1. CONFIGURACIÓN DE LA BASE DE DATOS
# ==========================================
def conectar_db():
    # Reemplaza estos valores con los de tu MariaDB local
    conexion = mysql.connector.connect(
        host="localhost",
        user="dev_user",          # <-- TU USUARIO DE MARIADB (ej: root)
        password="123456",          # <-- TU CONTRASEÑA DE MARIADB
        database="db_transporte_mantenimiento"  # <-- EL NOMBRE DE TU BASE DE DATOS
    )
    # Ya no creamos la tabla por código porque mencionas que ya existe
    return conexion

# ==========================================
# 2. FUNCIONES CRUD
# ==========================================
def insertar():
    if len(cedula_var.get()) == 0 or len(nombre_var.get()) == 0:
        messagebox.showerror("Error", "Cédula y Nombre son obligatorios")
        return
    
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        # En MariaDB usamos %s en lugar de ?
        sql = "INSERT INTO socio (cedula, nombre_completo, telefono) VALUES (%s, %s, %s)"
        valores = (cedula_var.get(), nombre_var.get(), telefono_var.get())
        
        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()
        
        limpiar_campos()
        mostrar_datos()
        messagebox.showinfo("Éxito", "Socio registrado correctamente")
    except mysql.connector.Error as error:
        messagebox.showerror("Error de Base de Datos", f"No se pudo insertar: {error}")

def mostrar_datos():
    # Limpiamos la tabla (Treeview)
    registros = tree.get_children()
    for elemento in registros:
        tree.delete(elemento)
        
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_socio, cedula, nombre_completo, telefono FROM socio")
        datos = cursor.fetchall()
        
        # Insertamos los datos en el Treeview
        for fila in datos:
            tree.insert("", tk.END, text=fila[0], values=(fila[1], fila[2], fila[3]))
        conexion.close()
    except mysql.connector.Error as error:
        messagebox.showerror("Error de Base de Datos", f"No se pudo consultar: {error}")

def seleccionar_registro(event):
    item = tree.focus()
    if item:
        valores = tree.item(item, "values")
        id_registro = tree.item(item, "text")
        
        # Llenamos los campos con los datos seleccionados
        id_var.set(id_registro)
        cedula_var.set(valores[0])
        nombre_var.set(valores[1])
        telefono_var.set(valores[2])

def actualizar():
    if id_var.get() == "":
        messagebox.showerror("Error", "Seleccione un socio de la lista para actualizar")
        return
        
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        # En MariaDB usamos %s
        sql = """
            UPDATE socio 
            SET cedula=%s, nombre_completo=%s, telefono=%s 
            WHERE id_socio=%s
        """
        valores = (cedula_var.get(), nombre_var.get(), telefono_var.get(), id_var.get())
        
        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()
        
        limpiar_campos()
        mostrar_datos()
        messagebox.showinfo("Éxito", "Datos del socio actualizados")
    except mysql.connector.Error as error:
        messagebox.showerror("Error de Base de Datos", f"No se pudo actualizar: {error}")

def eliminar():
    if id_var.get() == "":
        messagebox.showerror("Error", "Seleccione un socio para eliminar")
        return
        
    respuesta = messagebox.askquestion("Confirmar", "¿Seguro que desea eliminar este socio?")
    if respuesta == "yes":
        try:
            conexion = conectar_db()
            cursor = conexion.cursor()
            # En MariaDB usamos %s
            sql = "DELETE FROM socio WHERE id_socio=%s"
            
            cursor.execute(sql, (id_var.get(),))
            conexion.commit()
            conexion.close()
            
            limpiar_campos()
            mostrar_datos()
            messagebox.showinfo("Éxito", "Socio eliminado")
        except mysql.connector.Error as error:
             messagebox.showerror("Error de Base de Datos", f"No se pudo eliminar: {error}")

def limpiar_campos():
    id_var.set("")
    cedula_var.set("")
    nombre_var.set("")
    telefono_var.set("")

# ==========================================
# 3. INTERFAZ GRÁFICA (TKINTER)
# ==========================================
# (El código de Tkinter es exactamente el mismo de antes)
ventana = tk.Tk()
ventana.title("Gestión de Socios (MariaDB)")
ventana.geometry("700x500")

id_var = tk.StringVar()
cedula_var = tk.StringVar()
nombre_var = tk.StringVar()
telefono_var = tk.StringVar()

frame_form = tk.LabelFrame(ventana, text="Datos del Socio", padx=10, pady=10)
frame_form.pack(fill="x", padx=10, pady=10)

tk.Label(frame_form, text="Cédula:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
tk.Entry(frame_form, textvariable=cedula_var).grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Nombre Completo:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
tk.Entry(frame_form, textvariable=nombre_var, width=30).grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_form, text="Teléfono:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
tk.Entry(frame_form, textvariable=telefono_var).grid(row=1, column=1, padx=5, pady=5)

frame_botones = tk.Frame(ventana)
frame_botones.pack(fill="x", padx=10, pady=5)

tk.Button(frame_botones, text="Guardar", command=insertar, bg="lightgreen").pack(side="left", padx=5)
tk.Button(frame_botones, text="Actualizar", command=actualizar, bg="lightblue").pack(side="left", padx=5)
tk.Button(frame_botones, text="Eliminar", command=eliminar, bg="salmon").pack(side="left", padx=5)
tk.Button(frame_botones, text="Limpiar", command=limpiar_campos).pack(side="left", padx=5)

columnas = ("Cédula", "Nombre", "Teléfono")
tree = ttk.Treeview(ventana, columns=columnas)
tree.pack(fill="both", expand=True, padx=10, pady=10)

tree.heading("#0", text="ID")
tree.heading("Cédula", text="Cédula")
tree.heading("Nombre", text="Nombre Completo")
tree.heading("Teléfono", text="Teléfono")

tree.column("#0", width=50)
tree.column("Cédula", width=100)
tree.column("Nombre", width=200)
tree.column("Teléfono", width=100)

tree.bind("<ButtonRelease-1>", seleccionar_registro)

# Inicializar
try:
    mostrar_datos()
except Exception as e:
    messagebox.showerror("Error Crítico", f"No se pudo conectar al iniciar: {e}\n\nRevisa tus credenciales y si MariaDB está encendido.")

ventana.mainloop()