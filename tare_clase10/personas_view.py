import flet as ft
from conexion import ConexionDB


class PersonasView(ft.Container):
    def __init__(self, page, cambiar_vista):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista
        self.db = ConexionDB()

        titulo = ft.Text("📋 Gestión de Personas", size=22, weight="bold")

        btn_volver = ft.ElevatedButton("← Volver", on_click=self.volver)
        btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_personas())

        # DataTable
        self.table = ft.DataTable(columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombres")),
            ft.DataColumn(ft.Text("Apellidos")),
            ft.DataColumn(ft.Text("DNI")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Acciones")),
        ], rows=[], width=800)

        self.content = ft.Column([
            ft.Row([btn_volver, btn_actualizar], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            self.table
        ], expand=True, scroll=ft.ScrollMode.AUTO)

        # Cargar datos
        self.cargar_personas()

    def cargar_personas(self):
        resultado = self.db.listar_personas()
        if not resultado.get('status'):
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {resultado.get('mensaje')}"))
            self.page.snack_bar.open = True
            self.page.update()
            return

        filas = resultado.get('data', [])
        rows = []
        for f in filas:
            pid = f.get('id') or f.get('persona_id') or f.get('personaID') or ''
            nombres = f.get('nombres') or f.get('nombre') or ''
            apellidos = f.get('apellidos') or f.get('apellido') or ''
            dni = f.get('dni') or f.get('DNI') or ''
            telefono = f.get('telefono') or f.get('celular') or ''

            # Botones con icono (mejor estilo)
            btn_editar = ft.IconButton(ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, pid=pid: self.mostrar_formulario_editar(pid))
            btn_borrar = ft.IconButton(ft.Icons.DELETE, tooltip="Eliminar", on_click=lambda e, pid=pid: self.confirmar_borrar(pid))

            acciones = ft.Row([btn_editar, btn_borrar])

            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(pid))),
                ft.DataCell(ft.Text(nombres)),
                ft.DataCell(ft.Text(apellidos)),
                ft.DataCell(ft.Text(str(dni))),
                ft.DataCell(ft.Text(str(telefono))),
                ft.DataCell(acciones)
            ]))

        self.table.rows = rows
        # No llamar a self.update() aquí (evita AssertionError si el control aún no tiene UID)
        self.page.update()

    def mostrar_formulario_editar(self, persona_id):
        # Navegar a la vista de edición (archivo acciones/editar_persona_view.py)
        from acciones.editar_persona_view import EditarPersonaView

        # Definir una función 'volver' que recrea la vista de Personas y recarga los datos.
        def volver_a_personas():
            # Crear una nueva instancia de PersonasView para garantizar estado limpio
            nueva_vista = PersonasView(self.page, self.cambiar_vista)
            # Cambiar a la nueva vista y forzar carga de datos
            self.cambiar_vista(nueva_vista)
            try:
                nueva_vista.cargar_personas()
            except Exception:
                # Si algo falla, actualizamos la página para evitar estados inconsistentes
                self.page.update()

        editar_vista = EditarPersonaView(self.page, volver_a_personas, persona_id)
        # Cambiar a la vista de edición
        self.cambiar_vista(editar_vista)

    def confirmar_borrar(self, pid):
        def borrar(e):
            try:
                pid_int = int(pid)
            except Exception:
                pid_int = pid
            res = self.db.eliminar_persona(pid_int)
            try:
                print(f"[DEBUG] eliminar_persona id={pid} -> response: {res}")
            except Exception:
                pass
            # Cerrar diálogo y notificar resultado
            self._cerrar_dialogo()
            if res.get('status'):
                self.page.snack_bar = ft.SnackBar(ft.Text("Registro eliminado"))
                self.page.snack_bar.open = True
                self.cargar_personas()
            else:
                detalle = res.get('mensaje') or ''
                self.page.snack_bar = ft.SnackBar(ft.Text(f"No se eliminó: {detalle}"))
                self.page.snack_bar.open = True
            self.page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text("¿Desea eliminar este registro?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self._cerrar_dialogo()),
                ft.ElevatedButton("Eliminar", bgcolor=ft.Colors.RED_ACCENT_100, on_click=borrar)
            ]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def _cerrar_dialogo(self):
        try:
            if hasattr(self.page, 'dialog') and self.page.dialog:
                self.page.dialog.open = False
                self.page.update()
        except Exception:
            # si algo falla al cerrar el diálogo, actualizamos la página de todos modos
            self.page.update()

    def volver(self, e):
        from dashboard_view import DashboardView
        dash = DashboardView(self.page, self.cambiar_vista)
        self.cambiar_vista(dash)
