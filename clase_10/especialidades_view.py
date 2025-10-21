import flet as ft
from conexion import ConexionDB

class EspecialidadesView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.db = ConexionDB()

        self.titulo = ft.Text("📘 Lista de Especialidades", size=22, weight="bold")
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Descripción")),
            ],
            rows=[]
        )

        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_especialidades())

        self.content = ft.Column(
            [
                self.titulo,
                ft.Row([self.btn_volver, self.btn_actualizar]),
                ft.Container(ft.Column([self.tabla], scroll=ft.ScrollMode.AUTO), expand=True, padding=10)
            ],
            expand=True
        )

        self.cargar_especialidades()

    def cargar_especialidades(self):
        resultado = self.db.listar_especialidades()
        self.tabla.rows.clear()

        if not resultado.get("status"):
            print("❌", resultado.get("mensaje"))
            return

        for esp in resultado["data"]:
            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(esp["especialidad_id"]))),
                        ft.DataCell(ft.Text(esp["nombre"])),
                        ft.DataCell(ft.Text(esp["descripcion"] or "")),
                    ]
                )
            )
        self.page.update()
