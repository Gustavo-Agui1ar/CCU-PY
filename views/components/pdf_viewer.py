import flet as ft
from styles.style import BASE_WIDTH, PAGE_HEIGHT_ESTIMADA
import os

class PdfViewer:
    def __init__(
        self,
        page: ft.Page,
        pdf_saida_path_getter,
        on_reload,
    ):
        """
        page: ft.Page
        pdf_saida_path_getter: função que retorna o caminho do PDF atual
        on_reload: função chamada ao clicar em reload
        """
        self.page = page
        self.get_pdf_path = pdf_saida_path_getter
        self.on_reload = on_reload

        self.zoom = 1.0

        self._build()

    # ---------------- BUILD ----------------

    def _build(self):

        self.contador_paginas = ft.Text("0 / 0")

        self.viewer_column = ft.Column(
            spacing=30,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            on_scroll=self._update_page_counter,
        )

        self.viewer_container = ft.Container(
            expand=True,
            alignment=ft.Alignment(0, 0),
            bgcolor=ft.Colors.GREY_300,
            padding=30,
            content=self.viewer_column,
            visible=False,
        )

        self.toolbar = ft.Container(
            bgcolor=ft.Colors.GREY_900,
            padding=10,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        controls=[
                            ft.IconButton(ft.Icons.ZOOM_OUT, on_click=self.zoom_out),
                            ft.IconButton(ft.Icons.ZOOM_IN, on_click=self.zoom_in),
                        ]
                    ),
                    self.contador_paginas,
                    ft.Row(
                        controls=[
                            ft.IconButton(ft.Icons.REFRESH, on_click=self.reload),
                            ft.IconButton(ft.Icons.DOWNLOAD, on_click=self.download),
                        ]
                    ),
                ],
            ),
        )

    # ---------------- MÉTODOS PÚBLICOS ----------------

    def get_controls(self):
        """Retorna os controles para uso na view"""
        return [
            self.toolbar,
            self.viewer_container,
        ]

    def show(self):
        self.viewer_container.visible = True
        self.page.update()

    def hide(self):
        self.viewer_container.visible = False
        self.page.update()

    def clear(self):
        self.viewer_column.controls.clear()
        self.contador_paginas.value = "0 / 0"
        self.page.update()

    def load_images(self, image_paths: list[str]):
        """Atualiza visualização com imagens do PDF"""
        self.clear()

        if not image_paths:
            return

        for img_path in image_paths:
            self.viewer_column.controls.append(
                ft.Container(
                    width=int(BASE_WIDTH * self.zoom),
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

        self.contador_paginas.value = f"1 / {len(image_paths)}"
        self.show()

    # ---------------- AÇÕES ----------------

    def zoom_in(self, e=None):
        self.zoom += 0.1
        self._apply_zoom()

    def zoom_out(self, e=None):
        self.zoom = max(0.1, self.zoom - 0.1)
        self._apply_zoom()

    def reload(self, e=None):
        if callable(self.on_reload):
            self.on_reload(e)

    def download(self, e=None):
        pdf_path = self.get_pdf_path()
        if not pdf_path or not os.path.exists(pdf_path):
            return

        picker = ft.FilePicker(on_result=lambda ev: self._save_pdf(ev, pdf_path))
        self.page.overlay.append(picker)
        picker.get_directory_path()

    # ---------------- INTERNOS ----------------

    def _apply_zoom(self):
        for container in self.viewer_column.controls:
            container.width = int(BASE_WIDTH * self.zoom)
        self.page.update()

    def _update_page_counter(self, e: ft.ScrollEvent):
        if not self.viewer_container.visible:
            return

        page_size = PAGE_HEIGHT_ESTIMADA + self.viewer_column.spacing
        current_page = int(e.pixels // page_size) + 1
        total = len(self.viewer_column.controls)

        current_page = max(1, min(current_page, total))
        self.contador_paginas.value = f"{current_page} / {total}"
        self.page.update()

    def _save_pdf(self, e: ft.FilePickerResultEvent, pdf_path: str):
        if not e.path:
            return

        destino = os.path.join(e.path, os.path.basename(pdf_path))
        with open(pdf_path, "rb") as o, open(destino, "wb") as s:
            s.write(o.read())
