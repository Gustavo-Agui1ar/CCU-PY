import flet as ft
import pdf_generator as pg
import utils.utils as utils
import os
from styles.style import TITLE_STYLE, PAGE_PADDING


def home_view(page: ft.Page) -> ft.Control:

    zoom = {"value": 1.0}
    ZOOM_STEP = 0.1
    ZOOM_MIN = 0.5
    ZOOM_MAX = 2.5

    BASE_WIDTH = 800

    viewer_column = ft.Column(
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    viewer_container = ft.Container(
        expand=True,
        bgcolor=ft.Colors.GREY_200,
        padding=20,
        content=viewer_column,
        visible=False,
    )

    def aplicar_zoom():
        for page_container in viewer_column.controls:
            page_container.width = int(BASE_WIDTH * zoom["value"])
        page.update()

    def zoom_in(e):
        if zoom["value"] < ZOOM_MAX:
            zoom["value"] += ZOOM_STEP
            aplicar_zoom()

    def zoom_out(e):
        if zoom["value"] > ZOOM_MIN:
            zoom["value"] -= ZOOM_STEP
            aplicar_zoom()

    def gerar_e_mostrar(e):
        pg.main()

        if not os.path.exists(pg.PDF_SAIDA):
            return

        imagens, _ = utils.pdf_para_imagens(pg.PDF_SAIDA)

        viewer_column.controls.clear()

        for img_path in imagens:
            viewer_column.controls.append(
                ft.Container(
                    width=int(BASE_WIDTH * zoom["value"]),
                    bgcolor=ft.Colors.WHITE,
                    padding=10,
                    alignment=ft.alignment.center,
                    border_radius=4,
                    shadow=ft.BoxShadow(
                        blur_radius=12,
                        spread_radius=1,
                        color=ft.Colors.BLACK26,
                        offset=ft.Offset(0, 4),
                    ),
                    content=ft.Image(
                        src=img_path,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                )
            )

        viewer_container.visible = True
        page.update()

    return ft.Container(
        padding=PAGE_PADDING,
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=20,
            controls=[
                ft.Text("Relatório", style=TITLE_STYLE),

                ft.Row(
                    spacing=10,
                    controls=[
                        ft.ElevatedButton("Gerar Relatório", on_click=gerar_e_mostrar),
                        ft.IconButton(ft.Icons.ZOOM_IN, on_click=zoom_in),
                        ft.IconButton(ft.Icons.ZOOM_OUT, on_click=zoom_out),
                    ],
                ),

                ft.Divider(),
                viewer_container,
            ],
        ),
    )
