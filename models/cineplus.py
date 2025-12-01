from datetime import time
from typing import List
from tabulate import tabulate

# ----------------- Clases -----------------
class Persona:
    def __init__(self, id_: int, nombre: str, edad: int, correo: str):
        self._id = id_
        self._nombre = nombre
        self._edad = edad
        self._correo = correo

class Turno:
    def __init__(self, id_turno: int, hora_inicio: time, hora_fin: time, area: str):
        self.id_turno = id_turno
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.area = area

    def __repr__(self):
        return f"{self.hora_inicio.strftime('%H:%M')}-{self.hora_fin.strftime('%H:%M')} ({self.area})"

class Tarea:
    def __init__(self, descripcion: str, area: str, duracion_estimada: int):
        self.descripcion = descripcion
        self.area = area
        self.duracion_estimada = duracion_estimada
        self.estado = "Pendiente"

    def __repr__(self):
        return f"{self.descripcion} [{self.estado}]"

class Empleado(Persona):
    def __init__(self, id_, nombre, edad, correo, puesto, turno: Turno = None):
        super().__init__(id_, nombre, edad, correo)
        self._puesto = puesto
        self._turno = turno
        self._tareas: List[Tarea] = []

    def asignar_tarea(self, tarea: Tarea):
        self._tareas.append(tarea)

    @property
    def tareas(self):
        return list(self._tareas)

# ----------------- Ejemplo de uso -----------------
if __name__ == "__main__":
    # Crear turnos
    t1 = Turno(1, time(9,0), time(15,0), "Proyección")
    t2 = Turno(2, time(15,0), time(21,0), "Limpieza")

    # Crear 6 empleados
    empleados = [
        Empleado(1, "Carlos Díaz", 25, "carlos@cineplus.com", "Técnico", t1),
        Empleado(2, "Ana Torres", 28, "ana@cineplus.com", "Limpieza", t2),
        Empleado(3, "Luis Pérez", 30, "luis@cineplus.com", "Taquilla", t1),
        Empleado(4, "Marta Gómez", 26, "marta@cineplus.com", "Limpieza", t2),
        Empleado(5, "Jorge Ramírez", 32, "jorge@cineplus.com", "Seguridad", t1),
        Empleado(6, "Lucía Fernández", 29, "luciaf@cineplus.com", "Atención", t2)
    ]

    # Crear 6 tareas y asignarlas
    tareas = [
        Tarea("Revisar proyector sala 1", "Proyección", 30),
        Tarea("Revisar proyector sala 2", "Proyección", 30),
        Tarea("Cobrar entradas", "Taquilla", 15),
        Tarea("Limpiar pasillo principal", "Limpieza", 20),
        Tarea("Patrullar entrada", "Seguridad", 25),
        Tarea("Atender quejas clientes", "Atención", 10)
    ]

    for emp, tarea in zip(empleados, tareas):
        emp.asignar_tarea(tarea)

    # Preparar datos para tabla
    tabla = []
    for emp in empleados:
        tarea_str = ", ".join([str(t) for t in emp.tareas])
        tabla.append([emp._id, emp._nombre, emp._edad, emp._correo, emp._puesto, emp._turno, tarea_str])

    # Mostrar tabla
    print(tabulate(tabla, headers=["ID", "Nombre", "Edad", "Correo", "Puesto", "Turno", "Tarea"], tablefmt="grid"))
