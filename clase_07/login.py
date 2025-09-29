import flet as ft

def main(page: ft.Page):
    if not page.web:
        page.window_width = 400
        page.window_height = 600
        page.window.center()
        page.window_resizable = False

    usuario = ft.TextField(label="Usuario", width=300)
    contrasena = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    mensaje = ft.Text("")

    def iniciar_sesion(e):
        if usuario.value == "borja" and contrasena.value == "70783090":
            page.clean()
            page.add(
                ft.Column([
                    ft.Text("Panel de Administrador", size=30, weight="bold", color="green"),
                    ft.Text("Bienvenido, borja. Aquí puedes gestionar el sistema.", size=20),
                    ft.ElevatedButton("Cerrar sesión", on_click=lambda e: page.go("/"))
                ], alignment="center", horizontal_alignment="center", spacing=30)
            )
        elif usuario.value == "usuario" and contrasena.value == "30303030":
            page.clean()
            page.add(
                ft.Column([
                    ft.Text("Panel de Usuario", size=30, weight="bold", color="blue"),
                    ft.Text("Bienvenido, usuario. Esta es tu ventana personal.", size=20),
                    ft.ElevatedButton("Cerrar sesión", on_click=lambda e: page.go("/"))
                ], alignment="center", horizontal_alignment="center", spacing=30)
            )
        else:
            mensaje.value = "Usuario o contraseña incorrectos"
            mensaje.color = "red"
            page.update()

    boton = ft.ElevatedButton("Iniciar sesión", on_click=iniciar_sesion)

    page.add(
        ft.Row([
            ft.Column([
                ft.Text("Iniciar sesión", size=30, weight="bold", text_align="center"),
                usuario,
                contrasena,
                boton,
                mensaje
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=20
            )
        ],
        alignment="center",
        vertical_alignment="center",
        expand=True
        )
    )

ft.app(target=main)