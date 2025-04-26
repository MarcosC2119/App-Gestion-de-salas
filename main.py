import flet as ft
from flet import (
    Page, Text, TextField, ElevatedButton, Column, Row, 
    Container, colors, padding, margin, Image, Checkbox, 
    DatePicker, TimePicker, ProgressBar, alignment
)
from datetime import datetime, timedelta
from modules.auth import Auth
from modules.salas import GestorSalas, Sala, Reserva
from modules.qr import QRManager
from modules.capacitacion import GestorCapacitacion, Tutorial
from modules.reservations import cancelar_reserva, cancelar_reserva_admin
from modules.styles import (
    COLORS, primary_button, secondary_button, card, section,
    text_field, title, subtitle, caption, success_message, 
    error_message, nav_button, divider_with_text, SPACING
)
import base64

def main(page: Page):
    page.title = "Sistema de Gestión de Salas"
    page.theme_mode = "light"
    page.padding = 0
    page.bgcolor = COLORS["background"]
    page.window_width = 1200
    page.window_height = 800
    page.window_resizable = True
    page.window_maximized = True

    # Instancias de los gestores
    gestor_salas = GestorSalas()
    gestor_capacitacion = GestorCapacitacion()
    usuario_actual = None
    rol_actual = None

    # Componentes de la interfaz de login
    email_field = text_field(
        label="Correo electrónico",
        hint_text="Ingrese su correo electrónico",
        prefix_icon=ft.Icons.EMAIL,
        width=400
    )
    password_field = text_field(
        label="Contraseña",
        hint_text="Ingrese su contraseña",
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK,
        width=400
    )

    # Banners de mensajes
    error_banner = error_message("")
    error_banner.visible = False
    success_banner = success_message("")
    success_banner.visible = False

    def show_error(message: str):
        error_banner.visible = True
        page.update()

    def show_success(message: str):
        success_banner.visible = True
        page.update()

    def back_button():
        """Crea un botón de retroceso estándar"""
        return Container(
            content=Row(
                [
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color=COLORS["primary"],
                        icon_size=20,
                        on_click=lambda e: handle_back(),
                        tooltip="Volver"
                    ),
                    Text("Volver", color=COLORS["primary"]),
                ],
                spacing=SPACING["xs"],
            ),
            padding=padding.only(left=SPACING["lg"], top=SPACING["md"], bottom=SPACING["md"]),
        )

    def page_header(title_text: str, subtitle_text: str = None):
        """Crea un encabezado estándar para las páginas"""
        return Container(
            content=Column(
                [
                    title(title_text),
                    caption(subtitle_text) if subtitle_text else Container(),
                ],
                spacing=SPACING["xs"],
            ),
            padding=padding.only(
                left=SPACING["lg"],
                right=SPACING["lg"],
                bottom=SPACING["lg"]
            ),
        )

    def handle_back():
        """Maneja la navegación hacia atrás según el rol del usuario"""
        if rol_actual == "docente":
            show_docente_dashboard()
        elif rol_actual == "administrativo":
            show_admin_dashboard()
        else:
            show_login()

    def login_clicked(e):
        nonlocal usuario_actual, rol_actual
        success, role = Auth.login(email_field.value, password_field.value)
        if success:
            error_banner.visible = False
            usuario_actual = email_field.value
            rol_actual = role
            if role == "docente":
                show_docente_dashboard()
            elif role == "administrativo":
                show_admin_dashboard()
        else:
            show_error("Credenciales incorrectas")

    def show_reserva_form():
        page.clean()
        page.add(back_button())  # Agregar botón de retroceso
        
        # Componentes del formulario
        fecha_picker = DatePicker()
        hora_inicio_picker = TimePicker()
        hora_fin_picker = TimePicker()
        capacidad_field = text_field("Capacidad mínima", width=300)
        proyector_check = Checkbox(label="Requiere proyector")
        pizarra_check = Checkbox(label="Requiere pizarra digital")
        accesible_check = Checkbox(label="Requiere accesibilidad")
        
        def buscar_salas(e):
            try:
                fecha = fecha_picker.value
                hora_inicio = hora_inicio_picker.value
                hora_fin = hora_fin_picker.value
                capacidad = int(capacidad_field.value) if capacidad_field.value else 0
                
                if not all([fecha, hora_inicio, hora_fin]):
                    show_error("Por favor complete todos los campos de fecha y hora")
                    return
                
                fecha_inicio = datetime.combine(fecha, hora_inicio)
                fecha_fin = datetime.combine(fecha, hora_fin)
                
                salas_disponibles = gestor_salas.buscar_salas_disponibles(
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    capacidad_min=capacidad,
                    requiere_proyector=proyector_check.value,
                    requiere_pizarra=pizarra_check.value,
                    requiere_accesible=accesible_check.value
                )
                
                mostrar_resultados(salas_disponibles, fecha_inicio, fecha_fin)
                
            except ValueError:
                show_error("Por favor ingrese valores válidos")

        def mostrar_resultados(salas: list[Sala], fecha_inicio: datetime, fecha_fin: datetime):
            resultados_container.controls.clear()
            
            if not salas:
                resultados_container.controls.append(
                    error_message("No se encontraron salas disponibles")
                )
            else:
                for sala in salas:
                    card_content = Column([
                        subtitle(sala.nombre),
                        Text(f"Capacidad: {sala.capacidad} personas"),
                        Text(f"Proyector: {'Sí' if sala.tiene_proyector else 'No'}"),
                        Text(f"Pizarra digital: {'Sí' if sala.tiene_pizarra_digital else 'No'}"),
                        Text(f"Accesible: {'Sí' if sala.es_accesible else 'No'}"),
                        primary_button(
                            "Reservar",
                            on_click=lambda e, s=sala: reservar_sala(s, fecha_inicio, fecha_fin)
                        )
                    ])
                    resultados_container.controls.append(card(card_content))
            
            page.update()

        def reservar_sala(sala: Sala, fecha_inicio: datetime, fecha_fin: datetime):
            reserva = gestor_salas.crear_reserva(
                sala_id=sala.id,
                usuario_email=usuario_actual,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
            
            if reserva:
                # Generar QR
                qr_bytes = QRManager.generar_qr(
                    reserva_id=reserva.id,
                    sala_id=sala.id,
                    usuario_email=usuario_actual,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin
                )
                
                # Mostrar QR
                qr_base64 = base64.b64encode(qr_bytes).decode()
                qr_image = Image(
                    src_base64=qr_base64,
                    width=200,
                    height=200
                )
                
                page.clean()
                page.add(
                    Column([
                        title("¡Reserva exitosa!"),
                        card(Column([
                            Text(f"Sala: {sala.nombre}"),
                            Text(f"Fecha: {fecha_inicio.strftime('%d/%m/%Y')}"),
                            Text(f"Hora: {fecha_inicio.strftime('%H:%M')} - {fecha_fin.strftime('%H:%M')}"),
                            qr_image,
                            primary_button(
                                "Volver al panel",
                                on_click=lambda e: show_docente_dashboard()
                            )
                        ]))
                    ], alignment=ft.MainAxisAlignment.CENTER)
                )
            else:
                show_error("No se pudo realizar la reserva")

        # Contenedor de resultados
        resultados_container = Column(scroll=ft.ScrollMode.AUTO)
        
        page.add(
            Column([
                title("Reservar Sala"),
                card(Column([
                    fecha_picker,
                    Row([
                        Column([
                            Text("Hora inicio:"),
                            hora_inicio_picker
                        ]),
                        Column([
                            Text("Hora fin:"),
                            hora_fin_picker
                        ])
                    ]),
                    capacidad_field,
                    proyector_check,
                    pizarra_check,
                    accesible_check,
                    primary_button("Buscar Salas", on_click=buscar_salas)
                ])),
                resultados_container
            ], spacing=20)
        )

    def show_mis_reservas():
        page.clean()
        page.add(back_button())  # Agregar botón de retroceso
        reservas = gestor_salas.obtener_reservas_usuario(usuario_actual)
        
        if not reservas:
            page.add(card(Text("No tienes reservas activas")))
            return
        
        reservas_container = Column(scroll=ft.ScrollMode.AUTO)
        
        for reserva in reservas:
            sala = next(s for s in gestor_salas.salas if s.id == reserva.sala_id)
            card_content = Column([
                subtitle(sala.nombre),
                Text(f"Fecha: {reserva.fecha_inicio.strftime('%d/%m/%Y')}"),
                Text(f"Hora: {reserva.fecha_inicio.strftime('%H:%M')} - {reserva.fecha_fin.strftime('%H:%M')}"),
                Text(f"Estado: {reserva.estado}"),
                Row([
                    primary_button(
                        "Cancelar",
                        on_click=lambda e, r=reserva: handle_cancelar_reserva(r)
                    ) if reserva.estado != 'cancelada' else None
                ])
            ])
            reservas_container.controls.append(card(card_content))
        
        page.add(
            Column([
                title("Mis Reservas"),
                primary_button("Volver", on_click=lambda e: show_docente_dashboard()),
                reservas_container
            ])
        )

    def handle_cancelar_reserva(reserva):
        """Maneja la cancelación de una reserva"""
        success, message = cancelar_reserva(reserva.id, usuario_actual)
        if success:
            show_success(message)
            show_mis_reservas()  # Recargar la vista
        else:
            show_error(message)

    def show_capacitacion():
        page.clean()
        page.add(back_button())  # Agregar botón de retroceso
        tutoriales = gestor_capacitacion.obtener_tutoriales_pendientes(usuario_actual)
        progreso = gestor_capacitacion.obtener_progreso(usuario_actual)
        
        page.add(
            Column([
                title("Capacitación"),
                card(Column([
                    Text(f"Progreso general: {progreso:.1f}%"),
                    ProgressBar(value=progreso/100, width=300),
                ])),
                *[card(Column([
                    subtitle(t.titulo),
                    Text(t.descripcion),
                    Text(f"Duración: {t.duracion}"),
                    Row([
                        primary_button(
                            "Ver",
                            on_click=lambda e, t=t: ver_tutorial(t)
                        ),
                        primary_button(
                            "Marcar como completado",
                            on_click=lambda e, t=t: marcar_completado(t)
                        )
                    ])
                ])) for t in tutoriales],
                primary_button("Volver", on_click=lambda e: show_docente_dashboard())
            ])
        )

    def ver_tutorial(tutorial: Tutorial):
        # En una implementación real, esto abriría el video o documento
        show_success(f"Abriendo {tutorial.titulo}...")

    def marcar_completado(tutorial: Tutorial):
        if gestor_capacitacion.marcar_completado(usuario_actual, tutorial.id):
            show_success(f"¡{tutorial.titulo} marcado como completado!")
            show_capacitacion()
        else:
            show_error("No se pudo marcar como completado")

    def show_docente_dashboard():
        page.clean()
        page.add(
            Column([
                title("Panel del Docente"),
                Row([
                    nav_button("Reservar Sala", ft.icons.ADD, lambda e: show_reserva_form()),
                    nav_button("Mis Reservas", ft.icons.CALENDAR_MONTH, lambda e: show_mis_reservas()),
                    nav_button("Capacitación", ft.icons.SCHOOL, lambda e: show_capacitacion()),
                    nav_button("Cerrar Sesión", ft.icons.LOGOUT, lambda e: show_login())
                ], wrap=True),
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    def show_admin_dashboard():
        page.clean()
        page.add(
            Column([
                title("Panel del Administrador"),
                Row([
                    nav_button("Gestionar Reservas", ft.icons.EDIT_CALENDAR, lambda e: show_gestion_reservas()),
                    nav_button("Estadísticas", ft.icons.ANALYTICS, lambda e: show_estadisticas()),
                    nav_button("Capacitación", ft.icons.SCHOOL, lambda e: show_capacitacion()),
                    nav_button("Cerrar Sesión", ft.icons.LOGOUT, lambda e: show_login())
                ], wrap=True),
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    def show_gestion_reservas():
        page.clean()
        page.add(back_button())  # Agregar botón de retroceso
        todas_reservas = gestor_salas.reservas
        
        reservas_container = Column(scroll=ft.ScrollMode.AUTO)
        
        for reserva in todas_reservas:
            sala = next(s for s in gestor_salas.salas if s.id == reserva.sala_id)
            card_content = Column([
                subtitle(sala.nombre),
                Text(f"Usuario: {reserva.usuario_email}"),
                Text(f"Fecha: {reserva.fecha_inicio.strftime('%d/%m/%Y')}"),
                Text(f"Hora: {reserva.fecha_inicio.strftime('%H:%M')} - {reserva.fecha_fin.strftime('%H:%M')}"),
                Text(f"Estado: {reserva.estado}"),
                Row([
                    primary_button(
                        "Cancelar",
                        on_click=lambda e, r=reserva: handle_cancelar_reserva_admin(r)
                    ) if reserva.estado != 'cancelada' else None
                ])
            ])
            reservas_container.controls.append(card(card_content))
        
        page.add(
            Column([
                title("Gestión de Reservas"),
                primary_button("Volver", on_click=lambda e: show_admin_dashboard()),
                reservas_container
            ])
        )

    def handle_cancelar_reserva_admin(reserva):
        """Maneja la cancelación de una reserva por un administrador"""
        success, message = cancelar_reserva_admin(reserva.id)
        if success:
            show_success(message)
            show_gestion_reservas()  # Recargar la vista
        else:
            show_error(message)

    def show_estadisticas():
        page.clean()
        page.add(back_button())  # Agregar botón de retroceso
        
        # Estadísticas básicas
        total_reservas = len(gestor_salas.reservas)
        reservas_activas = len([r for r in gestor_salas.reservas if r.estado != 'cancelada'])
        salas_mas_utilizadas = {}
        
        for reserva in gestor_salas.reservas:
            if reserva.estado != 'cancelada':
                sala_id = reserva.sala_id
                salas_mas_utilizadas[sala_id] = salas_mas_utilizadas.get(sala_id, 0) + 1
        
        salas_ordenadas = sorted(salas_mas_utilizadas.items(), key=lambda x: x[1], reverse=True)
        
        page.add(
            Column([
                title("Estadísticas"),
                card(Column([
                    subtitle("Reservas"),
                    Text(f"Total de reservas: {total_reservas}"),
                    Text(f"Reservas activas: {reservas_activas}"),
                    subtitle("Salas más utilizadas"),
                    *[Text(f"{next(s for s in gestor_salas.salas if s.id == sala_id).nombre}: {count} reservas")
                      for sala_id, count in salas_ordenadas[:3]]
                ])),
                primary_button("Volver", on_click=lambda e: show_admin_dashboard())
            ])
        )

    def show_login():
        nonlocal usuario_actual, rol_actual
        usuario_actual = None
        rol_actual = None
        page.clean()
        
        # Contenedor de login centrado
        login_card = card(
            Column(
                [
                    Container(
                        content=Image(
                            src="/logo.png",
                            width=120,
                            height=120,
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        alignment=alignment.center,
                    ),
                    title("Bienvenido"),
                    caption("Ingrese sus credenciales para continuar"),
                    email_field,
                    password_field,
                    primary_button(
                        text="Iniciar sesión",
                        icon=ft.Icons.LOGIN,
                        width=400,
                        on_click=login_clicked
                    ),
                    Container(height=20),  # Espaciador
                    secondary_button(
                        "¿Olvidó su contraseña?",
                        on_click=lambda e: print("Recuperar contraseña"),
                        width=300,
                        icon=ft.Icons.HELP
                    ),
                ],
                spacing=SPACING["md"],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=400,
        )

        # Contenedor principal centrado
        main_container = Container(
            content=Column(
                [
                    login_card,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            margin=margin.symmetric(vertical=100),
            alignment=alignment.center,
        )

        page.add(main_container)

    # Iniciar con la pantalla de login
    show_login()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets") 