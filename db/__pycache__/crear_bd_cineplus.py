import mysql.connector
from mysql.connector import Error

def crear_bd_cineplus():
    conexion = None

    try:
        print("🔍 Conectando a MySQL...")
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="NuevaPassword123"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            # Crear BD
            cursor.execute("CREATE DATABASE IF NOT EXISTS cineplus;")
            cursor.execute("USE cineplus;")
            print("📁 Base de datos 'cineplus' lista.\n")

            # ======== TABLA PERSONA ========
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS persona (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                edad INT,
                correo VARCHAR(100)
            );
            """)

            # ======== TABLA TURNO ========
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS turno (
                id_turno INT AUTO_INCREMENT PRIMARY KEY,
                hora_inicio TIME NOT NULL,
                hora_fin TIME NOT NULL,
                area VARCHAR(50) NOT NULL
            );
            """)

            # ======== TABLA EMPLEADO ========
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS empleado (
                id_empleado INT AUTO_INCREMENT PRIMARY KEY,
                persona_id INT,
                puesto VARCHAR(50),
                turno_id INT,
                FOREIGN KEY (persona_id) REFERENCES persona(id),
                FOREIGN KEY (turno_id) REFERENCES turno(id_turno)
            );
            """)

            # ======== TABLA SUPERVISOR ========
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS supervisor (
                id_supervisor INT AUTO_INCREMENT PRIMARY KEY,
                persona_id INT,
                area_responsable VARCHAR(50),
                FOREIGN KEY (persona_id) REFERENCES persona(id)
            );
            """)

            # ======== TABLA AREA ========
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS area (
                id_area INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50),
                supervisor_id INT,
                FOREIGN KEY (supervisor_id) REFERENCES supervisor(id_supervisor)
            );
            """)

            # ======== TABLA TAREA ========
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tarea (
                id_tarea INT AUTO_INCREMENT PRIMARY KEY,
                descripcion VARCHAR(200),
                area VARCHAR(50),
                duracion_estimada INT,
                estado VARCHAR(20),
                empleado_id INT,
                FOREIGN KEY (empleado_id) REFERENCES empleado(id_empleado)
            );
            """)

            print("🧱 Tablas creadas con éxito.\n")

            # ===================================================
            # INSERTAR DATOS — CORRESPONDIENDO A TU CÓDIGO
            # ===================================================

            # Personas
            personas = [
                ("Carlos Díaz", 25, "carlos@cineplus.com"),
                ("Ana Torres", 28, "ana@cineplus.com"),
                ("Lucía Pérez", 35, "lucia@cineplus.com")
            ]
            cursor.executemany("INSERT INTO persona (nombre, edad, correo) VALUES (%s, %s, %s);", personas)

            # Turnos
            turnos = [
                ("09:00:00", "15:00:00", "Proyección"),
                ("15:00:00", "21:00:00", "Limpieza")
            ]
            cursor.executemany("INSERT INTO turno (hora_inicio, hora_fin, area) VALUES (%s, %s, %s);", turnos)

            # Supervisora
            cursor.execute("INSERT INTO supervisor (persona_id, area_responsable) VALUES (3, 'Proyección');")

            # Empleados
            empleados = [
                (1, "Técnico", 1),
                (2, "Limpieza", 2)
            ]
            cursor.executemany("""
                INSERT INTO empleado (persona_id, puesto, turno_id)
                VALUES (%s, %s, %s);
            """, empleados)

            # Área
            cursor.execute("""
                INSERT INTO area (nombre, supervisor_id)
                VALUES ('Proyección', 1);
            """)

            # Tareas
            tareas = [
                ("Revisar proyector sala 2", "Proyección", 30, "Pendiente", 1),
                ("Limpiar pasillo principal", "Limpieza", 20, "Pendiente", 2)
            ]
            cursor.executemany("""
                INSERT INTO tarea (descripcion, area, duracion_estimada, estado, empleado_id)
                VALUES (%s, %s, %s, %s, %s);
            """, tareas)

            conexion.commit()

            print("📦 Datos insertados correctamente.\n")

    except Error as e:
        print("❌ Error:", e)

    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()
            print("🔒 Conexión cerrada.")

if __name__ == "__main__":
    crear_bd_cineplus()
