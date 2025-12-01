import sqlite3
from datetime import time

# Conexión a la base de datos
conn = sqlite3.connect("cineplus.db")
cursor = conn.cursor()

# ----------------- Crear tablas -----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS turnos (
    id_turno INTEGER PRIMARY KEY,
    hora_inicio TEXT,
    hora_fin TEXT,
    area TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS empleados (
    id_empleado INTEGER PRIMARY KEY,
    nombre TEXT,
    edad INTEGER,
    correo TEXT,
    puesto TEXT,
    id_turno INTEGER,
    FOREIGN KEY (id_turno) REFERENCES turnos(id_turno)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tareas (
    id_tarea INTEGER PRIMARY KEY,
    descripcion TEXT,
    area TEXT,
    duracion_estimada INTEGER,
    estado TEXT,
    id_empleado INTEGER,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
);
""")

conn.commit()
print("✅ Tablas creadas correctamente.")

# ----------------- Insertar turnos -----------------
turnos = [
    (1, "09:00", "15:00", "Proyección"),
    (2, "15:00", "21:00", "Limpieza")
]

cursor.executemany("INSERT OR IGNORE INTO turnos (id_turno, hora_inicio, hora_fin, area) VALUES (?, ?, ?, ?);", turnos)
conn.commit()
print("✅ Turnos insertados correctamente.")

# ----------------- Insertar empleados -----------------
empleados = [
    (1, "Carlos Díaz", 25, "carlos@cineplus.com", "Técnico", 1),
    (2, "Ana Torres", 28, "ana@cineplus.com", "Limpieza", 2),
    (3, "Luis Pérez", 30, "luis@cineplus.com", "Taquilla", 1),
    (4, "Marta Gómez", 26, "marta@cineplus.com", "Limpieza", 2),
    (5, "Jorge Ramírez", 32, "jorge@cineplus.com", "Seguridad", 1),
    (6, "Lucía Fernández", 29, "luciaf@cineplus.com", "Atención", 2)
]

cursor.executemany("INSERT OR IGNORE INTO empleados (id_empleado, nombre, edad, correo, puesto, id_turno) VALUES (?, ?, ?, ?, ?, ?);", empleados)
conn.commit()
print("✅ Empleados insertados correctamente.")

# ----------------- Insertar tareas -----------------
tareas = [
    (1, "Revisar proyector sala 1", "Proyección", 30, "Pendiente", 1),
    (2, "Revisar proyector sala 2", "Proyección", 30, "Pendiente", 2),
    (3, "Cobrar entradas", "Taquilla", 15, "Pendiente", 3),
    (4, "Limpiar pasillo principal", "Limpieza", 20, "Pendiente", 4),
    (5, "Patrullar entrada", "Seguridad", 25, "Pendiente", 5),
    (6, "Atender quejas clientes", "Atención", 10, "Pendiente", 6)
]

cursor.executemany("INSERT OR IGNORE INTO tareas (id_tarea, descripcion, area, duracion_estimada, estado, id_empleado) VALUES (?, ?, ?, ?, ?, ?);", tareas)
conn.commit()
print("✅ Tareas insertadas correctamente.")

# ----------------- Verificación -----------------
cursor.execute("SELECT * FROM empleados;")
print("\nEmpleados en la base de datos:")
for row in cursor.fetchall():
    print(row)

cursor.execute("SELECT * FROM tareas;")
print("\nTareas en la base de datos:")
for row in cursor.fetchall():
    print(row)

cursor.execute("SELECT * FROM turnos;")
print("\nTurnos en la base de datos:")
for row in cursor.fetchall():
    print(row)

# Cerrar conexión
conn.close()
