import flet as ft

def apply_theme(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1000
    page.window_height = 650

    page.theme = ft.Theme(
        use_material3=True,
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE_400,
            secondary=ft.Colors.BLUE_GREY_300,

            background=ft.Colors.GREY_900,   # fundo geral
            surface=ft.Colors.GREY_800,      # cards / forms
            surface_variant=ft.Colors.GREY_800,

            outline=ft.Colors.GREY_600,      # 🔴 bordas visíveis
            outline_variant=ft.Colors.GREY_700,

            on_background=ft.Colors.GREY_100,
            on_surface=ft.Colors.GREY_100,
            on_primary=ft.Colors.BLACK,
        ),

        text_theme=ft.TextTheme(
            title_large=ft.TextStyle(
                size=26,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_400,
            ),
            title_medium=ft.TextStyle(
                size=18,
                weight=ft.FontWeight.W_600,
                color=ft.Colors.GREY_100,
            ),
            body_medium=ft.TextStyle(
                size=14,
                color=ft.Colors.GREY_200,
            ),
            label_large=ft.TextStyle(
                size=13,
                color=ft.Colors.GREY_300,
            ),
        ),
    )
