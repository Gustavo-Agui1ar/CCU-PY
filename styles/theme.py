import flet as ft

def apply_theme(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1000
    page.window_height = 650

    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE,
            secondary=ft.Colors.BLUE_GREY,
            background=ft.Colors.GREY_50,
        ),
        text_theme=ft.TextTheme(
            title_large=ft.TextStyle(
                size=24,
                weight=ft.FontWeight.BOLD,
            ),
            body_medium=ft.TextStyle(
                size=14,
            ),
        ),
    )
