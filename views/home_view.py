import flet as ft
from styles.style import TITLE_STYLE, PAGE_PADDING

def home_view(page: ft.Page) -> ft.Control:
    return ft.Container(
        padding=PAGE_PADDING,
        content=ft.Text("Home (em construção)", style=TITLE_STYLE),
    )
