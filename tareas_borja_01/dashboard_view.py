import flet as ft

class DashboardView(ft.Container):
    def __init__(self, page, cambiar_vista):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista

        titulo = ft.Text(
            "📘 Panel Principal – Sistema de Horarios Marello",
            size=24,
            weight="bold"
        )

        tablas = [
            ("Usuarios", "Cuentas, credenciales y roles del sistema"),
            ("Personas", "Datos básicos personales"),
            ("Especialidades", "Campos de estudio o áreas académicas"),
            ("Docentes", "Profesores y sus especialidades"),
        ]

        grid = ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=280,
            child_aspect_ratio=1.2,
            spacing=10,
            run_spacing=10,
        )

        for nombre, descripcion in tablas:
            card_content = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(nombre, size=18, weight="bold"),
                        ft.Text(descripcion, size=13, color=ft.Colors.GREY),
                    ],
                    spacing=5,
                ),
                padding=15,
                border_radius=10,
                bgcolor=ft.Colors.BLUE_50,
                ink=True,
                on_click=lambda e, n=nombre: self.mostrar_tabla(n),
            )
            grid.controls.append(ft.Card(content=card_content, elevation=3))

        self.content = ft.Column(
            [titulo, grid],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
        )

    def mostrar_tabla(self, nombre_tabla):
        nombre_tabla = nombre_tabla.lower()

        if nombre_tabla == "usuarios":
            from usuarios_view import UsuariosView
            self.cambiar_vista(UsuariosView(self.page, lambda: self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))))
            return

        elif nombre_tabla == "especialidades":
            from especialidades_view import EspecialidadesView
            self.cambiar_vista(EspecialidadesView(self.page, lambda: self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))))
            return

        elif nombre_tabla == "personas":
            from personas_view import PersonasView
            self.cambiar_vista(PersonasView(self.page, lambda: self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))))
            return

        elif nombre_tabla == "docentes":
            from docentes_view import DocentesView
            self.cambiar_vista(DocentesView(self.page, lambda: self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))))
            return
