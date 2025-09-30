@echo off
REM Cambia al directorio donde está este archivo .bat
cd C:\Users\hebii\OneDrive\Desktop\Proyectos\contract_lab_automation

REM Si no existe el entorno virtual, lo crea
if not exist venv (
    python -m venv venv
)

REM Establece las variables de entorno para Gmail
set GMAIL_SENDER_EMAIL=contratacionempresarial.ing@gmail.com
set GMAIL_APP_PASSWORD=kkkkkkkkkk

REM Activa el entorno virtual
call .\venv\Scripts\activate

REM Ejecuta la aplicación principal
start "" python app_laboral.py

REM Espera unos segundos para que el servidor arranque (ajusta si es necesario)
timeout /t 3 /nobreak > NUL

REM Abre la página web en el navegador predeterminado
start "" http://127.0.0.1:5000

REM Mantiene la ventana abierta para ver mensajes (opcional)
pause
