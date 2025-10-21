import flet as ft
from conexion import ConexionDB

class DocentesView(ft.Container):
    """
    Vista para mostrar la tabla de docentes.
    """
    def __init__(self, page, cambiar_vista):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista
        self.db = ConexionDB()

        # --- Título ---
        titulo = ft.Text("👨‍🏫 Gestión de Docentes", size=24, weight="bold")

        # --- Tabla ---
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombres")),
                ft.DataColumn(ft.Text("Apellidos")),
                ft.DataColumn(ft.Text("Especialidad")),
                ft.DataColumn(ft.Text("Activo")),
            ],
            rows=[]
        )

        # --- Botones ---
        btn_volver = ft.ElevatedButton(
            "⬅️ Volver al Dashboard",
            on_click=lambda e: self.cambiar_vista(
                __import__("dashboard_view").DashboardView(self.page, self.cambiar_vista)
            )
        )
        btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_docentes())

        # --- Layout principal ---
        self.content = ft.Column(
            [
                titulo,
                ft.Row([btn_volver, btn_actualizar], alignment=ft.MainAxisAlignment.START),
                ft.Container(
                    ft.Column([self.tabla], expand=True, scroll=ft.ScrollMode.AUTO),
                    expand=True,
                    padding=10,
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=10
                )
            ],
            spacing=15,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

        # --- Cargar datos iniciales ---
        self.cargar_docentes()

    # -------------------------------------------------------------------------
    def cargar_docentes(self):
        """Carga los docentes desde la base de datos y llena la tabla."""
        try:
            resultado = self.db.listar_docentes()
        except Exception as e:
            print(f"❌ Error al ejecutar listar_docentes(): {e}")
            return

        if not isinstance(resultado, dict) or not resultado.get("status"):
            print(f"❌ listar_docentes() devolvió un error o formato inválido: {resultado}")
            return

        filas = resultado.get("data", [])
        self.tabla.rows.clear()

        for fila in filas:
            # Soportar tanto diccionarios como tuplas
            if isinstance(fila, dict):
                docente_id = fila.get("docente_id", "")
                nombres = fila.get("nombres", "")
                apellidos = fila.get("apellidos", "")
                especialidad = fila.get("especialidad", "")
                activo = "Sí" if fila.get("activo") else "No"
            else:
                docente_id = fila[0] if len(fila) > 0 else ""
                nombres = fila[1] if len(fila) > 1 else ""
                apellidos = fila[2] if len(fila) > 2 else ""
                especialidad = fila[3] if len(fila) > 3 else ""
                activo = "Sí" if fila[4] else "No" if len(fila) > 4 else ""

            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(docente_id))),
                        ft.DataCell(ft.Text(nombres)),
                        ft.DataCell(ft.Text(apellidos)),
                        ft.DataCell(ft.Text(especialidad)),
                        ft.DataCell(ft.Text(activo)),
                    ]
                )
            )

        self.page.update()
