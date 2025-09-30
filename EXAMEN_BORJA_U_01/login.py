import flet as ft

def login_view(page):
    usuario = ft.TextField(
        label="Usuario",
        width=300,
        border_color="blue",
        border_width=2,
        text_align="center",
        color="black",
        text_size=18
    )
    contrasena = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=300,
        border_color="blue",
        border_width=2,
        text_align="center",
        color="black",
        text_size=18
    )
    mensaje = ft.Text("", size=18, weight="bold")

    def iniciar_sesion(e):
        if usuario.value == "borja" and contrasena.value == "70783090":
            page.go("/ejemplos")
        elif usuario.value == "usuario" and contrasena.value == "30303030":
            page.go("/usuario")
        elif usuario.value == "visitante" and contrasena.value == "12345678":
            page.go("/visitante")
        elif usuario.value == "cliente" and contrasena.value == "20202020":
            page.go("/cliente") 
        else:
            mensaje.value = "Usuario o contraseña incorrectos"
            mensaje.color = "red"
            page.update()

    boton = ft.ElevatedButton("Iniciar sesión", on_click=iniciar_sesion)

    page.add(
        ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("Iniciar sesión", size=32, weight="bold", text_align="center", color="blue"),
                    usuario,
                    contrasena,
                    boton,
                    mensaje
                ],
                alignment="center",
                horizontal_alignment="center",
                spacing=20
                ),
                width=370,
                padding=25,
                bgcolor="white",
                border_radius=15,
                border=ft.border.all(2, "blue"),
                shadow=ft.BoxShadow(blur_radius=16, color="#90caf9", offset=ft.Offset(0, 6)),
                alignment=ft.alignment.center
            )
        ],
        alignment="center",
        vertical_alignment="center",
        expand=True
        )
    )
    
    
def visitante_view(page):
    productos = [
        {
            "nombre": "Nike Air Max 90",
            "precio": "129,99 €",
            "imagen": "https://static.nike.com/a/images/t_PDP_864_v1/f_auto,q_auto:eco/4b2e2e2b-2e2e-4b2e-8e2e-2e2e2e2e2e2e/air-max-90-zapatillas.png"
        }
    ]

    catalogo = ft.Column([
        ft.Text("Bienvenido al Catálogo de Zapatillas (visitante)", size=32, weight="bold", color="blue", text_align="center"),
        ft.Text("Catálogo de Zapatillas", size=26, weight="bold", color="black", text_align="center"),
        ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Image(p["imagen"], width=140, height=140, fit="cover"),
                    ft.Text(p["nombre"], size=18, weight="bold", text_align="center"),
                    ft.Text(p["precio"], size=20, color="red", weight="bold"),
                    ft.ElevatedButton("Añadir al carrito")
                ], alignment="center", spacing=10),
                width=180,
                padding=12,
                bgcolor="#f5f5f5",
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=10, color="#90caf9", offset=ft.Offset(0, 2)),
                alignment=ft.alignment.center
            ) for p in productos
        ], alignment="center", spacing=28),
        ft.ElevatedButton("Cerrar sesión", on_click=lambda e: page.go("/"), style=ft.ButtonStyle(bgcolor="red", color="white", shape=ft.RoundedRectangleBorder(radius=8)))
    ], alignment="center", spacing=28)

    page.add(
        ft.Row([
            ft.Container(
                content=catalogo,
                width=820,
                padding=38,
                bgcolor="white",
                border_radius=18,
                shadow=ft.BoxShadow(blur_radius=18, color="#90caf9", offset=ft.Offset(0, 8)),
                alignment=ft.alignment.center
            )
        ], alignment="center", vertical_alignment="center", expand=True)
    )

def cliente_view(page):
    productos = [
        {
            "nombre": "Vans Old Skool",
            "precio": "89,99 €",
            "imagen": "https://images.vans.com/is/image/VansBrand/A4BV3BLK-HERO?wid=800&hei=800&fmt=png-alpha"
        }
    ]
    catalogo = ft.Column([
        ft.Text("Bienvenido al Catálogo de Zapatillas (Cliente)", size=32, weight="bold", color="blue", text_align="center"),
        ft.Text("Catálogo de Zapatillas", size=26, weight="bold", color="black", text_align="center"),
        ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Image(p["imagen"], width=140, height=140, fit="cover"),
                    ft.Text(p["nombre"], size=18, weight="bold", text_align="center"),
                    ft.Text(p["precio"], size=20, color="red", weight="bold"),
                    ft.ElevatedButton("Añadir al carrito")
                ], alignment="center", spacing=10),
                width=180,
                padding=12,
                bgcolor="#f5f5f5",
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=10, color="#90caf9", offset=ft.Offset(0, 2)),
                alignment=ft.alignment.center
            ) for p in productos
        ], alignment="center", spacing=28),
        ft.ElevatedButton("Cerrar sesión", on_click=lambda e: page.go("/"), style=ft.ButtonStyle(bgcolor="red", color="white", shape=ft.RoundedRectangleBorder(radius=8)))
    ], alignment="center", spacing=28)

    page.add(
        ft.Row([
            ft.Container(
                content=catalogo,
                width=820,
                padding=38,
                bgcolor="white",
                border_radius=18,
                shadow=ft.BoxShadow(blur_radius=18, color="#90caf9", offset=ft.Offset(0, 8)),
                alignment=ft.alignment.center
            )
        ], alignment="center", vertical_alignment="center", expand=True)
    )
        
    

def admin_view(page):
    page.add(
        ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("Panel de Administrador", size=30, weight="bold", color="white"),
                    ft.Text("Bienvenido, admin. Aquí puedes gestionar el sistema.", size=20, color="white")
                ], alignment="center", spacing=18),
                width=240,
                padding=22,
                bgcolor="#1976d2",
                border_radius=14,
                border=ft.border.all(2, "#1565c0"),
                shadow=ft.BoxShadow(blur_radius=12, color="#90caf9", offset=ft.Offset(0, 4)),
                alignment=ft.alignment.center,
                margin=ft.margin.only(left=0, right=14)
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Funciones del Administrador", size=26, weight="bold", color="green"),
                    ft.ElevatedButton("Gestionar usuarios"),
                    ft.ElevatedButton("Ver reportes"),
                    ft.ElevatedButton("Configuración"),
                    ft.ElevatedButton("Cerrar sesión", on_click=lambda e: page.go("/"))
                ], alignment="center", spacing=18),
                expand=1,
                padding=28,
                bgcolor="white",
                border_radius=14,
                border=ft.border.all(2, "green"),
                shadow=ft.BoxShadow(blur_radius=12, color="#a5d6a7", offset=ft.Offset(0, 4)),
                alignment=ft.alignment.center,
                margin=ft.margin.only(left=0, right=0)
            )
        ],
        alignment="start",
        vertical_alignment="center",
        expand=True
        )
    )

def usuario_view(page):
    productos = [
        {
            "nombre": "Nike Air Max 90",
            "precio": "129,99 €",
            "imagen": "https://static.nike.com/a/images/t_PDP_864_v1/f_auto,q_auto:eco/4b2e2e2b-2e2e-4b2e-8e2e-2e2e2e2e2e2e/air-max-90-zapatillas.png"
        },
        {
            "nombre": "Adidas Ultraboost",
            "precio": "149,99 €",
            "imagen": "https://assets.adidas.com/images/w_600,f_auto,q_auto/7e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e_9366/Ultraboost_21_Zapatillas_Blanco_FY0377_01_standard.jpg"
        },
        {
            "nombre": "Puma RS-X",
            "precio": "119,99 €",
            "imagen": "https://images.puma.com/image/upload/f_auto,q_auto,b_rgb:fafafa,w_600,h_600/global/369579/01/sv01/fnd/PNA/fmt/png/RS-X-Reinvention-Men's-Sneakers"
        }
    ]

    catalogo = ft.Column([
        ft.Text("Bienvenido al Catálogo de Zapatillas", size=32, weight="bold", color="blue", text_align="center"),
        ft.Text("Catálogo de Zapatillas", size=26, weight="bold", color="black", text_align="center"),
        ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Image(p["imagen"], width=140, height=140, fit="cover"),
                    ft.Text(p["nombre"], size=18, weight="bold", text_align="center"),
                    ft.Text(p["precio"], size=20, color="red", weight="bold"),
                    ft.ElevatedButton("Añadir al carrito")
                ], alignment="center", spacing=10),
                width=180,
                padding=12,
                bgcolor="#f5f5f5",
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=10, color="#90caf9", offset=ft.Offset(0, 2)),
                alignment=ft.alignment.center
            ) for p in productos
        ], alignment="center", spacing=28),
        ft.ElevatedButton("Cerrar sesión", on_click=lambda e: page.go("/"), style=ft.ButtonStyle(bgcolor="red", color="white", shape=ft.RoundedRectangleBorder(radius=8)))
    ], alignment="center", spacing=28)

    page.add(
        ft.Row([
            ft.Container(
                content=catalogo,
                width=820,
                padding=38,
                bgcolor="white",
                border_radius=18,
                shadow=ft.BoxShadow(blur_radius=18, color="#90caf9", offset=ft.Offset(0, 8)),
                alignment=ft.alignment.center
            )
        ], alignment="center", vertical_alignment="center", expand=True)
    )



def main(page: ft.Page):
    if not page.web:
        page.window_width = 400
        page.window_height = 600
        page.window.center()
        page.window_resizable = False
    page.bgcolor = "#b3e5fc"

    def route_change(e):
        page.clean()
        if page.route == "/":
            login_view(page)
        elif page.route == "/ejemplos":
            admin_view(page)
        elif page.route == "/usuario":
            usuario_view(page)
        elif page.route == "/visitante":
            visitante_view(page)
        elif page.route == "/cliente":
            cliente_view(page)
        else:
            page.go("/")

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)

