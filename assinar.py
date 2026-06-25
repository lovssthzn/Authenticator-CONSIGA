import sys
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

URL_PADRAO = "https://www.google.com"

# Dispositivos
DEVICES = {
    "iphone13":  "iPhone 13",
    "pixel5":    "Pixel 5",
    "galaxys21": "Galaxy S21",
}


def abrir_assinatura(url: str, device_key: str = "iphone13"):
    device_name = DEVICES.get(device_key, "iPhone 13")

    print(f"\n  Abrindo: {url}")
    print(f"  Dispositivo emulado: {device_name}")
    print("  Aguardando interação manual...\n")
    print("  Pressione ENTER aqui para encerrar após assinar.\n")

    with sync_playwright() as p:
        device = p.devices[device_name]

        browser = p.chromium.launch(
            headless=False,
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled",
            ],
        )

        context = browser.new_context(
            **device,
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
        )

        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        page = context.new_page()

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30_000)
        except PlaywrightTimeout:
            print("  [aviso] Timeout no carregamento, mas a página pode estar OK.")

        print(f"  URL atual: {page.url}")
        print("  Browser aberto. Realize a assinatura normalmente na janela.")

        input()

        print("  Encerrando...")
        browser.close()

    print("  Concluído.\n")


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else URL_PADRAO
    abrir_assinatura(url)
