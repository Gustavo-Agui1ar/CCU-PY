import flet as ft

PAGE_PADDING = 30
FIELD_WIDTH = 650
HALF_FIELD_WIDTH = 315
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 45
BASE_WIDTH = 800
PAGE_HEIGHT_ESTIMADA = int(BASE_WIDTH * 1.35)

TITLE_STYLE = ft.TextStyle(
    size=24,
    weight=ft.FontWeight.BOLD,
    color=ft.Colors.BLUE,
)

STATUS_SUCCESS = ft.TextStyle(
    color=ft.Colors.GREEN,
    weight=ft.FontWeight.BOLD,
)

DIVIDER = ft.Divider(
    height=1,
    thickness=1,
    color=ft.Colors.GREY_500,
)

