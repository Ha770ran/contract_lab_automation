[README.md](https://github.com/user-attachments/files/22643265/README.md)
# CONTRACT_LAB_AUTOMATION

Este proyecto es una aplicación web local diseñada para automatizar la generación de contratos laborales (Obra o Labor, Término Fijo, Término Indefinido). La aplicación permite a los usuarios ingresar datos a través de formularios web, generar documentos PDF personalizados, almacenar los detalles del contrato en un archivo Excel, y enviar notificaciones automáticas por correo electrónico a los equipos relevantes. Además, incluye un sistema de alertas para notificar sobre contratos próximos a vencer.

## 🚀 Funcionalidades Principales

*   **Generación de Contratos PDF:** Crea contratos individuales de trabajo por Obra o Labor, Término Fijo, y Término Indefinido (este último si se activa en `app_laboral.py`).
*   **Formularios Web Dinámicos:** Interfaz intuitiva para la entrada de datos de empleadores y trabajadores.
*   **Registro de Contratos en Excel:** Almacena automáticamente los datos de cada contrato generado en `contratos_lab.xlsx`.
*   **Envío de Notificaciones por Correo:** Envía un correo electrónico con los detalles del contrato recién generado a direcciones específicas (ej. `gtecnica@ingeurbanismo.com`, `gestionhumana@ingeurbanismo.com`).
*   **Sistema de Alertas de Vencimiento:** Un script programable verifica periódicamente los contratos en Excel y envía alertas por correo electrónico si un contrato está próximo a su `Fecha Final Estimada` (40 días antes).
*   **Copyright Personalizado:** Incluye una frase de copyright `© 2015 HEBITECH. All rights reserved.` en la última página de todos los PDFs generados.
*   **Campo "Fecha Final Estimada":** Permite registrar una fecha interna para seguimiento sin que aparezca en el PDF final.

## 🛠️ Tecnologías Utilizadas

*   **Python 3.x**
*   **Flask:** Microframework web para la interfaz de usuario.
*   **Pandas:** Para la lectura y escritura de datos en archivos Excel.
*   **ReportLab:** Librería para la generación de documentos PDF.
*   **smtplib & email.mime:** Para el envío de correos electrónicos.

## ⚙️ Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto en tu máquina.

### 1. Requisitos Previos

*   **Python 3.x:** Asegúrate de tener Python instalado. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).
*   **Windows PowerShell:** Será tu terminal principal para la configuración y ejecución.

### 2. Clonar el Repositorio (o copiar los archivos)

Asegúrate de tener todos los archivos del proyecto en una carpeta local, por ejemplo:
`C:\Users\TuUsuario\Desktop\contract_lab_automation`

### 3. Configurar la Política de Ejecución de PowerShell (si es necesario)

Si encuentras el error `No se puede cargar el archivo ... Activate.ps1 porque la ejecución de scripts está deshabilitada`, necesitas cambiar la política de ejecución:

1.  Abre **Windows PowerShell como Administrador** (haz clic derecho en el icono y selecciona "Ejecutar como administrador").
2.  Ejecuta el siguiente comando y presiona `S` (o `Y`) cuando se te pregunte:
    ```powershell
    Set-ExecutionPolicy RemoteSigned
    ```
3.  Cierra la ventana de PowerShell de Administrador.

### 4. Preparar y Ejecutar el Entorno Virtual e Instalar Dependencias

Abre una **nueva ventana de PowerShell normal** y sigue estos comandos:

1.  **Navega al directorio del proyecto:**
    ```powershell
    cd "C:\Users\TuUsuario\Desktop\contract_lab_automation"
    ```
    (Asegúrate de reemplazar `TuUsuario` con tu nombre de usuario real).

2.  **Crea el entorno virtual (si no existe):**
    ```powersels
    python -m venv venv
    ```

3.  **Activa el entorno virtual:**
    ```powershell
    .\venv\Scripts\activate
    ```
    Deberías ver `(venv)` al principio de tu prompt.

4.  **Instala las librerías necesarias:**
    ```powershell
    pip install Flask pandas ReportLab
    ```

### 5. Configurar Credenciales de Correo Electrónico (Gmail)

Para que el envío de correos y alertas funcione, necesitas configurar un correo de Gmail y una "Contraseña de Aplicación".

1.  **Activa la Verificación en dos pasos** en tu cuenta de Google (`contratacionempresarial.ing@gmail.com`).
2.  **Genera una "Contraseña de aplicación"**:
    *   Ve a [myaccount.google.com/security](https://myaccount.google.com/security).
    *   En "Cómo inicias sesión en Google", haz clic en **Contraseñas de aplicaciones**.
    *   Selecciona "Correo" como aplicación y "Otro (nombre personalizado)" para el dispositivo (ej. "Flask Automation").
    *   Haz clic en "Generar" y **copia la contraseña de 16 caracteres** que se muestra.
    *   **¡Revoca cualquier contraseña de aplicación anterior** que hayas generado para este propósito si ya no la usas!

3.  **Actualiza `iniciar_app.bat` con tus credenciales:**
    Abre el archivo `iniciar_app.bat` en el directorio de tu proyecto y asegúrate de que estas líneas contengan tu información **sin comillas** alrededor de los valores:
    ```batch
    set GMAIL_SENDER_EMAIL=contratacionempresarial.ing@gmail.com
    set GMAIL_APP_PASSWORD=TU_CONTRASENA_DE_APLICACION_DE_16_CARACTERES
    ```
    (Reemplaza `TU_CONTRASENA_DE_APLICACION_DE_16_CARACTERES` con la que acabas de generar).

## ▶️ Ejecución del Proyecto

### Iniciar la Aplicación Web (Flask)

1.  Abre una **nueva ventana de PowerShell**.
2.  Navega al directorio del proyecto:
    ```powershell
    cd "C:\Users\TuUsuario\Desktop\contract_lab_automation"
    ```
3.  Ejecuta el script de inicio:
    ```powershell
    .\iniciar_app.bat
    ```
    Esto configurará las variables de entorno, activará el entorno virtual y lanzará la aplicación Flask en tu navegador web predeterminado (`http://127.0.0.1:5000`).

### Ejecutar el Verificador de Alertas de Contratos

El script `alert_checker.py` está diseñado para ejecutarse de forma programada.

1.  **Ejecución Manual (para pruebas):**
    Abre una **nueva ventana de PowerShell**, navega al directorio del proyecto, activa el entorno virtual (`.\venv\Scripts\activate`), y luego ejecuta:
    ```powershell
    python alert_checker.py
    ```
    Esto mostrará la salida en la terminal y enviará alertas si encuentra contratos próximos a vencer.

2.  **Configurar en el Programador de Tareas de Windows (Recomendado):**
    Para que las alertas se envíen automáticamente (ej. diariamente):
    *   Abre el **Programador de Tareas** de Windows.
    *   Haz clic en **"Crear Tarea Básica..."**.
    *   **Nombre:** `Alerta Contratos Proximos Vencer`
    *   **Desencadenador:** `Diariamente` (o la frecuencia deseada). Elige una hora (ej. 09:00 AM).
    *   **Acción:** `Iniciar un programa`.
        *   **Programa o script:** `C:\Users\TuUsuario\Desktop\contract_lab_automation\venv\Scripts\python.exe`
        *   **Agregar argumentos (opcional):** `C:\Users\TuUsuario\Desktop\contract_lab_automation\alert_checker.py`
        *   **Iniciar en (opcional):** `C:\Users\TuUsuario\Desktop\contract_lab_automation`
    *   Finaliza el asistente.

## 📝 Notas Adicionales

*   **Debug Mode:** La aplicación Flask se ejecuta en modo `Debug` (`app.run(debug=True)`). Esto es útil para desarrollo, pero se recomienda desactivarlo para entornos de producción.
*   **Archivos PDF:** Los contratos generados se guardan en la carpeta `pdfs_laboral/`.
*   **Archivo Excel:** `contratos_lab.xlsx` es crucial; asegúrate de no moverlo o renombrarlo. La columna `Alerta_40_Dias_Enviada` se usa internamente para el sistema de alertas.

---
