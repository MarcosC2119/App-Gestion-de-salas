import flet as ft
from flet import (
    Page, Text, TextField, ElevatedButton, Column, Row, Container,
    colors, padding, Image, Checkbox, DatePicker, TimePicker,
    ProgressBar, NavigationBar, NavigationBarDestination, Icon,
    FloatingActionButton, AppBar, icons, ScrollMode
)
from datetime import datetime, timedelta
from modules.auth import Auth
from modules.salas import GestorSalas, Sala, Reserva
from modules.qr import QRManager
from modules.capacitacion import GestorCapacitacion, Tutorial
from modules.styles import (
    COLORS, primary_button, secondary_button, card, section,
    text_field, title, subtitle, success_message, error_message,
    nav_button
)
import base64
import os
import sys
import json

def main(page: Page):
    # Configuración de la página
    page.title = "Gestión de Salas - UES"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window_width = 400
    page.window_height = 800
    page.window_resizable = False
    page.window_center()
    page.fonts = {
        "Poppins": "fonts/Poppins-Regular.ttf",
        "Poppins-Bold": "fonts/Poppins-Bold.ttf"
    }
    page.theme = ft.Theme(font_family="Poppins")
    
    # Estado de la aplicación
    page.session.set("user", None)
    page.session.set("current_view", "login")
    
    # Funciones de navegación
    def navigate_to(view_name):
        page.session.set("current_view", view_name)
        page.update()
    
    def show_login():
        page.clean()
        page.add(login_view)
    
    def show_dashboard():
        user = page.session.get("user")
        if user:
            if user["role"] == "docente":
                page.clean()
                page.add(docente_dashboard)
            elif user["role"] == "administrativo":
                page.clean()
                page.add(admin_dashboard)
        else:
            show_login()
    
    # Vista de login
    login_view = ft.Container(
        content=ft.Column(
            controls=[
                ft.Image(
                    src="assets/logo.png",
                    width=200,
                    height=200,
                    fit=ft.ImageFit.CONTAIN,
                ),
                ft.Text("Iniciar Sesión", size=24, weight=ft.FontWeight.BOLD),
                ft.TextField(
                    label="Correo electrónico",
                    hint_text="ejemplo@ues.edu.sv",
                    width=300,
                ),
                ft.TextField(
                    label="Contraseña",
                    hint_text="Ingrese su contraseña",
                    password=True,
                    width=300,
                ),
                ft.ElevatedButton(
                    text="Iniciar Sesión",
                    on_click=lambda e: handle_login(e),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.BLUE_600,
                    ),
                ),
                ft.TextButton(
                    text="¿Olvidó su contraseña?",
                    on_click=lambda e: navigate_to("recovery"),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        alignment=ft.alignment.center,
        padding=20,
    )
    
    # Manejador de login
    def handle_login(e):
        try:
            email = login_view.content.controls[2].value
            password = login_view.content.controls[3].value
            
            if not email or not password:
                page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text("Por favor ingrese su correo y contraseña"),
                        bgcolor=ft.colors.RED,
                    )
                )
                return
            
            # Aquí iría la lógica de autenticación real
            # Por ahora usamos datos de prueba
            if email == "docente@ues.edu.sv" and password == "docente123":
                page.session.set("user", {
                    "email": email,
                    "role": "docente",
                    "name": "Docente Ejemplo"
                })
                show_dashboard()
            elif email == "admin@ues.edu.sv" and password == "admin123":
                page.session.set("user", {
                    "email": email,
                    "role": "administrativo",
                    "name": "Admin Ejemplo"
                })
                show_dashboard()
            else:
                page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text("Credenciales inválidas"),
                        bgcolor=ft.colors.RED,
                    )
                )
        except Exception as ex:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"Error: {str(ex)}"),
                    bgcolor=ft.colors.RED,
                )
            )
    
    # Dashboard para docentes
    docente_dashboard = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Dashboard Docente", size=24, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton(
                    text="Reservar Sala",
                    on_click=lambda e: navigate_to("reservar"),
                ),
                ft.ElevatedButton(
                    text="Escanear QR",
                    on_click=lambda e: navigate_to("qr"),
                ),
                ft.ElevatedButton(
                    text="Capacitación",
                    on_click=lambda e: navigate_to("capacitacion"),
                ),
                ft.ElevatedButton(
                    text="Cerrar Sesión",
                    on_click=lambda e: handle_logout(e),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        alignment=ft.alignment.center,
        padding=20,
    )
    
    # Dashboard para administradores
    admin_dashboard = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Dashboard Administrativo", size=24, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton(
                    text="Gestionar Salas",
                    on_click=lambda e: navigate_to("gestionar"),
                ),
                ft.ElevatedButton(
                    text="Reportes",
                    on_click=lambda e: navigate_to("reportes"),
                ),
                ft.ElevatedButton(
                    text="Cerrar Sesión",
                    on_click=lambda e: handle_logout(e),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        alignment=ft.alignment.center,
        padding=20,
    )
    
    # Manejador de logout
    def handle_logout(e):
        page.session.set("user", None)
        show_login()
    
    # Inicializar la aplicación
    show_login()

# Ejecutar la aplicación
if __name__ == "__main__":
    ft.app(target=main) 