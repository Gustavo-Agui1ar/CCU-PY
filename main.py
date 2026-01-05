import flet as ft
import traceback

import flet as ft

from styles.theme import apply_theme

from views.relatorio_view import relatorio_view

from views.configs_view import configuracoes_view


def main(page: ft.Page):

    try:
        page.title = "Aplicação Desktop"
    except Exception:
        traceback.print_exc()

    try:
        apply_theme(page)
    except Exception:
        traceback.print_exc()

    try:
        content = ft.Container(expand=True)
    except Exception:
        traceback.print_exc()

    def abrir_drawer(e):
        page.open(page.drawer)

    def trocar_view(index: int):
        try:
            if index == 0:
                content.content = relatorio_view(page)
            elif index == 1:
                content.content = configuracoes_view(page)

            page.drawer.selected_index = index
            page.close(page.drawer)
            page.update()

        except Exception:
            traceback.print_exc()

    try:
        page.drawer = ft.NavigationDrawer(
            selected_index=0,
            controls=[
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.PICTURE_AS_PDF_OUTLINED,
                    selected_icon=ft.Icons.PICTURE_AS_PDF,
                    label="Relatório",
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                    label="Configurações",
                ),
            ],
            on_change=lambda e: trocar_view(e.control.selected_index),
        )
    except Exception:
        traceback.print_exc()

    try:
        page.appbar = ft.AppBar(
            title=ft.Text("Aplicação Desktop"),
            leading=ft.IconButton(
                icon=ft.Icons.MENU,
                on_click=abrir_drawer,
            ),
            bgcolor=ft.Colors.GREY_900,
        )
    except Exception:
        traceback.print_exc()

    try:
        content.content = relatorio_view(page)
    except Exception:
        traceback.print_exc()

    try:
        page.add(content)
    except Exception:
        traceback.print_exc()


if __name__ == "__main__":

    ft.app(target=main, view=ft.FLET_APP)
