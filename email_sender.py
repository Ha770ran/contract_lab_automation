import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_contract_email(contract_data: dict, recipients: list):
    """
    Envía un correo electrónico con los datos del contrato generado.

    Args:
        contract_data (dict): Un diccionario con los datos del contrato.
        recipients (list): Una lista de direcciones de correo electrónico de los destinatarios.
    """
    sender_email = os.getenv("GMAIL_SENDER_EMAIL")
    sender_app_password = os.getenv("GMAIL_APP_PASSWORD")

    print(f"DEBUG: GMAIL_SENDER_EMAIL en el script: {sender_email}")
    print(f"DEBUG: GMAIL_APP_PASSWORD en el script: {sender_app_password}")

    if not sender_email or not sender_app_password:
        print("Advertencia: Las credenciales de Gmail no están configuradas en las variables de entorno.")
        print("Asegúrate de establecer GMAIL_SENDER_EMAIL y GMAIL_APP_PASSWORD.")
        return

    # Extraer el tipo de contrato y el nombre del trabajador para el asunto
    tipo_contrato = contract_data.get('tipo_contrato', 'Desconocido')
    nombre_trabajador = contract_data.get('contractor_name', 'Trabajador Desconocido')

    subject = f"Nuevo Contrato Laboral Generado: {tipo_contrato} - {nombre_trabajador}"

    # Construir el cuerpo del correo con las 23 variables
    body = f"""
    Estimados,

    Se ha generado un nuevo CONTRATO LABORAL con los siguientes detalles:

    <b>Número de Contrato:</b> {contract_data.get('contract_number', '')}<br/>
    <b>Fecha del Contrato:</b> {contract_data.get('contract_date', '')}<br/>
    <b>Nombre del Empleador:</b> {contract_data.get('employer_name', '')}<br/>
    <b>Nombre del Trabajador:</b> {contract_data.get('contractor_name', '')}<br/>
    <b>Cédula del Trabajador:</b> {contract_data.get('contractor_id', '')}<br/>
    <b>Lugar Nacimiento:</b> {contract_data.get('city_birth', '')}<br/>
    <b>Fecha Nacimiento:</b> {contract_data.get('date_birth', '')}<br/>
    <b>Dirección del Trabajador:</b> {contract_data.get('contractor_address', '')}<br/>
    <b>Teléfono del Trabajador:</b> {contract_data.get('contractor_phone', '')}<br/>
    <b>Email del Trabajador:</b> {contract_data.get('contractor_email', '')}<br/>
    <b>Cargo del Trabajador:</b> {contract_data.get('workers_position', '')}<br/>
    <b>Actividad a Realizar:</b> {contract_data.get('activity', '')}<br/>
    <b>Duración de la Obra:</b> {contract_data.get('final_time', '')}<br/>
    <b>Fecha de Inicio:</b> {contract_data.get('start_date', '')}<br/>
    <b>Fecha Final Estimada:</b> {contract_data.get('estimated_end_date', '')}<br/>
    <b>Nombre del Proyecto o Centro de Costos:</b> {contract_data.get('project_name', '')}<br/>
    <b>Lugar de Ejecución:</b> {contract_data.get('project_city', '')}<br/>
    <b>Salario Mensual:</b> {contract_data.get('salary', '')}<br/>
    <b>Frecuencia de Pago:</b> {contract_data.get('payment_frequency', '')}<br/>

    Por favor Gerente Tecnico confirmar la informaciòn al correo electronico de gestionhumana@ingeurbanismo.com,
.
    """

    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server: # Use 465 for SSL or 587 for TLS
            server.login(sender_email, sender_app_password)
            server.sendmail(sender_email, recipients, message.as_string())
        print(f"✅ Correo enviado exitosamente a {', '.join(recipients)}")
    except Exception as e:
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"Error al enviar el correo electrónico: {e}")
        import traceback
        print(traceback.format_exc())
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

def send_alert_email(contract_data: dict, recipients: list, days_remaining: int):
    """
    Envía un correo electrónico de alerta para contratos próximos a vencer.

    Args:
        contract_data (dict): Un diccionario con los datos del contrato.
        recipients (list): Una lista de direcciones de correo electrónico de los destinatarios.
        days_remaining (int): Número de días restantes para el vencimiento.
    """
    sender_email = os.getenv("GMAIL_SENDER_EMAIL")
    sender_app_password = os.getenv("GMAIL_APP_PASSWORD")

    if not sender_email or not sender_app_password:
        print("Advertencia: Las credenciales de Gmail no están configuradas en las variables de entorno para la alerta.")
        print("Asegúrate de establecer GMAIL_SENDER_EMAIL y GMAIL_APP_PASSWORD.")
        return

    nombre_trabajador = contract_data.get('contractor_name', 'Trabajador Desconocido')
    numero_contrato = contract_data.get('contract_number', 'SNC')

    subject = f"ALERTA: Contrato {numero_contrato} de {nombre_trabajador} vence en {days_remaining} días."

    body = f"""
    Estimados,

    Se informa que el contrato laboral del trabajador <b>{nombre_trabajador}</b> (C.C. {contract_data.get('contractor_id', '')}) 
    con número de contrato <b>{numero_contrato}</b> tiene una fecha final estimada de <b>{contract_data.get('estimated_end_date', '')}</b>. 
    Faltan aproximadamente <b>{days_remaining} días</b> para su vencimiento.

    Detalles del contrato:
    <ul>
        <li><b>Tipo de Contrato:</b> {contract_data.get('tipo_contrato', '')}</li>
        <li><b>Fecha de Inicio:</b> {contract_data.get('start_date', '')}</li>
        <li><b>Cargo:</b> {contract_data.get('workers_position', '')}</li>
        <li><b>Nombre del Proyecto:</b> {contract_data.get('project_name', '')}</li>
        <li><b>Salario:</b> {contract_data.get('salary', '')}</li>
    </ul>

    Por favor, tomar las acciones correspondientes.

    Saludos cordiales,
    Su sistema de automatización de contratos.
    """

    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_app_password)
            server.sendmail(sender_email, recipients, message.as_string())
        print(f"✅ Correo de ALERTA enviado exitosamente a {', '.join(recipients)}")
    except Exception as e:
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"Error al enviar el correo de alerta: {e}")
        import traceback
        print(traceback.format_exc())
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

if __name__ == '__main__':
    # Ejemplo de uso para probar la función (esto no se ejecutará en la app principal)
    example_data = {
        'tipo_contrato': 'Obra o Labor',
        'contract_number': '001',
        'contract_date': '2023-10-26',
        'employer_name': 'Ejemplo S.A.S.',
        'employer_nit': '123.456.789-0',
        'legal_representative': 'Juan Pérez',
        'legal_representative_id': '100.200.300',
        'employer_address': 'Calle Ficticia 123',
        'contractor_name': 'María García',
        'contractor_id': '98.765.432',
        'city_birth': 'Bogotá',
        'date_birth': '1990-01-15',
        'contractor_address': 'Avenida Imaginaria 456',
        'contractor_phone': '3001112233',
        'contractor_email': 'maria.garcia@example.com',
        'name_number_emergency': 'Pedro García - 3004445566',
        'workers_position': 'Asistente Administrativo',
        'activity': 'Soporte administrativo y gestión documental.',
        'final_time': 'Hasta la finalización del proyecto X.',
        'start_date': '2023-11-01',
        'estimated_end_date': '2024-12-31',
        'project_name': 'Proyecto Alpha',
        'project_city': 'Medellín',
        'salary': 'DOS MILLONES DE PESOS M/CTE ($2.000.000)',
        'payment_frequency': 'Mensual',
    }
    # recipients_list = ["gtecnica@ingeurbanismo.com", "gestionhumana@ingeurbanismo.com"]
    # send_contract_email(example_data, recipients_list)
    # send_alert_email(example_data, ["gestionhumana@ingeurbanismo.com"], 40)
