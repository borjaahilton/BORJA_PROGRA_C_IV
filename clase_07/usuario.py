import flet as ft

def main(page: ft.Page):
    if not page.web:
        page.window_width = 400
        page.window_height = 600
        page.window.center()
        page.window_resizable = False

    page.add(
        ft.Column([
            ft.Text("Panel de Usuario", size=30, weight="bold", color="blue"),
            ft.Text("Bienvenido, usuario. Esta es tu ventana personal.", size=20),
            ft.ElevatedButton("Cerrar sesión", on_click=lambda e: page.go("/"))
        ],
        alignment="center",
        horizontal_alignment="center",
        spacing=30
        )
    )

ft.app(target=main)