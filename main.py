import flet as ft

from styles.theme import apply_theme
from views.home_view import home_view
from views.configs_view import configuracoes_view

def main(page: ft.Page):
    page.title = "Aplicação Desktop"
    apply_theme(page)

    content = ft.Container(expand=True)

    def trocar_view(index: int):
        if index == 0:
            content.content = home_view(page)
        elif index == 1:
            content.content = configuracoes_view(page)
        page.update()

    trocar_view(0)

    menu = ft.NavigationRail(
        selected_index=0,
        extended=True,
        label_type=ft.NavigationRailLabelType.ALL,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Home",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label="Configurações",
            ),
        ],
        on_change=lambda e: trocar_view(e.control.selected_index),
    )

    page.add(
        ft.Row(
            expand=True,
            controls=[
                menu,
                ft.VerticalDivider(width=1),
                content,
            ],
        )
    )

ft.app(target=main)
