# employees_dao.py
import os
import sqlite3

# ------------------- CONFIGURAR BASE DE DATOS -------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER = os.path.join(BASE_DIR, "..", "cineplus_db")
DB_FOLDER = os.path.abspath(DB_FOLDER)

# Crear carpeta si no existe
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)

# Ruta completa del archivo
DB_NAME = os.path.join(DB_FOLDER, "cineplus.db")


def conectar():
    """Conecta a SQLite usando ruta absoluta"""
    return sqlite3.connect(DB_NAME)


# ------------------- CREAR TABLAS -------------------

def crear_tablas():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER,
            correo TEXT,
            puesto TEXT,
            turno TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS turnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            inicio TEXT,
            fin TEXT,
            area TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS areas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            descripcion TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            empleado_id INTEGER,
            fecha TEXT,
            FOREIGN KEY (empleado_id) REFERENCES empleados(id)
        )
    """)

    conn.commit()
    conn.close()


# ------------------- TURNOS POR DEFECTO -------------------

def insertar_turnos_por_defecto():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM turnos")
    count = cur.fetchone()[0]

    if count == 0:
        turnos = [
            ("Turno Mañana", "08:00", "14:00", "Proyección"),
            ("Turno Tarde", "14:00", "20:00", "Limpieza"),
            ("Turno Noche", "20:00", "02:00", "Seguridad")
        ]

        cur.executemany("""
            INSERT INTO turnos (nombre, inicio, fin, area)
            VALUES (?, ?, ?, ?)
        """, turnos)

        conn.commit()
        print("✅ Turnos insertados.")
    else:
        print("✔️ Tabla turnos ya tenía datos.")

    conn.close()


# ------------------- CRUD EMPLEADOS -------------------

def agregar_empleado(nombre, edad, correo, puesto, turno):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO empleados (nombre, edad, correo, puesto, turno)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, edad, correo, puesto, turno))
    conn.commit()
    conn.close()


def obtener_empleados():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM empleados")
    rows = cur.fetchall()
    conn.close()

    empleados = []
    for r in rows:
        empleados.append({
            "id": r[0],
            "nombre": r[1],
            "edad": r[2],
            "correo": r[3],
            "puesto": r[4],
            "turno": r[5]
        })
    return empleados


def obtener_empleado_por_id(emp_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM empleados WHERE id = ?", (emp_id,))
    r = cur.fetchone()
    conn.close()

    if not r:
        return None

    return {
        "id": r[0],
        "nombre": r[1],
        "edad": r[2],
        "correo": r[3],
        "puesto": r[4],
        "turno": r[5]
    }


def actualizar_empleado(emp_id, nombre, edad, correo, puesto, turno):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        UPDATE empleados SET
        nombre=?, edad=?, correo=?, puesto=?, turno=?
        WHERE id=?
    """, (nombre, edad, correo, puesto, turno, emp_id))
    conn.commit()
    conn.close()


def eliminar_empleado(emp_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM empleados WHERE id=?", (emp_id,))
    conn.commit()
    conn.close()


# ------------------- CRUD TURNOS -------------------

def obtener_turnos():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM turnos")
    rows = cur.fetchall()
    conn.close()

    turnos = []
    for r in rows:
        turnos.append({
            "id": r[0],
            "nombre": r[1],
            "inicio": r[2],
            "fin": r[3],
            "area": r[4]
        })
    return turnos


def agregar_turno(nombre, inicio, fin, area):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO turnos (nombre, inicio, fin, area)
        VALUES (?, ?, ?, ?)
    """, (nombre, inicio, fin, area))
    conn.commit()
    conn.close()


def actualizar_turno(turno_id, nombre, inicio, fin, area):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        UPDATE turnos SET nombre=?, inicio=?, fin=?, area=?
        WHERE id=?
    """, (nombre, inicio, fin, area, turno_id))
    conn.commit()
    conn.close()


def eliminar_turno(turno_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM turnos WHERE id=?", (turno_id,))
    conn.commit()
    conn.close()


# ------------------- AUTO EJECUCIÓN -------------------

if __name__ == "__main__":
    print("🔧 Inicializando base de datos CinePlus...")
    crear_tablas()
    insertar_turnos_por_defecto()
    print("📦 Listo.")
