# models.py
from dataclasses import dataclass, field
from typing import List, Optional

# ----------------------------
#      CLASE PERSONA
# ----------------------------
@dataclass
class Persona:
    id: Optional[int]
    nombre: str
    edad: Optional[int] = None
    correo: Optional[str] = None

    def mostrar(self) -> str:
        return f"{self.nombre} ({self.edad}) - {self.correo or '-'}"


# ----------------------------
#      CLASE TURNO
# ----------------------------
@dataclass
class Turno:
    id: Optional[int]
    nombre: str
    inicio: str
    fin: str
    area: Optional[str] = None

    def __repr__(self):
        return f"{self.nombre} {self.inicio}-{self.fin}"


# ----------------------------
#      CLASE TAREA
# ----------------------------
@dataclass
class Tarea:
    id: Optional[int]
    descripcion: str
    area: str
    duracion_estimada: int
    estado: str = "Pendiente"

    def marcar_completada(self):
        self.estado = "Completada"


# ----------------------------
#      CLASE EMPLEADO
# ----------------------------
@dataclass
class Empleado(Persona):
    puesto: Optional[str] = None
    turno: Optional[str] = None
    tareas: List[Tarea] = field(default_factory=list)

    def asignar_tarea(self, tarea: Tarea):
        self.tareas.append(tarea)


# ----------------------------
#      CLASE SUPERVISOR
# ----------------------------
@dataclass
class Supervisor(Persona):
    area: Optional[str] = None
    equipo: List[Empleado] = field(default_factory=list)

    def agregar_empleado(self, emp: Empleado):
        self.equipo.append(emp)


# ----------------------------
#      CLASE AREA TRABAJO
# ----------------------------
@dataclass
class AreaTrabajo:
    nombre: str
    descripcion: Optional[str] = None

    def info(self):
        return f"Área: {self.nombre} - {self.descripcion or 'Sin descripción'}"
