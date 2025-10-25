import flet as ft
from conexion import ConexionDB

class EditarPersonaView(ft.Container):
    def __init__(self, page, volver_atras, persona_id):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.persona_id = persona_id
        self.db = ConexionDB()

        titulo = ft.Text(f"✏️ Editar Persona #{persona_id}", size=22, weight="bold")

        # Campos (rellenados desde DB)
        self.txt_nombre = ft.TextField(label="Nombres")
        self.txt_apellido = ft.TextField(label="Apellidos")
        self.txt_dni = ft.TextField(label="DNI")
        self.txt_telefono = ft.TextField(label="Teléfono")

        btn_guardar = ft.ElevatedButton("Guardar", on_click=self.guardar)
        btn_volver = ft.ElevatedButton("Volver", on_click=lambda e: self.volver_atras())

        self.content = ft.Column([
            titulo,
            ft.Row([btn_volver, btn_guardar], alignment=ft.MainAxisAlignment.START),
            ft.Divider(),
            ft.Column([self.txt_nombre, self.txt_apellido, self.txt_dni, self.txt_telefono], spacing=10)
        ], expand=True, scroll=ft.ScrollMode.AUTO)

        # Cargar datos
        self.cargar_datos()

    def cargar_datos(self):
        conexion = self.db.conectar()
        if not conexion:
            self.page.snack_bar = ft.SnackBar(ft.Text("Error al conectar con la base de datos"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        cur = conexion.cursor()
        try:
            cur.execute("SELECT nombres, apellidos, numero_documento, telefono FROM personas WHERE persona_id = %s", (self.persona_id,))
            row = cur.fetchone()
            if row:
                self.txt_nombre.value = row[0] or ""
                self.txt_apellido.value = row[1] or ""
                self.txt_dni.value = row[2] or ""
                self.txt_telefono.value = row[3] or ""
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("No se encontró la persona"))
                self.page.snack_bar.open = True
            self.page.update()
        except Exception as e:
            print(f"❌ Error al cargar datos de persona: {e}")
        finally:
            self.db.cerrar(conexion)

    def guardar(self, e):
        campos = {
            'nombres': self.txt_nombre.value.strip(),
            'apellidos': self.txt_apellido.value.strip(),
            'numero_documento': self.txt_dni.value.strip(),
            'telefono': self.txt_telefono.value.strip(),
        }
        # Eliminar claves vacías para no sobrescribir con NULL
        campos = {k: v for k, v in campos.items() if v != ""}

        if not campos:
            self.page.snack_bar = ft.SnackBar(ft.Text("No hay cambios para guardar"))
            self.page.snack_bar.open = True
            self.page.update()
            return

        res = self.db.actualizar_persona(self.persona_id, campos)
        print(f"[DEBUG] EditarPersonaView.guardar -> res: {res}")
        if res.get('status'):
            self.page.snack_bar = ft.SnackBar(ft.Text("Persona actualizada"))
            self.page.snack_bar.open = True
            # Volver al listado
            self.volver_atras()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar: {res.get('mensaje')}"))
            self.page.snack_bar.open = True
        self.page.update()
