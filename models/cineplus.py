from datetime import datetime, time
from typing import List

class Persona:
    def __init__(self, id_: int, nombre: str, edad: int, correo: str):
        self._id = id_
        self._nombre = nombre
        self._edad = edad
        self._correo = correo

    def mostrar_informacion(self) -> str:
        return f"{self._nombre} ({self._edad}) - {self._correo}"

class Turno:
    def __init__(self, id_turno: int, hora_inicio: time, hora_fin: time, area: str):
        self.id_turno = id_turno
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.area = area

    def mostrar_turno(self):
        return f"Turno {self.id_turno}: {self.hora_inicio} - {self.hora_fin} ({self.area})"

class Tarea:
    def __init__(self, descripcion: str, area: str, duracion_estimada: int):
        self.descripcion = descripcion
        self.area = area
        self.duracion_estimada = duracion_estimada
        self.estado = "Pendiente"

    def marcar_completada(self):
        self.estado = "Completada"

    def __repr__(self):
        return f"Tarea({self.descripcion}, {self.area}, {self.estado})"

class Empleado(Persona):
    def __init__(self, id_, nombre, edad, correo, puesto, turno: Turno = None):
        super().__init__(id_, nombre, edad, correo)
        self._puesto = puesto
        self._turno = turno
        self._tareas: List[Tarea] = []
        self._asistencias: List[dict] = []

    def asignar_tarea(self, tarea: Tarea):
        self._tareas.append(tarea)

    def registrar_asistencia(self, fecha: datetime, presente: bool):
        self._asistencias.append({"fecha": fecha, "presente": presente})

    def mostrar_informacion(self):
        return f"Empleado: {self._nombre} - Puesto: {self._puesto}"

    @property
    def tareas(self):
        return list(self._tareas)

class Supervisor(Persona):
    def __init__(self, id_, nombre, edad, correo, area):
        super().__init__(id_, nombre, edad, correo)
        self._area = area
        self._equipo: List[Empleado] = []

    def agregar_empleado(self, empleado: Empleado):
        self._equipo.append(empleado)

    def asignar_turno(self, empleado: Empleado, turno: Turno):
        empleado._turno = turno

    def supervisar_tarea(self, empleado: Empleado, tarea: Tarea):
        # ejemplo simple: marcar tarea en proceso o completada
        for t in empleado._tareas:
            if t.descripcion == tarea.descripcion:
                t.estado = tarea.estado

    def mostrar_equipo(self):
        return list(self._equipo)

class Area:
    def __init__(self, nombre: str, responsable: Supervisor = None):
        self.nombre = nombre
        self.responsable = responsable
        self.personal: List[Empleado] = []

    def agregar_empleado(self, e: Empleado):
        self.personal.append(e)

    def mostrar_personal(self):
        return list(self.personal)

# Ejemplo de uso
if __name__ == "__main__":
    # Crear turnos
    t1 = Turno(1, time(9,0), time(15,0), "Proyección")
    t2 = Turno(2, time(15,0), time(21,0), "Limpieza")

    # Crear supervisor y empleados
    sup = Supervisor(1, "Lucía Pérez", 35, "lucia@cineplus.com", "Proyección")
    emp1 = Empleado(2, "Carlos Díaz", 25, "carlos@cineplus.com", "Técnico", t1)
    emp2 = Empleado(3, "Ana Torres", 28, "ana@cineplus.com", "Limpieza", t2)

    # Asignar empleados al supervisor and area
    sup.agregar_empleado(emp1)
    sup.agregar_empleado(emp2)
    area_proj = Area("Proyección", responsable=sup)
    area_proj.agregar_empleado(emp1)
    area_proj.agregar_empleado(emp2)

    # Asignar y completar tareas
    tarea1 = Tarea("Revisar proyector sala 2", "Proyección", 30)
    tarea2 = Tarea("Limpiar pasillo principal", "Limpieza", 20)
    emp1.asignar_tarea(tarea1)
    emp2.asignar_tarea(tarea2)

    print(sup.mostrar_equipo())
    print(emp1.mostrar_informacion())
    print("Tareas emp1:", emp1.tareas)
