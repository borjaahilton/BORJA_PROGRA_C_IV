import flet as ft
from conexion import ConexionDB

class EditarDocenteView(ft.Container):
    def __init__(self, page, cambiar_vista, docente_data):
        super().__init__()
        self.page = page
        self.cambiar_vista = cambiar_vista
        self.docente_data = docente_data
        self.db = ConexionDB()
        self.expand = True

        # --- Título ---
        titulo = ft.Text("✏️ Editar Docente", size=24, weight="bold")

        # --- Campos de edición ---
        self.txt_nombres = ft.TextField(
            label="Nombres",
            value=docente_data.get("nombres", ""),
            width=300
        )
        
        self.txt_apellidos = ft.TextField(
            label="Apellidos",
            value=docente_data.get("apellidos", ""),
            width=300
        )

        self.txt_codigo = ft.TextField(
            label="Código Docente",
            value=docente_data.get("codigo_docente", ""),
            width=300
        )

        self.cb_activo = ft.Checkbox(
            label="Activo",
            value=docente_data.get("activo", True)
        )

        self.txt_observaciones = ft.TextField(
            label="Observaciones",
            value=docente_data.get("observaciones", ""),
            width=600,
            multiline=True,
            min_lines=3,
            max_lines=5
        )

        # --- Botones ---
        btn_guardar = ft.ElevatedButton(
            "💾 Guardar Cambios",
            on_click=self.guardar_cambios
        )
        
        btn_cancelar = ft.OutlinedButton(
            "❌ Cancelar",
            on_click=lambda e: self.volver_a_docentes()
        )

        # --- Layout ---
        self.content = ft.Column(
            [
                titulo,
                ft.Container(height=20),  # Espaciador
                ft.Row([self.txt_nombres, self.txt_apellidos], spacing=20),
                ft.Row([self.txt_codigo, self.cb_activo], spacing=20),
                self.txt_observaciones,
                ft.Container(height=20),  # Espaciador
                ft.Row(
                    [btn_cancelar, btn_guardar],
                    alignment=ft.MainAxisAlignment.END,
                    spacing=10
                )
            ],
            spacing=10,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

    def guardar_cambios(self, e):
        print("🔄 Iniciando proceso de guardado...")

        # Validaciones básicas
        nombres = self.txt_nombres.value.strip()
        apellidos = self.txt_apellidos.value.strip()

        if not nombres or not apellidos:
            self.mostrar_mensaje("Los nombres y apellidos son obligatorios")
            return

        # Obtener el ID del docente
        docente_id = self.docente_data.get("docente_id")
        print(f"🆔 ID del docente a actualizar: {docente_id}")

        if not docente_id:
            self.mostrar_mensaje("Error: No se pudo obtener el ID del docente")
            return

        # Preparar datos para actualización
        datos_actualizados = {
            "nombres": nombres,
            "apellidos": apellidos,
            "codigo_docente": self.txt_codigo.value.strip(),
            "activo": self.cb_activo.value,
            "observaciones": self.txt_observaciones.value.strip()
        }
        print(f"📝 Datos a actualizar: {datos_actualizados}")

        try:
            # Intentar actualizar usando el método correcto
            resultado = self.db.actualizar_docente_completo(docente_id, datos_actualizados)
            print(f"📊 Resultado de la actualización: {resultado}")

            if resultado.get("status"):
                # Importar aquí para evitar ciclos y crear la vista actualizada
                from docentes_view import DocentesView
                self.mostrar_mensaje("✅ Docente actualizado correctamente")
                # Navegar directamente a la lista de docentes (se recargará al inicializarse)
                self.cambiar_vista(DocentesView(self.page, self.cambiar_vista))
            else:
                self.mostrar_mensaje(f"❌ Error: {resultado.get('mensaje')}")
        except Exception as e:
            print(f"❌ Error durante la actualización: {str(e)}")
            self.mostrar_mensaje(f"❌ Error al guardar: {str(e)}")

    def mostrar_mensaje(self, mensaje):
        """Muestra un mensaje usando SnackBar."""
        self.page.snack_bar = ft.SnackBar(content=ft.Text(mensaje))
        self.page.snack_bar.open = True
        self.page.update()

    def volver_a_docentes(self):
        from docentes_view import DocentesView
        self.cambiar_vista(DocentesView(self.page, self.cambiar_vista))