@echo off
chcp 65001 > nul
setlocal

set APP_NAME=AssinarDocumento
set INSTALL_DIR=%LOCALAPPDATA%\%APP_NAME%
set DESKTOP=%USERPROFILE%\Desktop
set STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs

echo.
echo ============================================
echo   Instalando: Assinatura Digital
echo ============================================
echo.

if not exist "AssinarDocumento.exe" (
    if exist "dist\AssinarDocumento.exe" (
        echo AVISO: Voce executou o instalador na pasta do codigo-fonte.
        echo Redirecionando automaticamente para o instalador na pasta dist\...
        echo.
        pushd dist
        call instalar.bat
        popd
        exit /b 0
    )
    echo ERRO: AssinarDocumento.exe nao encontrado.
    if exist "build.bat" (
        echo.
        echo ===============================================================
        echo  VOCE ESTA NA PASTA DO CODIGO-FONTE!
        echo  O aplicativo ainda nao foi compilado no seu computador.
        echo.
        echo  PASSO A PASSO PARA RESOLVER:
        echo  1. Execute primeiro o arquivo: build.bat
        echo  2. Aguarde a compilacao terminar (sera gerada a pasta dist\)
        echo  3. Acesse a pasta dist\ e execute o instalar.bat de la!
        echo ===============================================================
    ) else (
        echo Execute este instalador a partir da pasta do pacote distribuido.
    )
    echo.
    pause & exit /b 1
)

:: Cria diretorio de instalacao
echo [1/4] Criando pasta de instalacao...
echo   %INSTALL_DIR%
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
echo     OK

:: Copia o executavel principal
echo.
echo [2/4] Copiando executavel...
copy /Y "AssinarDocumento.exe" "%INSTALL_DIR%\AssinarDocumento.exe" > nul
echo     OK

:: Copia o Chromium (browsers/)
echo.
echo [3/4] Copiando navegador (Chromium)...
if exist "browsers\" (
    xcopy "browsers" "%INSTALL_DIR%\browsers\" /E /I /Q /Y > nul
    echo     OK
) else (
    echo     AVISO: pasta browsers\ nao encontrada.
    echo     O navegador sera baixado automaticamente na primeira execucao (~150MB).
)

:: Cria atalho na area de trabalho
echo.
echo [4/4] Criando atalhos...
powershell -NoProfile -Command ^
    "$d = [Environment]::GetFolderPath('Desktop'); ^
     $s = New-Object -COM WScript.Shell; ^
     $sc = $s.CreateShortcut($d + '\Assinar Documento.lnk'); ^
     $sc.TargetPath = '%INSTALL_DIR%\AssinarDocumento.exe'; ^
     $sc.WorkingDirectory = '%INSTALL_DIR%'; ^
     $sc.IconLocation = '%INSTALL_DIR%\AssinarDocumento.exe,0'; ^
     $sc.Description = 'Assinatura Digital - Trustic'; ^
     $sc.Save()"

:: Cria atalho no Menu Iniciar
powershell -NoProfile -Command ^
    "$s = New-Object -COM WScript.Shell; ^
     $sc = $s.CreateShortcut('%STARTMENU%\Assinar Documento.lnk'); ^
     $sc.TargetPath = '%INSTALL_DIR%\AssinarDocumento.exe'; ^
     $sc.WorkingDirectory = '%INSTALL_DIR%'; ^
     $sc.IconLocation = '%INSTALL_DIR%\AssinarDocumento.exe,0'; ^
     $sc.Description = 'Assinatura Digital - Trustic'; ^
     $sc.Save()"

echo     OK

echo.
echo ============================================
echo   INSTALACAO CONCLUIDA!
echo.
echo   Local: %INSTALL_DIR%
echo   Atalho criado na area de trabalho.
echo   Atalho criado no Menu Iniciar.
echo ============================================
echo.
pause
