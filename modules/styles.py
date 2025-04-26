import flet as ft
from flet import colors, padding, border_radius, ButtonStyle, TextStyle

# Paleta de colores profesional
COLORS = {
    "primary": "#1A237E",  # Azul profundo
    "primary_light": "#534BAE",
    "secondary": "#0277BD",  # Azul acento
    "background": "#F5F7FA",  # Gris claro profesional
    "surface": "#FFFFFF",
    "text": {
        "primary": "#1F2937",  # Gris oscuro para texto principal
        "secondary": "#6B7280",  # Gris medio para texto secundario
        "white": "#FFFFFF"
    },
    "error": "#DC2626",
    "success": "#059669",
    "warning": "#D97706",
    "info": "#2563EB"
}

# Tipografía
TYPOGRAPHY = {
    "h1": {"size": 32, "weight": "bold", "color": COLORS["text"]["primary"]},
    "h2": {"size": 24, "weight": "bold", "color": COLORS["text"]["primary"]},
    "h3": {"size": 20, "weight": "w600", "color": COLORS["text"]["primary"]},
    "body": {"size": 16, "weight": "normal", "color": COLORS["text"]["primary"]},
    "caption": {"size": 14, "weight": "normal", "color": COLORS["text"]["secondary"]},
    "button": {"size": 16, "weight": "w500", "color": COLORS["text"]["white"]}
}

# Espaciado y dimensiones
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32
}

# Bordes y sombras
BORDER_RADIUS_SM = 4
BORDER_RADIUS_MD = 8
BORDER_RADIUS_LG = 12
BORDER_RADIUS_XL = 16

# Estilos de botones
def primary_button(text: str, on_click=None, width=None, icon=None):
    return ft.ElevatedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        width=width,
        style=ButtonStyle(
            bgcolor={"": COLORS["primary"], "hovered": COLORS["primary_light"]},
            color=COLORS["text"]["white"],
            padding=padding.all(16),
            shadow_color=COLORS["primary"],
            elevation={"": 1, "hovered": 2},
        ),
    )

def secondary_button(text: str, on_click=None, width=None, icon=None):
    return ft.OutlinedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        width=width,
        style=ButtonStyle(
            bgcolor={"": COLORS["surface"], "hovered": ft.colors.with_opacity(0.05, COLORS["primary"])},
            color=COLORS["primary"],
            padding=padding.all(16),
            side=ft.BorderSide(1, COLORS["primary"]),
        ),
    )

# Contenedores y tarjetas
def card(content, width=None, height=None, padding_=SPACING["lg"], on_click=None):
    container = ft.Container(
        content=content,
        padding=padding.all(padding_),
        width=width,
        height=height,
    )
    
    return ft.Card(
        content=container,
        elevation=2,
        surface_tint_color=COLORS["surface"],
        color=COLORS["surface"],
    ) if not on_click else ft.Container(
        content=ft.Card(
            content=container,
            elevation=2,
            surface_tint_color=COLORS["surface"],
            color=COLORS["surface"],
        ),
        on_click=on_click,
        ink=True,
    )

def section(title_text: str, content, description=None):
    controls = [
        ft.Text(title_text, **TYPOGRAPHY["h2"]),
    ]
    if description:
        controls.append(ft.Text(description, **TYPOGRAPHY["caption"]))
    controls.append(content)
    
    return ft.Column(controls, spacing=SPACING["md"])

# Campos de texto
def text_field(
    label: str,
    hint_text=None,
    password=False,
    can_reveal_password=False,
    width=None,
    prefix_icon=None,
    helper_text=None
):
    return ft.TextField(
        label=label,
        hint_text=hint_text,
        width=width,
        password=password,
        can_reveal_password=can_reveal_password,
        prefix_icon=prefix_icon,
        helper_text=helper_text,
        border_radius=BORDER_RADIUS_MD,
        text_size=TYPOGRAPHY["body"]["size"],
        border_color=COLORS["text"]["secondary"],
        focused_border_color=COLORS["primary"],
        focused_color=COLORS["primary"],
    )

# Títulos y textos
def title(text: str):
    return ft.Text(text, **TYPOGRAPHY["h1"])

def subtitle(text: str):
    return ft.Text(text, **TYPOGRAPHY["h3"])

def caption(text: str):
    return ft.Text(text, **TYPOGRAPHY["caption"])

# Mensajes y alertas
def success_message(text: str):
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.icons.CHECK_CIRCLE, color=COLORS["success"], size=24),
                ft.Text(text, color=COLORS["success"], size=14),
            ],
            spacing=SPACING["sm"],
        ),
        padding=padding.all(SPACING["md"]),
        bgcolor=ft.colors.with_opacity(0.1, COLORS["success"]),
        border_radius=BORDER_RADIUS_MD,
        visible=bool(text)
    )

def error_message(text: str):
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.icons.ERROR, color=COLORS["error"], size=24),
                ft.Text(text, color=COLORS["error"], size=14),
            ],
            spacing=SPACING["sm"],
        ),
        padding=padding.all(SPACING["md"]),
        bgcolor=ft.colors.with_opacity(0.1, COLORS["error"]),
        border_radius=BORDER_RADIUS_MD,
        visible=bool(text)
    )

# Navegación
def nav_button(text: str, icon: str, on_click=None, badge=None):
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Icon(icon, size=32),
                    bgcolor=ft.colors.with_opacity(0.1, COLORS["primary"]),
                    border_radius=BORDER_RADIUS_LG,
                    padding=padding.all(12),
                ),
                ft.Text(text, **TYPOGRAPHY["caption"], text_align=ft.TextAlign.CENTER),
                ft.Badge(text=str(badge), visible=badge is not None) if badge else ft.Container(),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=SPACING["xs"],
        ),
        padding=padding.all(SPACING["sm"]),
        border_radius=BORDER_RADIUS_MD,
        ink=True,
        on_click=on_click,
        tooltip=text,
    )

# Divisor con texto
def divider_with_text(text: str):
    return ft.Container(
        content=ft.Text(text, **TYPOGRAPHY["caption"]),
        margin=padding.symmetric(vertical=SPACING["md"]),
        alignment=ft.alignment.center
    ) 