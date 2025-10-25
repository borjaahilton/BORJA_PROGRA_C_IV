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
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )

        # --- Botones ---
        btn_volver = ft.ElevatedButton(
            "⬅️ Volver al Dashboard",
            on_click=self.volver_dashboard
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

        # --- Almacenar datos originales ---
        self.datos_originales = []
        
        # --- Cargar datos iniciales ---
        self.cargar_docentes()

    def volver_dashboard(self, e):
        """Vuelve a la vista del dashboard."""
        from dashboard_view import DashboardView
        self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))

    def on_eliminar_click(self, e):
        """Maneja el evento de clic en el botón de eliminar."""
        if hasattr(e, 'control') and hasattr(e.control, 'data'):
            docente = e.control.data
            # Mostrar diálogo de confirmación
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirmar eliminación"),
                content=ft.Text(f"¿Está seguro que desea eliminar al docente {docente.get('nombres')} {docente.get('apellidos')}?"),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo()),
                    ft.TextButton("Eliminar", on_click=lambda e: self.confirmar_eliminacion(docente)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()

    def cerrar_dialogo(self):
        """Cierra el diálogo actual."""
        self.page.dialog.open = False
        self.page.update()

    def confirmar_eliminacion(self, docente):
        """Ejecuta la eliminación del docente tras confirmación."""
        try:
            # Primero cerramos el diálogo
            self.cerrar_dialogo()
            
            # Luego intentamos eliminar
            resultado = self.db.eliminar_docente(docente.get('docente_id'))
            
            if resultado.get('status'):
                self.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("✅ Docente eliminado correctamente"))
                )
                # Recargar la tabla
                self.cargar_docentes()
            else:
                self.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text(f"❌ Error: {resultado.get('mensaje')}"))
                )
        except Exception as e:
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text(f"❌ Error al eliminar: {str(e)}"))
            )

    def on_editar_click(self, e):
        """Maneja el evento de clic en el botón de editar."""
        if hasattr(e, 'control') and hasattr(e.control, 'data'):
            self.editar_docente(e.control.data)
        else:
            print("❌ Error: No se pudieron obtener los datos del docente")
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("❌ Error al obtener datos del docente"))
            )

    def editar_docente(self, docente_data):
        """Abre la vista de edición para el docente seleccionado."""
        from acciones.editar_docente_view import EditarDocenteView
        self.cambiar_vista(EditarDocenteView(self.page, self.cambiar_vista, docente_data))

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

        # Guardar datos originales
        self.datos_originales = resultado.get("data", [])
        self.tabla.rows.clear()

        for fila in self.datos_originales:
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
                
            # Crear los botones de acción
            # Crear una copia de los datos del docente para el botón
            # Crear los datos del docente para edición
            datos_docente = {
                "docente_id": docente_id,
                "nombres": nombres,
                "apellidos": apellidos,
                "especialidad": especialidad,
                "activo": activo == "Sí",
                "codigo_docente": fila.get("codigo_docente", "") if isinstance(fila, dict) else "",
                "observaciones": fila.get("observaciones", "") if isinstance(fila, dict) else "",
                "persona_id": fila.get("persona_id") if isinstance(fila, dict) else None
            }
            
            btn_editar = ft.IconButton(
                icon="edit",
                icon_color="blue400",
                tooltip="Editar",
                data=datos_docente,
                on_click=self.on_editar_click
            )

            btn_eliminar = ft.IconButton(
                icon="delete",
                icon_color="red400",
                tooltip="Eliminar",
                data=datos_docente,
                on_click=self.on_eliminar_click
            )

            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(docente_id))),
                        ft.DataCell(ft.Text(nombres)),
                        ft.DataCell(ft.Text(apellidos)),
                        ft.DataCell(ft.Text(especialidad)),
                        ft.DataCell(ft.Text(activo)),
                        ft.DataCell(ft.Row([btn_editar, btn_eliminar], spacing=10)),
                    ]
                )
            )

        self.page.update()
