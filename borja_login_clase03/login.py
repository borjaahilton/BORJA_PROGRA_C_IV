import flet as ft
import os
import sys
import subprocess

# Usuario/contraseña de ejemplo (puedes cambiarlo o conectarlo a BD)
USUARIO = "ahilton borja"
PASSWORD = "202020"

def main(page: ft.Page):
    if not page.web:
        page.window.width = 400
        page.window.height = 300
        page.window.center()
        page.window.resizable = False

    page.title = "Login - Sistema de Ventas"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Campos de entrada
    user_input = ft.TextField(label="Usuario", width=250)
    pass_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=250)
    mensaje = ft.Text("", color="red")

    # Función para validar login
    def validar_login(e):
        if user_input.value == USUARIO and pass_input.value == PASSWORD:
            mensaje.value = "✅ Acceso correcto"
            page.update()
            abrir_dashboard()
        else:
            mensaje.value = "❌ Usuario o contraseña incorrectos"
            page.update()

    # Botón de login
    btn_login = ft.ElevatedButton(
        text="Ingresar",
        bgcolor="#2196F3",
        color="white",
        width=250,
        on_click=validar_login
    )

    # Layout del login
    page.add(
        ft.Column(
            [
                ft.Text("🔑 INICIAR SESIÓN", size=22, weight=ft.FontWeight.BOLD, color="#2196F3"),
                user_input,
                pass_input,
                btn_login,
                mensaje
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )

    # Función para abrir dashboard
    def abrir_dashboard():
        page.window.close()
        ruta_dashboard = os.path.join(os.path.dirname(__file__), "dashboard.py")
        subprocess.Popen([sys.executable, ruta_dashboard])

if __name__ == "__main__":
    ft.app(target=main)

