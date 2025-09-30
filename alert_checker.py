import pandas as pd
from datetime import datetime, timedelta
import os
from email_sender import send_alert_email # Importa la nueva función de alerta

# --- Configuración ---
EXCEL_FILE = "contratos_lab.xlsx"
DAYS_BEFORE_EXPIRATION = 40
# Puedes ajustar los destinatarios aquí, o leerlos de variables de entorno si se hace más complejo.
ALERT_RECIPIENTS = ["gestionhumana@ingeurbanismo.com"]
# Si también quieres notificar a técnica, descomenta la línea de abajo y ajusta el array.
# ALERT_RECIPIENTS = ["gtecnica@ingeurbanismo.com", "gestionhumana@ingeurbanismo.com"]

def check_and_send_alerts():
    """
    Verifica los contratos en el Excel y envía alertas para aquellos próximos a vencer.
    """
    print(f"[{datetime.now()}] Iniciando verificación de alertas de contratos...")

    if not os.path.exists(EXCEL_FILE):
        print(f"[{datetime.now()}] Advertencia: El archivo {EXCEL_FILE} no existe. No se pueden verificar alertas.")
        return

    try:
        df = pd.read_excel(EXCEL_FILE)
    except Exception as e:
        print(f"[{datetime.now()}] Error al leer el archivo Excel {EXCEL_FILE}: {e}")
        return

    if df.empty:
        print(f"[{datetime.now()}] El archivo {EXCEL_FILE} está vacío. No hay contratos para verificar.")
        return

    today = datetime.now().date()
    updated_df = df.copy()
    alerts_sent_count = 0

    # Asegurarse de que la columna de estado de alerta exista
    if 'Alerta_40_Dias_Enviada' not in updated_df.columns:
        updated_df['Alerta_40_Dias_Enviada'] = False
        print(f"[{datetime.now()}] Columna 'Alerta_40_Dias_Enviada' creada en el DataFrame.")

    for index, row in updated_df.iterrows():
        try:
            estimated_end_date_str = str(row.get('estimated_end_date'))
            if pd.isna(estimated_end_date_str) or estimated_end_date_str == 'NaT' or estimated_end_date_str == '':
                # print(f"[{datetime.now()}] Contrato {row.get('contract_number', 'N/A')}: Fecha final estimada no válida o ausente. Saltando.")
                continue

            # Convertir la fecha, manejando posibles formatos (solo nos interesa la parte de la fecha)
            if ' ' in estimated_end_date_str: # Si incluye hora, separar
                estimated_end_date = datetime.strptime(estimated_end_date_str.split(' ')[0], '%Y-%m-%d').date()
            elif '/' in estimated_end_date_str: # Manejar formato MM/DD/YYYY o DD/MM/YYYY si es necesario (asumiendo que viene de un input date como YYYY-MM-DD)
                 # Mejor intentar varios formatos comunes si el origen no es 100% consistente
                try:
                    estimated_end_date = datetime.strptime(estimated_end_date_str, '%Y-%m-%d').date()
                except ValueError:
                    try:
                        estimated_end_date = datetime.strptime(estimated_end_date_str, '%m/%d/%Y').date()
                    except ValueError:
                        estimated_end_date = datetime.strptime(estimated_end_date_str, '%d/%m/%Y').date()
            else: # Asumir YYYY-MM-DD
                estimated_end_date = datetime.strptime(estimated_end_date_str, '%Y-%m-%d').date()
            
            days_left = (estimated_end_date - today).days
            alert_already_sent = row.get('Alerta_40_Dias_Enviada', False)

            if DAYS_BEFORE_EXPIRATION >= days_left > 0 and not alert_already_sent:
                print(f"[{datetime.now()}] Alerta detectada para contrato {row.get('contract_number', 'N/A')} de {row.get('contractor_name', 'N/A')}. Faltan {days_left} días.")
                # Envía el correo de alerta
                contract_data_for_alert = row.to_dict()
                send_alert_email(contract_data_for_alert, ALERT_RECIPIENTS, days_left)
                updated_df.loc[index, 'Alerta_40_Dias_Enviada'] = True # Marca como enviada
                alerts_sent_count += 1
            elif days_left <= 0 and alert_already_sent: # Si el contrato ya venció y la alerta se envió, resetear la alerta
                 updated_df.loc[index, 'Alerta_40_Dias_Enviada'] = False
                 # print(f"[{datetime.now()}] Contrato {row.get('contract_number', 'N/A')} vencido, alerta reseteada.")
            
        except Exception as e:
            print(f"[{datetime.now()}] Error procesando contrato {row.get('contract_number', 'N/A')}: {e}")

    if alerts_sent_count > 0:
        try:
            updated_df.to_excel(EXCEL_FILE, index=False) # Guarda el DataFrame actualizado
            print(f"[{datetime.now()}] {alerts_sent_count} alertas enviadas y el archivo Excel {EXCEL_FILE} ha sido actualizado.")
        except Exception as e:
            print(f"[{datetime.now()}] Error al guardar el archivo Excel actualizado: {e}")
    else:
        print(f"[{datetime.now()}] No se encontraron nuevas alertas de contratos para enviar.")

    print(f"[{datetime.now()}] Verificación de alertas de contratos finalizada.")

if __name__ == '__main__':
    check_and_send_alerts()
