#!/usr/bin/env python3
"""Ghost Writer Local - autocompletar em qualquer app do Windows, 100% local.

Protótipo do MVP descrito em ../DESIGN.md. Requer Windows + llama-server local.

Instalação:
    pip install uiautomation pynput requests pywin32 pyperclip
Servidor:
    llama-server -m modelo.gguf -c 4096 --host 127.0.0.1 --port 8080 --no-webui
Execução:
    python ghostwriter.py --model seu-modelo

Limitações conhecidas:
  - apps que não expõem texto via UI Automation ficam sem sugestão;
  - apps rodando como administrador exigem o script também elevado;
  - o overlay é aproximado (não mede largura de fonte).
"""

from __future__ import annotations

import argparse
import ctypes
import ctypes.wintypes as wt
import json
import queue
import re
import sys
import threading
import time
from pathlib import Path

import requests
import tkinter as tk

try:
    import uiautomation as auto
except ImportError:  # sem UIA o app roda, mas não sugere
    auto = None

try:
    import pyperclip
except ImportError:
    pyperclip = None

from pynput import keyboard

ENDPOINT = "http://127.0.0.1:8080/completion"
DEBOUNCE_S = 0.30
MIN_CHARS = 8
MAX_TOKENS = 12
PROFILE = Path(__file__).with_name("perfil.jsonl")

SENSITIVE = re.compile(
    r"(senha|password|passwd|cart[aã]o|credit ?card|banco|bank|conta|token|"
    r"cpf|cvv|login|prontu[aá]rio|sa[uú]de)",
    re.IGNORECASE,
)

STOP_SEQUENCES = ["\n", ". ", ", ", ";", "? ", "! "]


# --------------------------------------------------------------------------- #
# Contexto
# --------------------------------------------------------------------------- #
def foreground_title() -> str:
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    buf = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.GetWindowTextW(hwnd, buf, 512)
    return buf.value


def focused_text() -> tuple[str, str]:
    """Retorna (texto_do_campo, nome_do_controle). Vazio se não suportado."""
    if auto is None:
        return "", ""
    try:
        ctrl = auto.GetFocusedControl()
        if ctrl is None:
            return "", ""
        try:
            if ctrl.IsPassword:
                return "", "password"
        except Exception:
            pass
        value = ""
        try:
            value = ctrl.GetValuePattern().Value or ""
        except Exception:
            try:
                value = ctrl.GetPattern(auto.PatternId.ValuePattern).Value or ""
            except Exception:
                value = ""
        return value, ctrl.Name or ""
    except Exception:
        return "", ""


def caret_position() -> tuple[int, int] | None:
    """Posição do cursor na tela, quando o app expõe caret via GUI thread."""

    class GUITHREADINFO(ctypes.Structure):
        _fields_ = [
            ("cbSize", wt.DWORD),
            ("flags", wt.DWORD),
            ("hwndActive", wt.HWND),
            ("hwndFocus", wt.HWND),
            ("hwndCapture", wt.HWND),
            ("hwndMenuOwner", wt.HWND),
            ("hwndMoveSize", wt.HWND),
            ("hwndCaret", wt.HWND),
            ("rcCaret", wt.RECT),
        ]

    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        tid = ctypes.windll.user32.GetWindowThreadProcessId(hwnd, None)
        info = GUITHREADINFO()
        info.cbSize = ctypes.sizeof(GUITHREADINFO)
        if not ctypes.windll.user32.GetGUIThreadInfo(tid, ctypes.byref(info)):
            return None
        if not info.hwndCaret:
            return None
        point = wt.POINT(info.rcCaret.left, info.rcCaret.bottom)
        ctypes.windll.user32.ClientToScreen(info.hwndCaret, ctypes.byref(point))
        return point.x, point.y + 6
    except Exception:
        return None


# --------------------------------------------------------------------------- #
# Perfil e sugestão
# --------------------------------------------------------------------------- #
def load_style_hint() -> str:
    """Últimas aceitações viram uma dica curta de estilo."""
    if not PROFILE.exists():
        return ""
    accepted: list[str] = []
    try:
        for line in PROFILE.read_text(encoding="utf-8").splitlines()[-200:]:
            item = json.loads(line)
            if item.get("accepted"):
                accepted.append(item.get("text", ""))
    except Exception:
        return ""
    if not accepted:
        return ""
    sample = " / ".join(a.strip() for a in accepted[-5:] if a.strip())
    return f"Estilo do usuário (exemplos reais): {sample[:300]}\n"


def log_signal(accepted: bool, text: str, app: str) -> None:
    entry = {"ts": time.time(), "app": app, "accepted": accepted, "text": text[:120]}
    try:
        with PROFILE.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass


def build_prompt(before: str, mode: str) -> str:
    tail = before[-400:]
    if mode == "codigo":
        return f"<|fim_prefix|>{tail}<|fim_suffix|><|fim_middle|>"
    return (
        "Continue o texto exatamente do ponto onde ele para. "
        "Não repita o que já está escrito. No máximo uma frase curta.\n"
        f"{load_style_hint()}"
        f"---\n{tail}"
    )


def sanitize(suggestion: str) -> str:
    text = suggestion.split("\n")[0].strip()
    if not text:
        return ""
    # regra dura: nada de fato inventado
    if re.search(r"\d", text):
        return ""
    if len(text.split()) > 12:
        return ""
    return text


def complete(prompt: str, model: str) -> str:
    payload = {
        "prompt": prompt,
        "n_predict": MAX_TOKENS,
        "temperature": 0.35,
        "top_p": 0.9,
        "stop": STOP_SEQUENCES,
        "cache_prompt": True,
        "model": model,
    }
    try:
        resp = requests.post(ENDPOINT, json=payload, timeout=2.5)
        resp.raise_for_status()
        return resp.json().get("content", "")
    except Exception:
        return ""


def detect_mode(title: str, control: str) -> str:
    blob = f"{title} {control}".lower()
    if SENSITIVE.search(blob):
        return "sensitive"
    if re.search(r"(visual studio code|cursor|notepad\+\+|pycharm|sublime)", blob):
        return "codigo"
    if re.search(r"(whatsapp|telegram|discord|slack|teams)", blob):
        return "curto"
    return "prosa"


# --------------------------------------------------------------------------- #
# Interface
# --------------------------------------------------------------------------- #
class GhostOverlay:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        try:
            self.root.attributes("-alpha", 0.82)
        except tk.TclError:
            pass
        self.label = tk.Label(
            self.root,
            text="",
            font=("Segoe UI", 11),
            bg="#1f1f1f",
            fg="#9aa0a6",
            padx=6,
            pady=2,
        )
        self.label.pack()
        self.visible = False
        self.current = ""
        self.queue: queue.Queue = queue.Queue()

    def show(self, text: str, x: int, y: int) -> None:
        self.current = text
        self.label.config(text=text)
        self.root.geometry(f"+{max(x, 0)}+{max(y, 0)}")
        self.root.deiconify()
        self.visible = True

    def hide(self) -> None:
        self.visible = False
        self.current = ""
        self.root.withdraw()

    def drain(self) -> None:
        while True:
            try:
                action, payload = self.queue.get_nowait()
            except queue.Empty:
                break
            if action == "show" and payload[0]:
                self.show(*payload)
            else:
                self.hide()
        self.root.after(40, self.drain)


# --------------------------------------------------------------------------- #
# Loop principal
# --------------------------------------------------------------------------- #
def poll_loop(ui: GhostOverlay, model: str, stop: threading.Event) -> None:
    last_text = ""
    pending_since = 0.0
    while not stop.is_set():
        time.sleep(0.10)
        if ui.visible:
            continue
        text, control = focused_text()
        if not text:
            last_text = ""
            continue
        title = foreground_title()
        mode = detect_mode(title, control)
        if mode == "sensitive":
            last_text = text
            continue
        if text == last_text:
            continue
        last_text = text
        if len(text) < MIN_CHARS:
            continue
        pending_since = time.time()

        # debounce: espera o usuário parar de digitar
        while time.time() - pending_since < DEBOUNCE_S:
            time.sleep(0.03)
        fresh, _ = focused_text()
        if fresh != text:
            continue

        suggestion = sanitize(complete(build_prompt(text, mode), model))
        if not suggestion:
            continue
        pos = caret_position() or (200, 200)
        ui.queue.put(("show", (suggestion, pos[0], pos[1])))


def make_listener(ui: GhostOverlay) -> keyboard.Listener:
    controller = keyboard.Controller()

    def on_press(key):
        if key == keyboard.Key.esc and ui.visible:
            log_signal(False, ui.current, foreground_title())
            ui.hide()
            return False
        if key == keyboard.Key.tab and ui.visible:
            text = ui.current
            app = foreground_title()
            ui.hide()
            if pyperclip is not None:
                try:
                    backup = pyperclip.paste()
                    pyperclip.copy(text)
                    controller.press(keyboard.Key.ctrl)
                    controller.press("v")
                    controller.release("v")
                    controller.release(keyboard.Key.ctrl)
                    time.sleep(0.05)
                    pyperclip.copy(backup)
                except Exception:
                    controller.type(text)
            else:
                controller.type(text)
            log_signal(True, text, app)
            return False
        return True

    return keyboard.Listener(on_press=on_press)


def main() -> int:
    parser = argparse.ArgumentParser(description="Ghost Writer Local (MVP)")
    parser.add_argument("--model", default="local", help="nome do modelo no llama-server")
    parser.add_argument("--check", action="store_true", help="testa o servidor e sai")
    args = parser.parse_args()

    if args.check:
        print("servidor:", "ok" if complete("teste", args.model) is not None else "falhou")
        print("UIA:", "ok" if auto is not None else "indisponível")
        print("clipboard:", "ok" if pyperclip is not None else "indisponível")
        return 0

    ui = GhostOverlay()
    ui.root.withdraw()
    stop = threading.Event()

    threading.Thread(target=poll_loop, args=(ui, args.model, stop), daemon=True).start()
    listener = make_listener(ui)
    listener.start()
    ui.root.after(40, ui.drain)
    try:
        ui.root.mainloop()
    finally:
        stop.set()
        listener.stop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
