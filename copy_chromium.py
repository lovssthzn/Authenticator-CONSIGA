import os, shutil, glob, sys

pw_dir = os.path.join(os.environ['LOCALAPPDATA'], 'ms-playwright')
dest_base = os.path.join(os.getcwd(), 'dist', 'browsers')

matches = glob.glob(os.path.join(pw_dir, 'chromium-*', 'chrome-win64', 'chrome.exe'))
if not matches:
    print('AVISO: Chromium nao encontrado em ms-playwright. Instale com: python -m playwright install chromium')
    sys.exit(0)

chromium_dirs = sorted(set(os.path.dirname(os.path.dirname(m)) for m in matches))
latest = chromium_dirs[-1]
name = os.path.basename(latest)
dest = os.path.join(dest_base, name)
print(f'  Copiando {name}...')
shutil.copytree(latest, dest, dirs_exist_ok=True)
print('  OK')
