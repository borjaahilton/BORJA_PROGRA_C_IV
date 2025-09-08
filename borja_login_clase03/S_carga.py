import flet as ft
import sys
import time
import threading
import subprocess
import os

def main(page: ft.Page, tipo_operacion):
    # Configurar la ventana de carga (SOLO DESKTOP)
    page.window.width = 400
    page.window.height = 300
    page.window.resizable = False
    page.window.maximizable = False
    page.window.center()
    page.title = "Cargando..."
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Definir el mensaje según el tipo de operación
    mensajes = {
        "compra": "Procesando su compra...",
        "login": "Iniciando sesión..."
    }
    
    # Definir a qué archivo redirigir después de la carga
    redirecciones = {
        "compra": "Portada.py",
        "login": "logeo.py"
    }
    
    mensaje = mensajes.get(tipo_operacion, "Procesando...")
    archivo_destino = redirecciones.get(tipo_operacion, "main.py")
    
    # Crear elementos de la interfaz
    progress_ring = ft.ProgressRing(width=100, height=100, stroke_width=10)
    texto_carga = ft.Text(mensaje, size=20, weight=ft.FontWeight.BOLD)
    texto_estado = ft.Text("Por favor espere...", size=14)
    
    # Función para abrir el archivo destino
    def abrir_archivo_destino():
        ruta_destino = os.path.join(os.path.dirname(__file__), archivo_destino)
        if os.path.exists(ruta_destino):
            subprocess.Popen([sys.executable, ruta_destino])
        else:
            print(f"Archivo {archivo_destino} no encontrado")
    
    # Función para simular la carga
    def simular_carga():
        for i in range(1, 101):
            time.sleep(0.05)
            texto_estado.value = f"Progreso: {i}%"
            page.update()
        
        time.sleep(0.2)
        texto_estado.value = "¡Operación completada!"
        progress_ring.value = 1.0
        page.update()
        
        time.sleep(1)
        page.window.close()
        abrir_archivo_destino()
    
    # Iniciar la simulación de carga
    threading.Thread(target=simular_carga, daemon=True).start()
    
    # Agregar elementos a la página
    page.add(
        ft.Column([
            progress_ring,
            ft.Divider(height=20),
            texto_carga,
            ft.Divider(height=10),
            texto_estado
        ], 
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    
    page.update()

if __name__ == "__main__":
    tipo = sys.argv[1] if len(sys.argv) > 1 else "general"
    ft.app(target=lambda page: main(page, tipo))