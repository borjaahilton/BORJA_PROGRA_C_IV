import flet as ft

USUARIO = "chamoy"
PASSWORD = "1234"
CUPOS_INICIALES = 5

def main(page: ft.Page):
    page.title = "Reserva Guía Turística"
    page.bgcolor = "#e3f2fd"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

   
    if not hasattr(main, "cupos"):
        main.cupos = CUPOS_INICIALES
    if not hasattr(main, "reservas"):
        main.reservas = []

   
    usuario = ft.TextField(label="Usuario", width=250)
    contrasena = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=250)
    mensaje_login = ft.Text("", color="red")

    def mostrar_login():
        usuario.value = ""
        contrasena.value = ""
        mensaje_login.value = ""
        page.clean()
        page.add(
            ft.Column([
                ft.Text("Iniciar sesión", size=28, weight="bold", color="blue"),
                usuario,
                contrasena,
                ft.ElevatedButton("Ingresar", on_click=validar_login),
                mensaje_login
            ], alignment="center", horizontal_alignment="center", spacing=18)
        )

    def validar_login(e):
        if usuario.value == USUARIO and contrasena.value == PASSWORD:
            mostrar_reserva()
        else:
            mensaje_login.value = "Usuario o contraseña incorrectos"
            page.update()

    
    nombre = ft.TextField(label="Nombre del turista", width=250)
    fecha = ft.TextField(label="Fecha de reserva (dd/mm/aaaa)", width=250)
    mensaje_reserva = ft.Text("", color="red")
    cupos_text = ft.Text(f"Cupos disponibles: {main.cupos}", size=22, color="green")

    def mostrar_reserva():
        nombre.value = ""
        fecha.value = ""
        mensaje_reserva.value = ""
        cupos_text.value = f"Cupos disponibles: {main.cupos}"
        page.clean()
        page.add(
            ft.Column([
                ft.Text("Reserva de Guía Turística", size=28, weight="bold", color="blue"),
                cupos_text,
                nombre,
                fecha,
                ft.ElevatedButton("Reservar cupo", on_click=reservar),
                mensaje_reserva,
                ft.ElevatedButton("Cerrar sesión", on_click=lambda e: mostrar_login(), style=ft.ButtonStyle(bgcolor="red", color="white"))
            ], alignment="center", horizontal_alignment="center", spacing=18)
        )

    def reservar(e):
        if not nombre.value or not fecha.value:
            mensaje_reserva.value = "Completa todos los campos."
            mensaje_reserva.color = "red"
        elif main.cupos > 0:
            main.cupos -= 1
            main.reservas.append((nombre.value, fecha.value))
            cupos_text.value = f"Cupos disponibles: {main.cupos}"
            mensaje_reserva.value = f"Reserva exitosa para {nombre.value} el {fecha.value}."
            mensaje_reserva.color = "blue"
            nombre.value = ""
            fecha.value = ""
        else:
            mensaje_reserva.value = "No hay cupos disponibles."
            mensaje_reserva.color = "red"
        page.update()



    mostrar_login()

if __name__ == "__main__":
    ft.app(target=main)