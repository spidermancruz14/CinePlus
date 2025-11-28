import sqlite3
import os

DB_NAME = "cineplus.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def crear_tablas():
    conexion = conectar()
    cursor = conexion.cursor()

    # Crear tabla turnos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS turnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hora_inicio TEXT,
        hora_fin TEXT,
        area TEXT
    )
    """)

    # Crear tabla empleados
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS empleados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        edad INTEGER,
        correo TEXT,
        puesto TEXT,
        turno_id INTEGER,
        FOREIGN KEY(turno_id) REFERENCES turnos(id)
    )
    """)

    # Crear tabla supervisores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS supervisores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT,
        area TEXT
    )
    """)

    # Crear tabla tareas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT,
        area TEXT,
        duracion_estimada INTEGER,
        estado TEXT,
        empleado_id INTEGER,
        FOREIGN KEY(empleado_id) REFERENCES empleados(id)
    )
    """)

    # Opcional asistencias
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS asistencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empleado_id INTEGER,
        fecha TEXT,
        presente INTEGER,
        FOREIGN KEY(empleado_id) REFERENCES empleados(id)
    )
    """)

    conexion.commit()
    conexion.close()
    print("✔ Tablas creadas correctamente")
