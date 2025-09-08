import flet as ft

def main(page: ft.Page):
    page.window.width = 800
    page.window.height = 600
    page.window.resizable = True
    page.window.center()
    page.title = "Portada - Sistema de Ventas"
    
    page.add(
        ft.Column([
            ft.Text("🛍️ PORTADA DE COMPRAS", size=30, weight=ft.FontWeight.BOLD, color="#4CAF50"),
            ft.Divider(height=20),
            ft.Text("Sección de compras y procesamiento de pedidos", size=18),
            ft.Divider(height=30),
            ft.Row([
                ft.ElevatedButton("Nueva Compra"),
                ft.ElevatedButton("Historial"),
                ft.ElevatedButton("Carrito"),
            ], spacing=20),
            ft.Divider(height=30),
            ft.ElevatedButton("Volver al Inicio", on_click=lambda e: volver_inicio())
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    
    def volver_inicio():
        page.window.close()
        import subprocess
        import sys
        import os
        ruta_main = os.path.join(os.path.dirname(__file__), "main.py")
        subprocess.Popen([sys.executable, ruta_main])
    
    page.update()

if __name__ == "__main__":
    ft.app(target=main)