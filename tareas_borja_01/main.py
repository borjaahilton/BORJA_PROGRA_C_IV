import flet as ft
from inicio_sesion import LoginView
from dashboard_view import DashboardView
from especialidades_view import EspecialidadesView
from docentes_view import DocentesView  

def main(page: ft.Page):
    page.title = "Sistema de Horarios Marello"
    page.window_width = 900
    page.window_height = 650
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- Función central para cambiar de vistas ---
    def cambiar_vista(vista):
        page.clean()
        page.add(vista)
        page.update()

    # --- Crear instancia de Login inicial ---
    login_view = LoginView(page, cambiar_vista)
    cambiar_vista(login_view)

ft.app(target=main)
