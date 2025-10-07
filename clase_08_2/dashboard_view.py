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

        # --- Lista de tablas del sistema ---
        tablas = [
            ("Personas", "Datos básicos (base de la identidad)"),
            ("Usuarios", "Cuentas, credenciales, y roles (enlace a personas)"),
            ("Especialidades", "Campos de estudio (Informática, Contabilidad, etc.)"),
            ("Ciclos", "Los 6 niveles académicos (I, II, III, etc.)"),
            ("Cursos", "Materias que se dictan"),
            ("Aulas", "Recurso físico limitado"),
            ("Docentes", "Quién enseña (enlace a Personas)"),
            ("Horarios_Base", "Slots fijos de tiempo"),
            ("Semanas", "Las 18 semanas del ciclo"),
            ("Estructura_Curricular", "Regla curricular (Curso–Ciclo–Especialidad)"),
            ("Asignaciones_Semanales", "Asignación final Docente + Curso + Aula + Semana"),
        ]

        # --- Diseño de la cuadrícula ---
        grid = ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=280,
            child_aspect_ratio=1.2,
            spacing=10,
            run_spacing=10,
        )

        # --- Crear tarjetas dinámicamente ---
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

        # --- Estructura visual principal ---
        self.content = ft.Column(
            [
                titulo,
                grid,
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
        )

    # --- Controlador de clics en las tarjetas ---
    def mostrar_tabla(self, nombre_tabla):
        nombre_tabla = nombre_tabla.lower()

        # 🧩 Importaciones locales para evitar bucles circulares
        if nombre_tabla == "personas":
            from personas_view import PersonasView
            self.cambiar_vista(PersonasView(self.page, self.cambiar_vista))
            return

        elif nombre_tabla == "especialidades":
            from especialidades_view import EspecialidadesView
            self.cambiar_vista(EspecialidadesView(self.page, self.cambiar_vista))
            return

        elif nombre_tabla == "docentes":
            from docentes_view import DocentesView
            self.cambiar_vista(DocentesView(self.page, self.cambiar_vista))
            return

        # 🟡 Si la tabla no tiene vista aún, mostrar un diálogo informativo
        dlg = ft.AlertDialog(
            title=ft.Text("Tabla seleccionada"),
            content=ft.Text(f"Has abierto la tabla: {nombre_tabla.capitalize()}"),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.dialog.close())
            ],
        )

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
