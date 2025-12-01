import sqlite3

def get_connection():
    return sqlite3.connect("cineplus.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # TABLA clientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telefono TEXT,
            fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # TABLA turnos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turnos (
            id_turno INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_turno TEXT NOT NULL,
            hora_inicio TEXT NOT NULL,
            hora_fin TEXT NOT NULL
        );
    """)

    # Insertar turnos si no existen
    cursor.execute("SELECT COUNT(*) FROM turnos;")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO turnos (nombre_turno, hora_inicio, hora_fin)
            VALUES (?, ?, ?);
        """, [
            ("Mañana", "08:00", "14:00"),
            ("Tarde", "14:00", "20:00"),
            ("Noche", "20:00", "02:00")
        ])

    # TABLA empleados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            puesto TEXT NOT NULL,
            id_turno INTEGER,
            FOREIGN KEY(id_turno) REFERENCES turnos(id_turno)
        );
    """)

    # TABLA salas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS salas (
            id_sala INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_sala TEXT NOT NULL,
            capacidad INTEGER NOT NULL
        );
    """)

    # TABLA asientos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asientos (
            id_asiento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_sala INTEGER NOT NULL,
            numero_asiento TEXT NOT NULL,
            FOREIGN KEY(id_sala) REFERENCES salas(id_sala)
        );
    """)

    # TABLA peliculas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS peliculas (
            id_pelicula INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            duracion INTEGER NOT NULL,
            clasificacion TEXT,
            genero TEXT
        );
    """)

    # TABLA funciones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funciones (
            id_funcion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pelicula INTEGER NOT NULL,
            id_sala INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            FOREIGN KEY(id_pelicula) REFERENCES peliculas(id_pelicula),
            FOREIGN KEY(id_sala) REFERENCES salas(id_sala)
        );
    """)

    # TABLA ventas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_funcion INTEGER NOT NULL,
            id_asiento INTEGER NOT NULL,
            fecha_venta TEXT DEFAULT CURRENT_TIMESTAMP,
            total REAL NOT NULL,
            FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente),
            FOREIGN KEY(id_funcion) REFERENCES funciones(id_funcion),
            FOREIGN KEY(id_asiento) REFERENCES asientos(id_asiento)
        );
    """)

    conn.commit()
    conn.close()
