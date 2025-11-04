@echo off
REM 🚀 SCRIPT PARA RODAR A APLICAÇÃO NO WINDOWS

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║     🚀 INICIANDO SISTEMA DE AGENDAMENTOS 🚀       ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM Verificar se credentials.json existe
if not exist "credentials.json" (
    echo ⚠️  AVISO: Arquivo 'credentials.json' não encontrado!
    echo.
    echo Para usar em DESENVOLVIMENTO:
    echo   1. Baixe credentials.json do Google Cloud Console
    echo   2. Coloque na pasta: %cd%\credentials.json
    echo.
    echo Para PRODUÇÃO, configure:
    echo   set GOOGLE_CREDENTIALS_JSON=seu-json-aqui
    echo.
    set /p confirm="Deseja continuar mesmo assim? (s/n) "
    if /i not "%confirm%"=="s" (
        echo Abortado.
        pause
        exit /b 1
    )
)

REM Verificar se as dependências estão instaladas
echo 📌 Verificando dependências...
python -m pip show flask >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Flask não está instalado. Instalando dependências...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Erro ao instalar dependências!
        pause
        exit /b 1
    )
)

echo.
echo ✅ Tudo pronto!
echo.
echo 🚀 Iniciando aplicação...
echo 📱 Acesse: http://localhost:5000
echo.
echo 💡 Dicas:
echo    - Pressione CTRL+C para parar
echo    - Consulte LEIA-ME-PRIMEIRO.txt para mais informações
echo.

REM Rodar a aplicação
python app.py

REM Se chegou aqui, significa que app.py encerrou
if errorlevel 1 (
    echo.
    echo ❌ Erro ao iniciar a aplicação!
    echo 💡 Verifique:
    echo    1. Se credentials.json está na pasta correta
    echo    2. Se todas as dependências estão instaladas
    echo    3. Consulte CONFIGURAR_CREDENCIAIS.md
    echo.
    pause
    exit /b 1
)

pause
