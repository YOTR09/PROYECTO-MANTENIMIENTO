import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

# ==========================================
# 1. CONFIGURACIÓN Y UTILIDADES
# ==========================================
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="dev_user",          # <-- Tu usuario
        password="123456",          # <-- Tu contraseña
        database="db_transporte_mantenimiento"  # <-- Tu base de datos
    )

# Diccionario para mapear "Nombre del Socio" -> "ID del Socio"
diccionario_socios = {}

def cargar_socios():
    """Carga los socios de la base de datos para llenar el Combobox"""
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_socio, nombre_completo FROM socio")
        socios = cursor.fetchall()
        
        nombres_para_combobox = []
        diccionario_socios.clear()
        
        for id_socio, nombre in socios:
            nombres_para_combobox.append(nombre)
            diccionario_socios[nombre] = id_socio # Guardamos la relación
            
        combo_socios['values'] = nombres_para_combobox
        conexion.close()
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"No se pudieron cargar los socios: {error}")

# ==========================================
# 2. FUNCIONES CRUD
# ==========================================
def insertar():
    nombre_seleccionado = socio_var.get()
    
    if nombre_seleccionado not in diccionario_socios:
        messagebox.showerror("Error", "Debe seleccionar un socio válido")
        return
        
    id_socio_real = diccionario_socios[nombre_seleccionado]
    
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        sql = "INSERT INTO vehiculo (id_socio, placa, marca_modelo, status) VALUES (%s, %s, %s, %s)"
        valores = (id_socio_real, placa_var.get(), marca_var.get(), status_var.get())
        
        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()
        
        limpiar_campos()
        mostrar_datos()
        messagebox.showinfo("Éxito", "Vehículo registrado")
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Fallo al registrar: {error}")

def mostrar_datos():
    for elemento in tree.get_children():
        tree.delete(elemento)
        
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        # Hacemos un JOIN para mostrar el nombre del socio en lugar de su ID en la tabla
        sql = """
            SELECT v.id_vehiculo, s.nombre_completo, v.placa, v.marca_modelo, v.status 
            FROM vehiculo v
            INNER JOIN socio s ON v.id_socio = s.id_socio
        """
        cursor.execute(sql)
        datos = cursor.fetchall()
        
        for fila in datos:
            tree.insert("", tk.END, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4]))
        conexion.close()
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Fallo al consultar: {error}")

def seleccionar_registro(event):
    item = tree.focus()
    if item:
        valores = tree.item(item, "values")
        id_registro = tree.item(item, "text")
        
        id_var.set(id_registro)
        socio_var.set(valores[0]) # Nombre del socio
        placa_var.set(valores[1])
        marca_var.set(valores[2])
        status_var.set(valores[3])

def actualizar():
    if id_var.get() == "":
        messagebox.showerror("Error", "Seleccione un vehículo")
        return
        
    nombre_seleccionado = socio_var.get()
    id_socio_real = diccionario_socios.get(nombre_seleccionado)
    
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        sql = """
            UPDATE vehiculo 
            SET id_socio=%s, placa=%s, marca_modelo=%s, status=%s 
            WHERE id_vehiculo=%s
        """
        valores = (id_socio_real, placa_var.get(), marca_var.get(), status_var.get(), id_var.get())
        
        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()
        
        limpiar_campos()
        mostrar_datos()
        messagebox.showinfo("Éxito", "Vehículo actualizado")
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Fallo al actualizar: {error}")

def eliminar():
    if id_var.get() == "": return
    if messagebox.askyesno("Confirmar", "¿Eliminar este vehículo?"):
        try:
            conexion = conectar_db()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM vehiculo WHERE id_vehiculo=%s", (id_var.get(),))
            conexion.commit()
            conexion.close()
            limpiar_campos()
            mostrar_datos()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Fallo al eliminar: {error}")

def limpiar_campos():
    id_var.set("")
    socio_var.set("")
    placa_var.set("")
    marca_var.set("")
    status_var.set("")

# ==========================================
# 3. INTERFAZ GRÁFICA
# ==========================================
ventana = tk.Tk()
ventana.title("Gestión de Vehículos")
ventana.geometry("750x550")

id_var = tk.StringVar()
socio_var = tk.StringVar()
placa_var = tk.StringVar()
marca_var = tk.StringVar()
status_var = tk.StringVar()

frame_form = tk.LabelFrame(ventana, text="Datos del Vehículo", padx=10, pady=10)
frame_form.pack(fill="x", padx=10, pady=10)

# Combobox para Socio
tk.Label(frame_form, text="Propietario (Socio):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
combo_socios = ttk.Combobox(frame_form, textvariable=socio_var, state="readonly", width=25)
combo_socios.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Placa:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
tk.Entry(frame_form, textvariable=placa_var).grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_form, text="Marca/Modelo:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
tk.Entry(frame_form, textvariable=marca_var, width=28).grid(row=1, column=1, padx=5, pady=5)

# Combobox para Status (Opcional, asumiendo que hay estados fijos)
tk.Label(frame_form, text="Status:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
combo_status = ttk.Combobox(frame_form, textvariable=status_var, state="readonly", values=["Activo", "En Taller", "Inactivo"])
combo_status.grid(row=1, column=3, padx=5, pady=5)

frame_botones = tk.Frame(ventana)
frame_botones.pack(fill="x", padx=10, pady=5)

tk.Button(frame_botones, text="Guardar", command=insertar, bg="lightgreen").pack(side="left", padx=5)
tk.Button(frame_botones, text="Actualizar", command=actualizar, bg="pink").pack(side="left", padx=5)
tk.Button(frame_botones, text="Eliminar", command=eliminar, bg="lightgreen").pack(side="left", padx=5)
tk.Button(frame_botones, text="Limpiar", command=limpiar_campos).pack(side="left", padx=5)
tk.Button(frame_botones, text="Salidas", bg="lightblue").pack(side="left", padx=5)
tk.Button(frame_botones, text="Buscar", bg="lightblue").pack(side="left", padx=5)
tk.Button(frame_botones, text="Salir", command=insertar, bg="lightblue").pack(side="left", padx=5)

columnas = ("Socio", "Placa", "Marca", "Status")
tree = ttk.Treeview(ventana, columns=columnas)
tree.pack(fill="both", expand=True, padx=10, pady=10)

tree.heading("#0", text="ID")
tree.heading("Socio", text="Propietario")
tree.heading("Placa", text="Placa")
tree.heading("Marca", text="Marca/Modelo")
tree.heading("Status", text="Status")

tree.column("#0", width=40)
tree.column("Socio", width=150)
tree.column("Placa", width=80)
tree.column("Marca", width=150)
tree.column("Status", width=80)

tree.bind("<ButtonRelease-1>", seleccionar_registro)

# Inicializar
cargar_socios()
mostrar_datos()

ventana.mainloop()