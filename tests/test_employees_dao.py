import unittest
from dao import employees_dao as dao

# ==========================================================
# 💡 IMPORTANTE: Crear tablas antes de las pruebas
# ==========================================================
dao.crear_tablas()
dao.insertar_turnos_por_defecto()


class TestCinePlus(unittest.TestCase):

    # ----------------------
    # Prueba 1: Insertar empleado
    # ----------------------
    def test_insertar_empleado(self):
        dao.agregar_empleado(
            "Prueba Uno",
            22,
            "uno@mail.com",
            "Limpieza",
            "Mañana"
        )

        empleados = dao.obtener_empleados()
        self.assertGreater(
            len(empleados),
            0,
            "❌ No se insertó ningún empleado."
        )

    # ----------------------
    # Prueba 2: Consultar empleado por ID
    # ----------------------
    def test_consultar_empleado(self):
        empleados = dao.obtener_empleados()
        self.assertGreater(
            len(empleados),
            0,
            "❌ No hay empleados para consultar."
        )

        primer = empleados[0]
        encontrado = dao.obtener_empleado_por_id(primer["id"])

        self.assertIsNotNone(
            encontrado,
            "❌ No se encontró el empleado por ID."
        )


if __name__ == "__main__":
    unittest.main()
