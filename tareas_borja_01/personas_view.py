# personas_view.py
import flet as ft
from conexion import ConexionDB

class PersonasView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()

        self.titulo = ft.Text("👥 Gestión de Personas", size=22, weight="bold")

        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombres")),
                ft.DataColumn(ft.Text("Apellidos")),
                ft.DataColumn(ft.Text("DNI")),
                ft.DataColumn(ft.Text("Teléfono")),
            ],
            rows=[]
        )

        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_personas())

        self.content = ft.Column(
            [
                self.titulo,
                ft.Row([self.btn_volver, self.btn_actualizar], alignment=ft.MainAxisAlignment.START),
                ft.Container(self.tabla, expand=True, border_radius=10, padding=10, bgcolor=ft.Colors.BLUE_50)
            ],
            spacing=15,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

        # cargar datos iniciales
        self.cargar_personas()

    # Carga de datos desde MySQL
    def cargar_personas(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("SELECT persona_id, nombres, apellidos, numero_documento, telefono FROM personas")
                resultados = cursor.fetchall()

                self.tabla.rows.clear()
                for fila in resultados:
                    self.tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(fila[0]))),
                                ft.DataCell(ft.Text(fila[1])),
                                ft.DataCell(ft.Text(fila[2])),
                                ft.DataCell(ft.Text(fila[3])),
                                ft.DataCell(ft.Text(fila[4])),
                            ]
                        )
                    )
                self.page.update()

            except Exception as e:
                print(f"❌ Error al cargar personas: {e}")
            finally:
                self.conexion.cerrar(conexion)
