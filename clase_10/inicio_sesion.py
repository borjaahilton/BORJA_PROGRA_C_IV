import flet as ft
from conexion import ConexionDB
from dashboard_view import DashboardView

class LoginView(ft.Container):
    def __init__(self, page: ft.Page, cambiar_vista=None):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista
        self.conexion = ConexionDB()

        # Campos de texto
        self.txt_usuario = ft.TextField(label="Usuario", width=250)
        self.txt_password = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=250
        )
        self.lbl_mensaje = ft.Text(value="", color="red")

        # Botón de ingreso
        self.btn_ingresar = ft.ElevatedButton("Ingresar", on_click=self.login)

        # Contenedor del formulario centrado
        self.content = ft.Column(
            [
                ft.Text("🔐 Login del Sistema de Horarios", size=22, weight="bold"),
                self.txt_usuario,
                self.txt_password,
                self.btn_ingresar,
                self.lbl_mensaje
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        # Centramos todo el formulario
        self.alignment = ft.alignment.center
        self.content.alignment = ft.MainAxisAlignment.CENTER
        self.content.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ──────────────────────────────────────────────
    # FUNCIÓN DE LOGIN
    # ──────────────────────────────────────────────
    def login(self, e):
        usuario = self.txt_usuario.value.strip()
        password = self.txt_password.value.strip()

        # Validación de campos vacíos
        if not usuario or not password:
            self.lbl_mensaje.value = "⚠️ Ingrese usuario y contraseña"
            self.lbl_mensaje.color = "red"
            self.update()
            return

        # Llamada al método de conexión
        datos = self.conexion.login_usuario(usuario, password)

        if datos:
            self.lbl_mensaje.value = "✅ Acceso correcto"
            self.lbl_mensaje.color = "green"
            self.update()
            # Carga del dashboard
            dashboard = DashboardView(self.page, self.cambiar_vista)
            self.cambiar_vista(dashboard)
        else:
            self.lbl_mensaje.value = "❌ Usuario o contraseña incorrectos"
            self.lbl_mensaje.color = "red"
            self.update()
