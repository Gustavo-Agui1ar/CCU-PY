import flet as ft
from datetime import time, datetime


def TimeField(page: ft.Page, label: str, width=180):
    state = {"time": None}

    tf = ft.TextField(
        label=label,
        width=width,
        read_only=True,
    )

    time_picker = ft.TimePicker()

    def on_time(e):
        if not e.control.value:
            return

        state["time"] = e.control.value
        tf.value = e.control.value.strftime("%H:%M")
        page.update()

    time_picker.on_change = on_time

    tf.on_click = lambda e: page.open(time_picker)

    page.overlay.append(time_picker)

    def get_value():
        return state["time"]  # datetime.time


    def set_value(value):
        if not value:
            return

        if isinstance(value, time):
            t = value

        elif isinstance(value, datetime):
            t = value.time()

        elif isinstance(value, str):
            try:
                # ISO datetime
                if "T" in value:
                    t = datetime.fromisoformat(value).time()
                else:
                    parts = value.split(":")
                    h = int(parts[0])
                    m = int(parts[1])
                    t = time(h, m)
            except Exception:
                return

        else:
            return
        
        state["time"] = t
        tf.value = t.strftime("%H:%M")

    tf.get_value = get_value
    tf.set_value = set_value

    return tf

