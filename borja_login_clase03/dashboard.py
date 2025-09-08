import flet as ft
import os
import sys
import subprocess

def main(page: ft.Page):
    page.window.width = 800
    page.window.height = 600
    page.window.resizable = True
    page.window.center()
    page.title = "Dashboard - Sistema de Ventas"

    def volver_inicio():
        page.window.close()
        ruta_main = os.path.join(os.path.dirname(__file__), "main.py")
        subprocess.Popen([sys.executable, ruta_main])

    page.add(
        ft.Column([
            ft.Text("🎯 DASHBOARD PRINCIPAL", size=30, weight=ft.FontWeight.BOLD, color="#2196F3"),
            ft.Divider(height=20),
            ft.Text("Bienvenido al sistema de gestión de ventas", size=18),
            ft.Divider(height=30),
            ft.Row([
                ft.ElevatedButton("Ver Reportes"),
                ft.ElevatedButton("Gestionar Productos"),
                ft.ElevatedButton("Clientes"),
            ], spacing=20),
            ft.Divider(height=30),
            ft.ElevatedButton("Volver al Inicio", on_click=lambda e: volver_inicio())
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    
    page.update()

if __name__ == "__main__":
    ft.app(target=main)

