import flet as ft
from conexion import ConexionDB
import hashlib
import getpass


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


class UsuariosView(ft.Container):
    def __init__(self, page: ft.Page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.db = ConexionDB()

        self.titulo = ft.Text("\U0001F465 Gestión de Usuarios", size=22, weight="bold")

        # Tabla de usuarios
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Usuario")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Rol")),
                ft.DataColumn(ft.Text("Activo")),
            ],
            rows=[],
            expand=True
        )

        # Form para crear usuario
        self.txt_usuario = ft.TextField(label="Usuario", width=250)
        self.txt_email = ft.TextField(label="Email", width=300)
        self.txt_password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=250)
        self.txt_rol = ft.Dropdown(width=150, value="user", options=[ft.dropdown.Option("user"), ft.dropdown.Option("admin")])

        self.btn_crear = ft.ElevatedButton("Crear usuario", on_click=self.crear_usuario)
        self.btn_volver = ft.ElevatedButton("\u2b05\ufe0f Volver", on_click=lambda e: self.volver_atras())
        self.lbl_mensaje = ft.Text("", color=ft.Colors.RED)

        self.content = ft.Column([
            ft.Row([self.titulo, self.btn_volver], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(self.tabla, expand=True, padding=10, border_radius=8, bgcolor=ft.Colors.BLUE_50),
            ft.Divider(),
            ft.Text("Crear nuevo usuario", weight="bold"),
            ft.Row([self.txt_usuario, self.txt_email, self.txt_password, self.txt_rol], alignment=ft.MainAxisAlignment.START),
            ft.Row([self.btn_crear, self.lbl_mensaje], alignment=ft.MainAxisAlignment.START),
        ], spacing=10, expand=True)

        # Cargar usuarios al iniciar
        self.cargar_usuarios()

    def cargar_usuarios(self):
        conexion = self.db.conectar()
        if not conexion:
            self.lbl_mensaje.value = "Error al conectar con la base de datos"
            self.lbl_mensaje.color = ft.Colors.RED
            self.update()
            return

        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT usuario_id, nombre_usuario, email, rol, activo FROM usuarios")
            filas = cursor.fetchall()

            self.tabla.rows.clear()
            for fila in filas:
                self.tabla.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(fila[0]))),
                        ft.DataCell(ft.Text(fila[1] or "")),
                        ft.DataCell(ft.Text(fila[2] or "")),
                        ft.DataCell(ft.Text(fila[3] or "user")),
                        ft.DataCell(ft.Text(str(fila[4]))),
                    ])
                )
            self.page.update()
        except Exception as e:
            # intentar también la tabla singular 'usuario'
            try:
                cursor.execute("SELECT usuario_id, nombre_usuario, email, rol, activo FROM usuario")
                filas = cursor.fetchall()
                self.tabla.rows.clear()
                for fila in filas:
                    self.tabla.rows.append(
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(str(fila[0]))),
                            ft.DataCell(ft.Text(fila[1] or "")),
                            ft.DataCell(ft.Text(fila[2] or "")),
                            ft.DataCell(ft.Text(fila[3] or "user")),
                            ft.DataCell(ft.Text(str(fila[4]))),
                        ])
                    )
                self.page.update()
                return
            except Exception as e2:
                self.lbl_mensaje.value = f"Error al cargar usuarios: {e} / {e2}"
                self.lbl_mensaje.color = ft.Colors.RED
                self.update()
        finally:
            cursor.close()
            self.db.cerrar(conexion)

    def crear_usuario(self, e):
        nombre = self.txt_usuario.value.strip() if self.txt_usuario.value else ""
        email = self.txt_email.value.strip() if self.txt_email.value else None
        pwd = self.txt_password.value if self.txt_password.value else ""
        rol = self.txt_rol.value or 'user'

        if not nombre or not pwd:
            self.lbl_mensaje.value = "Usuario y contraseña son obligatorios"
            self.lbl_mensaje.color = ft.Colors.RED
            self.update()
            return

        hashed = hash_password(pwd)

        conexion = self.db.conectar()
        if not conexion:
            self.lbl_mensaje.value = "Error al conectar con la base de datos"
            self.lbl_mensaje.color = ft.Colors.RED
            self.update()
            return

        cursor = conexion.cursor()
        try:
            # intentar tabla plural primero
            try:
                cursor.execute("INSERT INTO usuarios (nombre_usuario, hashed_pass, email, rol) VALUES (%s,%s,%s,%s)", (nombre, hashed, email, rol))
                conexion.commit()
            except Exception:
                # intentar tabla singular
                cursor.execute("INSERT INTO usuario (nombre_usuario, hashed_pass, email, rol) VALUES (%s,%s,%s,%s)", (nombre, hashed, email, rol))
                conexion.commit()

            self.lbl_mensaje.value = f"Usuario '{nombre}' creado"
            self.lbl_mensaje.color = ft.Colors.GREEN
            # limpiar campos
            self.txt_usuario.value = ""
            self.txt_email.value = ""
            self.txt_password.value = ""
            self.page.update()
            # recargar tabla
            self.cargar_usuarios()
        except Exception as e:
            self.lbl_mensaje.value = f"Error al crear usuario: {e}"
            self.lbl_mensaje.color = ft.Colors.RED
            self.update()
        finally:
            cursor.close()
            self.db.cerrar(conexion)
