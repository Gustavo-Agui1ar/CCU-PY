import flet as ft

from styles.theme import apply_theme
from views.relatorio_view import relatorio_view
from views.configs_view import configuracoes_view

def main(page: ft.Page):
    page.title = "Aplicação Desktop"
    
    try:
        apply_theme(page)
    except Exception as e:
        print(f"Aviso: Não foi possível carregar o tema: {e}")

    content = ft.Container(expand=True)

    def abrir_drawer(e):
        page.open(page.drawer)

    def trocar_view(index: int):
        if index == 0:
            content.content = relatorio_view(page)
        elif index == 1:
            content.content = configuracoes_view(page)

        page.drawer.selected_index = index
        page.close(page.drawer)
        page.update()
   
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

    page.appbar = ft.AppBar(
        title=ft.Text("Aplicação Desktop"),
        leading=ft.IconButton(
            icon=ft.Icons.MENU,
            on_click=abrir_drawer,
        ),
        bgcolor=ft.Colors.GREY_900,
    )

    content.content = relatorio_view(page)
    
    page.add(content)

if __name__ == "__main__":
    ft.app(target=main)