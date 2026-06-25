import sys
import os
import subprocess
import webview

# Dispositivos
PLAYWRIGHT_DEVICES = {
    "iPhone 15 Pro":      "iPhone 15 Pro",
    "iPhone 13":          "iPhone 13",
    "Samsung Galaxy S23": "Galaxy S9+",   
    "Google Pixel 7":     "Pixel 5",      
}

# Launcher
LAUNCHER_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Assinatura Digital</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0d0d1a;
    color: #dde1f0;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    -webkit-app-region: drag;
  }

  button, input, select { -webkit-app-region: no-drag; }

  /* ── Header ── */
  .header {
    padding: 22px 26px 16px;
    background: linear-gradient(160deg, #13132b 0%, #0d0d1a 100%);
    border-bottom: 1px solid #1c1c3a;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .header-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #4361ee, #7209b7);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
  }
  .header-text h1 {
    font-size: 15px; font-weight: 700;
    color: #fff; letter-spacing: 0.3px;
  }
  .header-text p {
    font-size: 11px; color: #5a5a8a; margin-top: 2px;
  }

  /* ── Content ── */
  .content {
    flex: 1;
    padding: 20px 26px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    overflow-y: auto;
  }

  .field { display: flex; flex-direction: column; gap: 6px; }

  label {
    font-size: 11px; font-weight: 600;
    color: #7070a0;
    text-transform: uppercase;
    letter-spacing: 0.6px;
  }

  .row { display: flex; gap: 8px; }

  input[type="text"], select {
    flex: 1;
    background: #13132b;
    border: 1.5px solid #1e1e40;
    border-radius: 9px;
    padding: 10px 13px;
    color: #dde1f0;
    font-size: 13px;
    outline: none;
    transition: border-color .18s, box-shadow .18s;
  }
  input[type="text"]:focus, select:focus {
    border-color: #4361ee;
    box-shadow: 0 0 0 3px rgba(67,97,238,.15);
  }
  input::placeholder { color: #35355a; }

  select { cursor: pointer; appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%235a5a8a'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 13px center;
    padding-right: 30px;
  }
  select option { background: #13132b; }

  /* ── Buttons ── */
  .btn-paste {
    background: #13132b;
    border: 1.5px solid #1e1e40;
    border-radius: 9px;
    padding: 10px 14px;
    color: #7070a0;
    font-size: 12px;
    cursor: pointer;
    transition: all .18s;
    white-space: nowrap;
  }
  .btn-paste:hover { border-color: #4361ee; color: #4361ee; }

  .btn-open {
    width: 100%;
    background: linear-gradient(135deg, #4361ee 0%, #7209b7 100%);
    border: none;
    border-radius: 10px;
    padding: 13px;
    color: #fff;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.6px;
    cursor: pointer;
    transition: all .18s;
    box-shadow: 0 4px 16px rgba(67,97,238,.25);
  }
  .btn-open:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 6px 22px rgba(67,97,238,.4);
  }
  .btn-open:active:not(:disabled) { transform: translateY(0); }
  .btn-open:disabled { opacity: .45; cursor: not-allowed; }

  /* ── Status ── */
  .status {
    font-size: 12px; text-align: center;
    min-height: 18px; color: #4cc9f0;
    transition: color .2s;
  }
  .status.error { color: #f72585; }
  .status.ok    { color: #4cc9f0; }

  /* ── Info ── */
  .info {
    background: #0a0a18;
    border: 1px solid #1a1a35;
    border-radius: 9px;
    padding: 12px 14px;
    font-size: 11px;
    color: #50507a;
    line-height: 1.8;
  }
  .info b { color: #8080aa; }
  .info .step { display: flex; align-items: flex-start; gap: 8px; }
  .info .num {
    background: #1a1a35; border-radius: 50%;
    width: 18px; height: 18px;
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 700; color: #6060a0;
    flex-shrink: 0; margin-top: 1px;
  }
</style>
</head>
<body>

<div class="header">
  <div class="header-icon">✍️</div>
  <div class="header-text">
    <h1>Assinatura Digital</h1>
    <p>Assine documentos mobile-only pelo computador</p>
  </div>
</div>

<div class="content">

  <div class="field">
    <label>Link do documento</label>
    <div class="row">
      <input type="text" id="url"
             value="https://www.google.com"
             placeholder="https://assinar.io/...">
      <button class="btn-paste" onclick="colarUrl()" title="Colar da área de transferência">
        📋 Colar
      </button>
    </div>
  </div>

  <div class="field">
    <label>Dispositivo mobile emulado</label>
    <select id="device">
      <option>iPhone 15 Pro</option>
      <option>iPhone 13</option>
      <option>Samsung Galaxy S23</option>
      <option>Google Pixel 7</option>
    </select>
  </div>

  <button class="btn-open" id="btnAbrir" onclick="abrir()">
    ABRIR PARA ASSINAR
  </button>

  <div class="status" id="status"></div>

  <div class="info">
    <b>Como usar:</b>
    <br>
    <div class="step"><div class="num">1</div><span>Cole o link recebido por SMS ou e-mail</span></div>
    <div class="step"><div class="num">2</div><span>Selecione o dispositivo e clique em Abrir</span></div>
    <div class="step"><div class="num">3</div><span>Uma janela mobile abrirá — autorize e assine</span></div>
  </div>

</div>

<script>
  async function colarUrl() {
    try {
      const text = await navigator.clipboard.readText();
      if (text.startsWith('http')) {
        document.getElementById('url').value = text;
      }
    } catch(e) {
      // clipboard pode ser negado — ignora silenciosamente
    }
  }

  async function abrir() {
    const url    = document.getElementById('url').value.trim();
    const device = document.getElementById('device').value;
    const btn    = document.getElementById('btnAbrir');
    const status = document.getElementById('status');

    if (!url) {
      setStatus('Informe o link do documento.', 'error');
      return;
    }

    btn.disabled = true;
    setStatus('🟢 Janela mobile ativa! Conclua a assinatura na outra tela.', 'ok');

    const result = await window.pywebview.api.abrir(url, device);

    if (result.ok) {
      setStatus('🏁 Janela fechada! Sessão encerrada com sucesso.', 'ok');
    } else {
      setStatus(result.msg || 'Erro ao abrir.', 'error');
    }

    btn.disabled = false;
  }

  function setStatus(msg, cls) {
    const el = document.getElementById('status');
    el.textContent = msg;
    el.className = 'status ' + (cls || '');
  }
</script>
</body>
</html>
"""


# API js
class LauncherAPI:
    def abrir(self, url: str, device: str):
        if getattr(sys, "frozen", False):
            exe = [sys.executable]
        else:
            exe = [sys.executable, os.path.abspath(__file__)]

        try:
            proc = subprocess.Popen(
                exe + ["--browser", url, device],
                close_fds=True,
            )
            proc.wait()
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "msg": str(e)}


# Executar launcher
def run_launcher():
    api = LauncherAPI()
    webview.create_window(
        title="Assinatura Digital",
        html=LAUNCHER_HTML,
        js_api=api,
        width=460,
        height=460,
        resizable=False,
        on_top=False,
    )
    webview.start()


def _setup_playwright_path():
    if not getattr(sys, "frozen", False):
        return

    exe_dir = os.path.dirname(sys.executable)
    exe_browsers = os.path.join(exe_dir, "browsers")
    if os.path.isdir(exe_browsers):
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = exe_browsers
        return

    fallback = os.path.join(
        os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
        "AssinarDocumento", "browsers",
    )
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = fallback
    os.makedirs(fallback, exist_ok=True)


def _get_geolocation() -> dict:
    try:
        import urllib.request, json
        with urllib.request.urlopen("https://ipapi.co/json/", timeout=5) as r:
            data = json.loads(r.read())
            return {"latitude": float(data["latitude"]), "longitude": float(data["longitude"])}
    except Exception:
        return {"latitude": -23.5505, "longitude": -46.6333}  # São Paulo


def _instalar_chromium():
    try:
        from playwright._impl._driver import compute_driver_executable
        driver_exec, _ = compute_driver_executable()
        subprocess.run([str(driver_exec), "install", "chromium"], check=False)
    except Exception:
        pass


def run_browser(url: str, device_name: str):
    """Abre janela mobile"""
    import threading
    from playwright.sync_api import sync_playwright

    _setup_playwright_path()

    pw_device = PLAYWRIGHT_DEVICES.get(device_name, "iPhone 13")

    LAUNCH_ARGS = [
        "--disable-blink-features=AutomationControlled",
        "--use-fake-device-for-media-stream",  # cria câmera/microfone fake
        "--use-fake-ui-for-media-stream",       # concede permissão automaticamente
    ]

    with sync_playwright() as p:
        if pw_device not in p.devices:
            pw_device = "iPhone 13"

        if not os.path.exists(p.chromium.executable_path):
            _instalar_chromium()

        if not os.path.exists(p.chromium.executable_path):
            import tkinter.messagebox as mb
            mb.showerror(
                "Navegador não encontrado",
                "Não foi possível instalar o Chromium automaticamente.\n\n"
                "Verifique sua conexão com a internet e tente novamente.",
            )
            return

        try:
            browser = p.chromium.launch(headless=False, args=LAUNCH_ARGS)
        except Exception as err:
            import tkinter.messagebox as mb
            mb.showerror(
                "Erro ao abrir navegador",
                f"Não foi possível iniciar o Chromium.\n\nDetalhe: {err}",
            )
            return

        context = browser.new_context(
            **p.devices[pw_device],
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
            permissions=["camera", "microphone", "geolocation"],
            geolocation=_get_geolocation(),
        )
        context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
        )
        page = context.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30_000)
        except Exception:
            pass

        try:
            page.wait_for_event("close", timeout=0)
        except Exception:
            pass
        finally:
            try:
                browser.close()
            except Exception:
                pass


# Entry Point
if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "--browser":
        run_browser(url=sys.argv[2], device_name=sys.argv[3])
    else:
        run_launcher()
