import tkinter as tk
from tkinter import ttk, messagebox
from dao import employees_dao as dao



# ======================================================
#                  GUI PRINCIPAL CINEPLUS
# ======================================================
class CinePlusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 CinePlus — Gestión de Empleados")
        self.root.geometry("1000x650")
        self.root.configure(bg="#e9f0ff")  # azul clarito profesional

        # ---------- VARIABLES ----------
        self.var_id = None
        self.var_nombre = tk.StringVar()
        self.var_edad = tk.StringVar()
        self.var_correo = tk.StringVar()
        self.var_puesto = tk.StringVar()
        self.var_turno = tk.StringVar()

        # =====================================================
        # LOGO SUPERIOR
        # =====================================================
        header = tk.Frame(self.root, bg="#0b3d91", height=80)
        header.pack(fill="x")

        logo = tk.Label(
            header,
            text=" 🎬 🍿 🎥   C I N E P L U S ",
            bg="#0b3d91",
            fg="white",
            font=("Segoe UI", 26, "bold")
        )
        logo.pack(pady=10)

        # =====================================================
        # FORMULARIO IZQUIERDO
        # =====================================================
        form_frame = tk.LabelFrame(
            self.root,
            text="Registro de Empleados",
            bg="#e9f0ff",
            font=("Segoe UI", 12, "bold"),
            padx=10, pady=10
        )
        form_frame.place(x=20, y=100, width=450, height=260)

        # Etiquetas y campos
        labels = ["Nombre:", "Edad:", "Correo:", "Puesto:", "Turno:"]
        vars_ = [self.var_nombre, self.var_edad, self.var_correo,
                 self.var_puesto, self.var_turno]

        for i, (lab, var) in enumerate(zip(labels, vars_)):
            tk.Label(form_frame, text=lab, bg="#e9f0ff",
                     font=("Segoe UI", 11)).grid(row=i, column=0, sticky="w")
            tk.Entry(form_frame, textvariable=var,
                     width=30).grid(row=i, column=1)

        # =====================================================
        # BOTONES CRUD
        # =====================================================
        btn_frame = tk.Frame(self.root, bg="#e9f0ff")
        btn_frame.place(x=20, y=360, width=450, height=60)

        # Estilos
        def btn(style_color):
            return {
                "bg": style_color,
                "fg": "white",
                "font": ("Segoe UI", 11, "bold"),
                "width": 10,
                "height": 1,
                "bd": 0,
                "activebackground": style_color
            }

        tk.Button(btn_frame, text="✔ Agregar", command=self.agregar,
                  **btn("#1e88e5")).grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="✏️ Editar", command=self.editar,
                  **btn("#1565c0")).grid(row=0, column=1, padx=5)

        tk.Button(btn_frame, text="💾 Guardar", command=self.guardar,
                  **btn("#0d47a1")).grid(row=0, column=2, padx=5)

        tk.Button(btn_frame, text="🗑️ Eliminar", command=self.eliminar,
                  **btn("#c62828")).grid(row=0, column=3, padx=5)

        # =====================================================
        # TABLA DERECHA
        # =====================================================
        table_frame = tk.LabelFrame(
            self.root,
            text="Empleados registrados",
            bg="#e9f0ff",
            font=("Segoe UI", 12, "bold"),
            padx=5, pady=5
        )
        table_frame.place(x=500, y=100, width=480, height=380)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "nombre", "puesto", "turno"),
            show="headings",
            height=12
        )
        self.tree.pack(fill="both", expand=True)

        self.tree.heading("id", text="Id")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("puesto", text="Puesto")
        self.tree.heading("turno", text="Turno")

        # Ancho columnas
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=150)
        self.tree.column("puesto", width=120)
        self.tree.column("turno", width=120)

        # =====================================================
        # LISTA DE TURNOS
        # =====================================================
        turnos_frame = tk.LabelFrame(
            self.root,
            text="Turnos disponibles",
            bg="#e9f0ff",
            font=("Segoe UI", 12, "bold")
        )
        turnos_frame.place(x=20, y=440, width=450, height=170)

        self.list_turnos = tk.Listbox(turnos_frame, width=55, height=6)
        self.list_turnos.pack(padx=10, pady=10)

        # Cargar datos iniciales
        self.cargar_empleados()
        self.cargar_turnos()

    # =====================================================
    # CRUD: AGREGAR
    # =====================================================
    def agregar(self):
        self.var_id = None
        self.var_nombre.set("")
        self.var_edad.set("")
        self.var_correo.set("")
        self.var_puesto.set("")
        self.var_turno.set("")
        messagebox.showinfo("Agregar", "Modo agregar activado.")

    # =====================================================
    # EDITAR
    # =====================================================
    def editar(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Editar", "Selecciona un empleado.")
            return

        emp_id = self.tree.item(selected[0])["values"][0]
        emp = dao.obtener_empleado_por_id(emp_id)

        self.var_id = emp_id
        self.var_nombre.set(emp["nombre"])
        self.var_edad.set(emp["edad"])
        self.var_correo.set(emp["correo"])
        self.var_puesto.set(emp["puesto"])
        self.var_turno.set(emp["turno"])

        messagebox.showinfo("Editar", "Modo edición activado.")

    # =====================================================
    # GUARDAR (Agregar o Actualizar)
    # =====================================================
    def guardar(self):
        nombre = self.var_nombre.get()

        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio.")
            return

        if self.var_id is None:
            # Agregar nuevo empleado
            dao.agregar_empleado(
                nombre,
                self.var_edad.get(),
                self.var_correo.get(),
                self.var_puesto.get(),
                self.var_turno.get()
            )
            messagebox.showinfo("Guardar", "Empleado agregado.")
        else:
            # Actualizar empleado
            dao.actualizar_empleado(
                self.var_id,
                nombre,
                self.var_edad.get(),
                self.var_correo.get(),
                self.var_puesto.get(),
                self.var_turno.get()
            )
            messagebox.showinfo("Guardar", "Empleado actualizado.")

        self.cargar_empleados()

    # =====================================================
    # ELIMINAR
    # =====================================================
    def eliminar(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Eliminar", "Selecciona un empleado.")
            return

        emp_id = self.tree.item(selected[0])["values"][0]
        dao.eliminar_empleado(emp_id)

        messagebox.showinfo("Eliminar", "Empleado eliminado.")
        self.cargar_empleados()

    # =====================================================
    # CARGAR EMPLEADOS
    # =====================================================
    def cargar_empleados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        empleados = dao.obtener_empleados()

        for emp in empleados:
            self.tree.insert(
                "", "end",
                values=(emp["id"], emp["nombre"], emp["puesto"], emp["turno"])
            )

    # =====================================================
    # CARGAR TURNOS
    # =====================================================
    def cargar_turnos(self):
        self.list_turnos.delete(0, tk.END)

        turnos = dao.obtener_turnos()
        for t in turnos:
            texto = f"{t['nombre']} {t['inicio']}-{t['fin']} ({t['area']})"
            self.list_turnos.insert(tk.END, texto)


# =====================================================
# EJECUCIÓN PRINCIPAL
# =====================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = CinePlusGUI(root)
    root.mainloop()
