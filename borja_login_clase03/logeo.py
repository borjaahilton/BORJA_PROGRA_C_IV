import flet as ft
import time

def main(page: ft.Page):
    # Configuración de la página
    page.title = "Inicio de Sesión - Sistema de Ventas"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.bgcolor = "#f8f9fa"
    
    # Variables de estado
    is_loading = False
    
    def iniciar_sesion(e):
        nonlocal is_loading
        
        if is_loading:
            return
            
        usuario = txt_usuario.value.strip()
        password = txt_password.value.strip()
        
        if not usuario or not password:
            mostrar_mensaje("Por favor complete todos los campos", "error")
            animar_logo()
            return
        
        # Mostrar loading
        is_loading = True
        btn_ingresar.content.controls[0].visible = False
        btn_ingresar.content.controls[1].visible = False
        progress_ring.visible = True
        btn_ingresar.disabled = True
        page.update()
        
        # Simular proceso de login
        def proceso_login():
            time.sleep(2)  # Simular verificación
            
            # Aquí iría la lógica real de autenticación
            if usuario == "admin" and password == "admin123":
                mostrar_mensaje("¡Login exitoso! Redirigiendo...", "success")
                time.sleep(1)
                # Redirigir a dashboard
                redirigir_dashboard()
            else:
                mostrar_mensaje("Credenciales incorrectas. Intente nuevamente.", "error")
            
            # Ocultar loading
            is_loading = False
            btn_ingresar.content.controls[0].visible = True
            btn_ingresar.content.controls[1].visible = True
            progress_ring.visible = False
            btn_ingresar.disabled = False
            page.update()
        
        import threading
        threading.Thread(target=proceso_login, daemon=True).start()
    
    # Animaciones
    def animar_campo(campo, focused):
        campo.border_width = 3 if focused else 1
        campo.update()
    
    def animar_boton(e):
        e.control.style.elevation = 12 if e.data == "true" else 8
        e.control.style.bgcolor = ft.Colors.BLUE_800 if e.data == "true" else ft.Colors.BLUE_700
        e.control.update()
    
    def animar_logo():
        logo.scale = ft.Scale(1.1)
        logo.update()
        time.sleep(0.1)
        logo.scale = ft.Scale(1.0)
        logo.update()
    
    def mostrar_mensaje(mensaje, tipo="error"):
        color = ft.Colors.RED_700 if tipo == "error" else ft.Colors.BLUE_700 if tipo == "info" else ft.Colors.GREEN_700
        bgcolor = ft.Colors.RED_100 if tipo == "error" else ft.Colors.BLUE_100 if tipo == "info" else ft.Colors.GREEN_100
        
        lbl_mensaje.bgcolor = bgcolor
        lbl_mensaje.content.value = mensaje
        lbl_mensaje.content.color = color
        lbl_mensaje.opacity = 1
        lbl_mensaje.update()
        
        # Ocultar mensaje después de 3 segundos
        def ocultar_mensaje():
            time.sleep(3)
            lbl_mensaje.opacity = 0
            lbl_mensaje.update()
        
        import threading
        threading.Thread(target=ocultar_mensaje, daemon=True).start()
        
    
    
    # Controles con diseño profesional - ICONOS CORREGIDOS
    logo = ft.Container(
        content=ft.Icon(
            ft.Icons.SHOPPING_CART,
            size=80,
            color=ft.Colors.BLUE_700
        ),
        animate_scale=ft.Animation(600, ft.AnimationCurve.BOUNCE_OUT)
    )
    
    titulo = ft.Text(
        "SISTEMA DE VENTAS",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_900,
        text_align=ft.TextAlign.CENTER
    )
    
    subtitulo = ft.Text(
        "Ingrese sus credenciales para continuar",
        size=16,
        color=ft.Colors.GREY_600,
        text_align=ft.TextAlign.CENTER
    )
    
    txt_usuario = ft.TextField(
        label="Usuario",
        prefix_icon=ft.Icons.PERSON,
        border_radius=15,
        border_color=ft.Colors.BLUE_GREY_200,
        focused_border_color=ft.Colors.BLUE_700,
        cursor_color=ft.Colors.BLUE_700,
        text_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_800),
        width=320,
        height=55,
        on_focus=lambda e: animar_campo(txt_usuario, True),
        on_blur=lambda e: animar_campo(txt_usuario, False)
    )
    
    txt_password = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True,
        border_radius=15,
        border_color=ft.Colors.BLUE_GREY_200,
        focused_border_color=ft.Colors.BLUE_700,
        cursor_color=ft.Colors.BLUE_700,
        text_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_800),
        width=320,
        height=55,
        on_focus=lambda e: animar_campo(txt_password, True),
        on_blur=lambda e: animar_campo(txt_password, False),
        on_submit=lambda e: iniciar_sesion(e)
    )
    
    btn_ingresar = ft.ElevatedButton(
        content=ft.Row([
            ft.Icon(ft.Icons.LOGIN, color=ft.Colors.WHITE),
            ft.Text("INGRESAR", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        width=320,
        height=55,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=15),
            overlay_color=ft.Colors.BLUE_900,
            animation_duration=300,
            elevation=8,
            shadow_color=ft.Colors.BLUE_300
        ),
        on_click=iniciar_sesion,
        on_hover=animar_boton
    )
    
    progress_ring = ft.ProgressRing(
        width=30,
        height=30,
        stroke_width=3,
        color=ft.Colors.WHITE,
        visible=False
    )
    
    lbl_mensaje = ft.Container(
        content=ft.Text(
            "",
            size=14,
            color=ft.Colors.WHITE,
            text_align=ft.TextAlign.CENTER
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=12),
        border_radius=10,
        animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        opacity=0
    )
    
    link_olvide = ft.TextButton(
        content=ft.Text(
            "¿Olvidaste tu contraseña?",
            size=14,
            color=ft.Colors.BLUE_600,
            weight=ft.FontWeight.W_500
        ),
        on_click=lambda e: mostrar_mensaje("Función en desarrollo", "info")
    )
    
    link_registro = ft.TextButton(
        content=ft.Text(
            "Crear una cuenta nueva",
            size=14,
            color=ft.Colors.GREEN_600,
            weight=ft.FontWeight.W_500
        ),
        on_click=lambda e: mostrar_mensaje("Registro en desarrollo", "info")
    )
    


    def redirigir_dashboard():
        if not page.web:
            page.window.close()
            # Aquí abrirías Dashboard.py
            mostrar_mensaje("Redirección a Dashboard (modo desktop)", "info")
        else:
            # En web, cambiarías el contenido
            mostrar_mensaje("Redirección a Dashboard (modo web)", "info")
    
    # Construir interfaz
    card_login = ft.Container(
        content=ft.Column([
            ft.Container(logo, alignment=ft.alignment.center),
            ft.Container(titulo, padding=ft.padding.only(bottom=5)),
            ft.Container(subtitulo, padding=ft.padding.only(bottom=30)),
            
            ft.Container(txt_usuario, padding=ft.padding.only(bottom=15)),
            ft.Container(txt_password, padding=ft.padding.only(bottom=20)),
            
            ft.Container(
                content=btn_ingresar,
                alignment=ft.alignment.center
            ),
            
            ft.Container(
                content=ft.Row([
                    progress_ring,
                    lbl_mensaje
                ], alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.padding.only(top=20)
            ),
            
            ft.Container(
                content=ft.Row([
                    link_olvide,
                    ft.VerticalDivider(width=20, color=ft.Colors.TRANSPARENT),
                    link_registro
                ], alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.padding.only(top=25)
            )
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        
        width=400,
        padding=40,
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLUE_GREY_100,
            offset=ft.Offset(0, 4)
        ),
        animate_scale=ft.Animation(600, ft.AnimationCurve.BOUNCE_OUT)
    )
    
    # Layout principal con gradiente de fondo
    layout_principal = ft.Container(
        content=ft.Column([
            card_login
        ], alignment=ft.MainAxisAlignment.CENTER),
        
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.BLUE_50, ft.Colors.INDIGO_100]
        ),
        expand=True,
        padding=20
    )
    
    page.add(layout_principal)
    
    # Animación inicial
    def animar_entrada():
        time.sleep(0.1)
        card_login.scale = ft.Scale(0.9)
        card_login.opacity = 0
        page.update()
        
        time.sleep(0.1)
        card_login.scale = ft.Scale(1.0)
        card_login.opacity = 1
        page.update()
    
    animar_entrada()

if __name__ == "__main__":
    ft.app(target=main)