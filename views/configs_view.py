import flet as ft
import flet.canvas as cv
import json
import os
from utils.cripto_utils import CriptoUtils
from PIL import Image, ImageDraw

from styles.style import (
    PAGE_PADDING,
    TITLE_STYLE,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    FIELD_WIDTH,
    HALF_FIELD_WIDTH,
    STATUS_SUCCESS,
)

CONFIG_PATH = "configs/config.json"

W, H = 800, 200


class SignatureState:
    x: float | None = None
    y: float | None = None
    stroke: int = 2


def configuracoes_view(page: ft.Page) -> ft.Control:
    # =========================================================
    # CAMPOS BÁSICOS
    # =========================================================
    url_ccu = ft.TextField(label="URL", width=FIELD_WIDTH)
    usuario_ccu = ft.TextField(label="Usuário", width=FIELD_WIDTH)
    senha_ccu = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        width=FIELD_WIDTH,
    )

    browser = ft.Dropdown(
        label="Browser",
        value="firefox",
        width=FIELD_WIDTH,
        options=[
            ft.dropdown.Option("firefox"),
            ft.dropdown.Option("chrome"),
            ft.dropdown.Option("edge"),
        ],
    )

    timeout_bloqueio = ft.TextField(label="Timeout Bloqueio", width=HALF_FIELD_WIDTH)
    timeout_visibilidade = ft.TextField(label="Timeout Visibilidade", width=HALF_FIELD_WIDTH)

    csv_horas = ft.TextField(label="CSV Horas", width=FIELD_WIDTH)

    status = ft.Text()

    # =========================================================
    # CONFIGURAÇÃO DE ASSINATURA
    # =========================================================
    assinatura_tipo = ft.RadioGroup(
        value="canvas",
        content=ft.Row(
            controls=[
                ft.Radio(value="canvas", label="Desenhada"),
                ft.Radio(value="digitada", label="Digitada"),
            ]
        ),
    )

    assinatura_texto = ft.TextField(
        label="Assinatura digitada",
        width=FIELD_WIDTH,
        visible=False,
    )

    url_email = ft.TextField(label="URL E-mail", width=FIELD_WIDTH)
    usuario_email = ft.TextField(label="Usuário E-mail", width=FIELD_WIDTH)
    senha_email = ft.TextField(
        label="Senha E-mail",
        password=True,
        can_reveal_password=True,
        width=FIELD_WIDTH,
    )

    # =========================================================
    # ASSINATURA DESENHADA (CANVAS)
    # =========================================================
    sig_state = SignatureState()

    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    def pan_start(e: ft.DragStartEvent):
        sig_state.x = e.local_x
        sig_state.y = e.local_y

    def pan_update(e: ft.DragUpdateEvent):
        if sig_state.x is None:
            return

        canvas.shapes.append(
            cv.Line(
                sig_state.x,
                sig_state.y,
                e.local_x,
                e.local_y,
                paint=ft.Paint(
                    stroke_width=sig_state.stroke,
                    color=ft.Colors.BLACK,
                ),
            )
        )

        draw.line(
            (sig_state.x, sig_state.y, e.local_x, e.local_y),
            fill="black",
            width=sig_state.stroke,
        )

        sig_state.x = e.local_x
        sig_state.y = e.local_y
        canvas.update()

    def limpar_assinatura(e):
        canvas.shapes.clear()
        canvas.shapes.append(cv.Fill(ft.Paint(color=ft.Colors.GREY_500)))
        img.paste((0, 0, 0, 0), (0, 0, W, H))
        canvas.update()

    def salvar_assinatura():
        os.makedirs("results", exist_ok=True)
        img.save("results/assinatura.png")

    def mudar_espessura(e):
        sig_state.stroke = int(e.control.value)

    slider_espessura = ft.Slider(
        min=1,
        max=10,
        value=2,
        divisions=9,
        label="{value}",
        on_change=mudar_espessura,
        width=300,
    )

    canvas = cv.Canvas(
        shapes=[cv.Fill(ft.Paint(color=ft.Colors.GREY_500))],
        content=ft.GestureDetector(
            on_pan_start=pan_start,
            on_pan_update=pan_update,
            drag_interval=10,
        ),
        width=W,
        height=H,
    )

    assinatura_canvas = ft.Column(
        controls=[
            ft.Container(
                content=canvas,
                border=ft.border.all(2, ft.Colors.GREY),
                border_radius=6,
                width=W,
                height=H,
            ),
            ft.Text("Espessura do traço"),
            slider_espessura,
            ft.OutlinedButton("Limpar assinatura", on_click=limpar_assinatura),
        ],
        visible=True,
    )

    # =========================================================
    # CONTROLE DE VISIBILIDADE
    # =========================================================
    def on_tipo_assinatura_change(e):
        assinatura_texto.visible = assinatura_tipo.value == "digitada"
        assinatura_canvas.visible = assinatura_tipo.value == "canvas"
        page.update()

    assinatura_tipo.on_change = on_tipo_assinatura_change

    # =========================================================
    # CARREGAR CONFIGURAÇÃO
    # =========================================================
    def carregar_config():
        if not os.path.exists(CONFIG_PATH):
            return

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)

        url_ccu.value = config.get("url", "")
        usuario_ccu.value = config.get("usuario", "")
        senha_ccu.value = CriptoUtils.decrypt(config.get("senha", ""))
        browser.value = config.get("browser", "firefox")

        timeouts = config.get("timeouts", {})
        timeout_bloqueio.value = timeouts.get("bloqueio", "")
        timeout_visibilidade.value = timeouts.get("visibilidade", "")

        arquivos = config.get("arquivos", {})
        csv_horas.value = arquivos.get("csv_horas", "")

        assinatura = config.get("assinatura", {})
        assinatura_tipo.value = assinatura.get("tipo", "canvas")
        assinatura_texto.value = assinatura.get("texto", "")

        assinatura_texto.visible = assinatura_tipo.value == "digitada"
        assinatura_canvas.visible = assinatura_tipo.value == "canvas"

        email = config.get("email", {})
        url_email.value = email.get("url_email", "")
        usuario_email.value = email.get("usuario_email", "")
        senha_email.value = CriptoUtils.decrypt(email.get("senha_email", ""))

    # =========================================================
    # SALVAR CONFIGURAÇÃO
    # =========================================================
    def salvar_config(e):
        if assinatura_tipo.value == "canvas":
            salvar_assinatura()

        config = {
            "url": url_ccu.value,
            "usuario": usuario_ccu.value,
            "senha": CriptoUtils.encrypt(senha_ccu.value),
            "browser": browser.value,
            "timeouts": {
                "bloqueio": timeout_bloqueio.value,
                "visibilidade": timeout_visibilidade.value,
            },
            "arquivos": {
                "csv_horas": csv_horas.value
            },
            "assinatura": {
                "tipo": assinatura_tipo.value,
                "texto": assinatura_texto.value if assinatura_tipo.value == "digitada" else "",
                "arquivo": "results/assinatura.png",
            },
            "email": {
                "url_email": url_email.value,
                "usuario_email": usuario_email.value,
                "senha_email": CriptoUtils.encrypt(senha_email.value),
            },
        }

        os.makedirs("configs", exist_ok=True)

        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        status.value = "Configurações salvas com sucesso"
        status.style = STATUS_SUCCESS
        page.update()

    # =========================================================
    # INICIALIZA
    # =========================================================
    carregar_config()

    # =========================================================
    # LAYOUT FINAL
    # =========================================================
    return ft.Container(
        padding=PAGE_PADDING,
        content=ft.Column(
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("Configurações", style=TITLE_STYLE),

                url_ccu,
                usuario_ccu,
                senha_ccu,
                browser,

                ft.Text("Timeouts", weight=ft.FontWeight.BOLD),
                ft.Row(
                    spacing=20,
                    controls=[timeout_bloqueio, timeout_visibilidade],
                ),

                csv_horas,

                ft.Divider(),
                ft.Text("Configurações de E-mail", style=TITLE_STYLE),

                url_email,
                usuario_email,
                senha_email,

                ft.Divider(),
                ft.Text("Assinatura", style=TITLE_STYLE),
                assinatura_tipo,
                assinatura_texto,
                assinatura_canvas,


                ft.ElevatedButton(
                    "Salvar",
                    width=BUTTON_WIDTH,
                    height=BUTTON_HEIGHT,
                    on_click=salvar_config,
                ),
                status,
            ],
        ),
    )
