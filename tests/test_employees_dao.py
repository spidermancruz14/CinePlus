import unittest
from gui import employees_dao as dao

class TestCinePlus(unittest.TestCase):

    # Prueba 1: Insertar empleado
    def test_insertar_empleado(self):
        dao.agregar_empleado("Prueba Uno", 22, "uno@mail.com", "Limpieza", "Mañana")
        empleados = dao.obtener_empleados()
        self.assertGreater(len(empleados), 0)

    # Prueba 2: Consultar empleado por ID
    def test_consultar_empleado(self):
        empleados = dao.obtener_empleados()
        emp = empleados[0]  # tomar el primero
        encontrado = dao.obtener_empleado_por_id(emp["id"])
        self.assertIsNotNone(encontrado)

if __name__ == "__main__":
    unittest.main()
