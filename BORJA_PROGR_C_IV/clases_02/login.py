import flet as ft
def main(page: ft.Page):
    page.window.width = 500
    page.window.height = 200
    page.window.resizable = False
    page.window.maximizable = False
    page.window.center()
    page.title = "segunda clases - programacion concurrente"

    btn_compra = ft.ElevatedButton(
        text= "Comprar",
        width =200,
        height =100,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            bgcolor="#6ee02b",
            color="white"
        )
        
    )

    btn_login = ft.ElevatedButton(
        text="iniciar sesion",
        width=200,
        height=100,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            bgcolor="#18e418",
            color="red"
        )
    )

    fila_botones = ft.Row(
        controls=[btn_compra, btn_login],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )
    
    page.add(
        ft.Divider(height=6, color="transparent"),
        fila_botones
    )
    page.update()
ft.app(target=main)