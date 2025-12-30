import asyncio
import flet as ft
import pdf_generator as pg
import robot_utils.robot_runner as rr
import utils.utils as utils
import os
from styles.style import TITLE_STYLE, PAGE_PADDING


BASE_WIDTH = 800
PAGE_HEIGHT_ESTIMADA = int(BASE_WIDTH * 1.35)

def relatorio_view(page: ft.Page) -> ft.Control:

    # ---------------- DIALOG ----------------

    def criar_dialog():
        return ft.AlertDialog(
            modal=True,
            content=ft.Container(
                width=380,
                padding=20,
                content=ft.Column(
                    tight=True,
                    spacing=16,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(size=48),
                        ft.Text(size=20, weight=ft.FontWeight.BOLD),
                        ft.Text(size=14, color=ft.Colors.GREY_700),
                        ft.Divider(height=1),
                        ft.ElevatedButton("OK", on_click=lambda e: page.close(dialog)),
                    ],
                ),
            ),
        )

    dialog = criar_dialog()

    def mostrar_dialog(titulo, mensagem, sucesso=True):
        icon, title, text = dialog.content.content.controls[:3]

        icon.name = ft.Icons.CHECK_CIRCLE if sucesso else ft.Icons.ERROR
        icon.color = ft.Colors.GREEN_600 if sucesso else ft.Colors.RED_600

        title.value = titulo
        text.value = mensagem

        page.open(dialog)

    # ---------------- FILE PICKER ----------------

    def selecionar_diretorio(e: ft.FilePickerResultEvent):
        if not e.path:
            return
        try:
            destino = os.path.join(e.path, os.path.basename(pg.PDF_SAIDA))
            with open(pg.PDF_SAIDA, "rb") as o, open(destino, "wb") as s:
                s.write(o.read())
            mostrar_dialog("Sucesso", "PDF salvo com sucesso.")
        except Exception as ex:
            mostrar_dialog("Erro", str(ex), False)

    file_picker = ft.FilePicker(on_result=selecionar_diretorio)
    page.overlay.append(file_picker)

    # ---------------- PROGRESSO ----------------

    progress_text = ft.Text("", visible=False)
    progress_bar = ft.ProgressBar(width=420, visible=False)

    progress_container = ft.Container(
        alignment=ft.alignment.center,
        visible=False,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[progress_text, progress_bar],
        ),
    )

    def atualizar_progresso(msg, value):
        progress_text.value = msg
        progress_bar.value = value
        page.update()

    # ---------------- PDF VIEWER ----------------

    zoom = {"value": 1.0}
    BASE_WIDTH = 800

    def update_page_counter(e: ft.ScrollEvent):
        if not viewer_container.visible or not viewer_column.controls:
            return

        scroll_pos = e.pixels
        page_size = PAGE_HEIGHT_ESTIMADA + viewer_column.spacing

        current_page = int(scroll_pos // page_size) + 1
        total = len(viewer_column.controls)

        current_page = max(1, min(current_page, total))
        contador_paginas.value = f"{current_page} / {total}"
        page.update()


    viewer_column = ft.Column(
        spacing=30,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        on_scroll=update_page_counter,
    )

    viewer_container = ft.Container(
        expand=True,
        alignment= ft.alignment.center,
        bgcolor=ft.Colors.GREY_300,
        padding=30,
        content=viewer_column,
        visible=False,
    )

    contador_paginas = ft.Text("0 / 0", style=TITLE_STYLE)


    # ---------------- AÇÕES ----------------

    def gerar_e_mostrar(e):
        progress_container.visible = True
        progress_text.visible = True
        progress_bar.visible = True
        progress_bar.value = 0
        page.update()

        async def tarefa():

            await asyncio.to_thread(rr.executar_robot, on_progress=atualizar_progresso)
            await asyncio.to_thread(pg.main, on_progress=atualizar_progresso)

            if not os.path.exists(pg.PDF_SAIDA):
                return

            imagens, _ = utils.pdf_para_imagens(pg.PDF_SAIDA)

            viewer_column.controls.clear()
            contador_paginas.value = f"1 / {len(imagens)}"

            for img_path in imagens:
                viewer_column.controls.append(
                    ft.Container(
                        width=int(BASE_WIDTH * zoom["value"]),
                        bgcolor=ft.Colors.WHITE,
                        padding=12,
                        border_radius=4,
                        shadow=ft.BoxShadow(
                            blur_radius=15,
                            spread_radius=1,
                            color=ft.Colors.BLACK26,
                            offset=ft.Offset(0, 5),
                        ),
                        content=ft.Image(src=img_path, fit=ft.ImageFit.CONTAIN),
                    )
                )

            progress_container.visible = False
            viewer_container.visible = True
            page.update()

        page.run_task(tarefa)

    def baixar_pdf(e):
        if os.path.exists(pg.PDF_SAIDA):
            file_picker.get_directory_path()

    def zoom_in(e):
        zoom["value"] += 0.1
        for container in viewer_column.controls:
            container.width = int(BASE_WIDTH * zoom["value"])
        page.update()

    def zoom_out(e):
        zoom["value"] = max(0.1, zoom["value"] - 0.1)
        for container in viewer_column.controls:
            container.width = int(BASE_WIDTH * zoom["value"])
        page.update()

    # ---------------- TOOLBAR ----------------

    toolbar = ft.Container(
        bgcolor=ft.Colors.GREY_900,
        padding=10,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(ft.Icons.ZOOM_OUT, on_click=zoom_out),
                        ft.IconButton(ft.Icons.ZOOM_IN, on_click=zoom_in),
                    ]
                ),
                contador_paginas,
                ft.Row(
                    controls=[
                        ft.IconButton(ft.Icons.REFRESH, on_click=gerar_e_mostrar),
                        ft.IconButton(ft.Icons.DOWNLOAD, on_click=baixar_pdf),
                    ]
                ),
            ],
        ),
    )

    # ---------------- BOTÃO ----------------

    row_generate_button = ft.Container(
        padding=PAGE_PADDING,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.ElevatedButton("Gerar Relatório PDF", on_click=gerar_e_mostrar)
            ],
        ),
    )

    # ---------------- VIEW FINAL ----------------

    return ft.Container(
        expand=True,
        padding=PAGE_PADDING,
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                ft.Text("Relatório", style=TITLE_STYLE),
                row_generate_button,
                progress_container,
                toolbar,
                viewer_container,
            ],
        ),
    )
