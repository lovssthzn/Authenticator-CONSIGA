@echo off
chcp 65001 > nul
echo.
echo ============================================
echo   Build: Assinatura Digital (.exe)
echo ============================================
echo.

echo [1/4] Instalando dependencias Python...
python -m pip install pywebview playwright pyinstaller
python -m playwright install chromium
if %errorlevel% neq 0 (
    echo ERRO: falha ao instalar dependencias.
    pause & exit /b 1
)
echo     OK

echo.
echo [2/4] Gerando executavel...
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name "AssinarDocumento" ^
    --collect-all webview ^
    --collect-all playwright ^
    --hidden-import webview.platforms.winforms ^
    --hidden-import webview.platforms.edgechromium ^
    --noconfirm ^
    interface.py

if %errorlevel% neq 0 (
    echo.
    echo ERRO: falha no PyInstaller.
    pause & exit /b 1
)

echo.
echo [3/4] Copiando Chromium para o pacote...
python copy_chromium.py
if %errorlevel% neq 0 (
    echo AVISO: falha ao copiar Chromium. Verifique se python -m playwright install chromium foi executado.
)

echo.
echo [4/4] Copiando instalador para dist\...
copy /Y instalar.bat dist\instalar.bat > nul

echo.
echo Limpando arquivos temporarios...
if exist build rmdir /s /q build
if exist AssinarDocumento.spec del /q AssinarDocumento.spec

echo.
echo ============================================
echo   PRONTO! Pacote de distribuicao:
echo.
echo   dist\
echo   ├── AssinarDocumento.exe   (app principal)
echo   ├── browsers\              (Chromium - incluso)
echo   └── instalar.bat           (instalador)
echo.
echo   Distribua a pasta dist\ completa.
echo   Em cada maquina, executar instalar.bat
echo ============================================
echo.
pause
