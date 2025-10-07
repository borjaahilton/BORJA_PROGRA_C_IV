import flet as ft
from conexion import ConexionDB

def main(page: ft.Page):
    page.title = "Sistema de Horarios - Login"
    page.theme_mode = "light"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 420
    page.window_height = 420

    page.bgcolor = "#F3F4F6"

    usuario = ft.TextField(label="Usuario", width=300, autofocus=True)
    contrasena = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    mensaje_estado = ft.Text("", color="gray", size=12)
    mensaje_debug = ft.Text("", color="gray", size=12)

    def verificar_conexion():
        db = ConexionDB()
        conexion = db.conectar()
        if conexion:
            mensaje_debug.value = "✅ Conexión establecida con la base de datos"
            db.cerrar(conexion)
        else:
            mensaje_debug.value = "❌ No se pudo conectar a la base de datos"
            mensaje_debug.color = "red"
        page.update()

    def login_click(e):
        user = usuario.value.strip()
        pwd = contrasena.value.strip()

        if not user or not pwd:
            mensaje_estado.value = "⚠️ Complete ambos campos."
            mensaje_estado.color = "orange"
            page.update()
            return

        db = ConexionDB()
        resultado = db.login_usuario(user, pwd)

        if resultado["status"]:
            mensaje_estado.value = f"✅ {resultado['mensaje']}: {resultado['data']['nombre_usuario']}"
            mensaje_estado.color = "green"
        else:
            mensaje_estado.value = f"❌ {resultado['mensaje']}"
            mensaje_estado.color = "red"

        page.update()

    boton_login = ft.ElevatedButton("Iniciar Sesión", width=300, on_click=login_click)

    card = ft.Container(
        content=ft.Column(
            [
                ft.Text("Inicio de Sesión", size=22, weight="bold", text_align="center"),
                usuario,
                contrasena,
                boton_login,
                mensaje_estado,
                mensaje_debug
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=40,
        border_radius=20,
        bgcolor="white",
        shadow=ft.BoxShadow(blur_radius=20, color="#ccc"),
        alignment=ft.alignment.center
    )

    page.add(card)
    verificar_conexion()

ft.app(target=main)
