# app_laboral.py
# Este es el archivo principal de la aplicación Flask para generar contratos laborales.

from flask import Flask, render_template, request, redirect
import pandas as pd
import os

# funcion de cada archivo pdf:

from pdf_generators_lab.obra_labor_pdf import generar_pdf_obra_labor
#from pdf_generators_lab.prestacion_servicios_pdf import generar_pdf_prestacion_servicios_laboral
from pdf_generators_lab.termino_fijo_pdf import generar_pdf_termino_fijo
from pdf_generators_lab.termino_indefinido_pdf import generar_pdf_termino_indefinido
#from pdf_generators_lab.teletrabajo_pdf import generar_pdf_teletrabajo
from email_sender import send_contract_email

app = Flask(__name__)

# Ruta principal - pagina principal
@app.route("/")
def index():
    return render_template("index_laboral.html")

# --- Rutas para mostrar formularios ---
@app.route("/contrato-laboral/obra-labor")
def form_obra_labor(): 
    """Muestra el formulario para el Contrato de Prestación de Servicios."""
    return render_template("form_obra_labor.html")

#@app.route("/contrato-laboral/prestacion-servicios")
#def form_prestacion_servicios():
    """Muestra el formulario para el Contrato de Prestación de Servicios."""
    return render_template("form_prestacion_servicios.html")

@app.route("/contrato-laboral/termino-fijo")
def form_termino_fijo():
    """Muestra el formulario para el Contrato a Término Fijo."""
    return render_template("form_termino_fijo.html")

@app.route("/contrato-laboral/termino-indefinido")
def form_termino_indefinido():
    """Muestra el formulario para el Contrato a Término Indefinido."""
    return render_template("form_termino_indefinido.html")

#@app.route("/contrato-laboral/teletrabajo")
#def form_teletrabajo():
    """Muestra el formulario para el Contrato de Teletrabajo."""
    return render_template("form_teletrabajo.html")


# --- RUTA PARA LISTAR LOS CONTRATOS GENERADOS ---

@app.route("/lista-contratos-laborales")
def lista_contratos_laborales():
    """Lee y muestra los datos de los contratos laborales desde un archivo Excel."""
    excel_file = "contratos_lab.xlsx"
    if os.path.exists(excel_file):
        try:
            df = pd.read_excel(excel_file)
            if df.empty:
                return "El archivo de contratos laborales está vacío."
            df = df.fillna('') 
            return render_template("tabla_contratos_laborales.html", data=df.to_dict(orient="records"))
        except Exception as e:
            return f"Error al leer el archivo Excel: {e}"
    return "No hay contratos laborales registrados o el archivo no existe."


# --- RUTAS PARA PROCESAR FORMULARIOS Y CREAR LOS PDFs ---

def procesar_y_guardar_contrato(datos, tipo_contrato, funcion_pdf):
    """Función auxiliar para procesar datos, generar PDF y guardar en Excel."""
    datos['tipo_contrato'] = tipo_contrato
    
    # Llama a la función específica para generar el PDF
    funcion_pdf(datos)

    # Guarda los datos en un archivo Excel específico para contratos laborales
    excel_file = "contratos_lab.xlsx"
    try:
        df_excel = pd.read_excel(excel_file) if os.path.exists(excel_file) else pd.DataFrame()
    except Exception as e:
        print(f"Error al leer {excel_file}: {e}. Se creará uno nuevo.")
        df_excel = pd.DataFrame()
        
    df_new_row = pd.DataFrame([datos])
    df_final = pd.concat([df_excel, df_new_row], ignore_index=True)
    df_final.to_excel(excel_file, index=False)
    print(f"Contrato '{tipo_contrato}' guardado en {excel_file}")

    # Enviar correo electrónico
    recipients = ["gtecnica@ingeurbanismo.com", "gestionhumana@ingeurbanismo.com"]
    send_contract_email(datos, recipients)

@app.route("/create/obra-labor", methods=["POST"])
def create_obra_labor():
    datos = request.form.to_dict()
    # Cuando tengas el generador real, cambia 'generar_pdf_temporal' por 'generar_pdf_obra_labor'
    procesar_y_guardar_contrato(datos, "Obra o Labor", generar_pdf_obra_labor)
    return redirect("/")

#@app.route("/create/prestacion-servicios", methods=["POST"])
#def create_prestacion_servicios():
    datos = request.form.to_dict()
    # Cambia 'generar_pdf_temporal' por 'generar_pdf_prestacion_servicios_laboral'
    procesar_y_guardar_contrato(datos, "Prestación de Servicios", generar_pdf_temporal)
    return redirect("/")

@app.route("/create/termino-fijo", methods=["POST"])
def create_termino_fijo():
    datos = request.form.to_dict()
    # Cambia 'generar_pdf_temporal' por 'generar_pdf_termino_fijo'
    procesar_y_guardar_contrato(datos, "Término Fijo", generar_pdf_termino_fijo)
    return redirect("/")

@app.route("/create/termino-indefinido", methods=["POST"])
def create_termino_indefinido():
    datos = request.form.to_dict()
    # Cambia 'generar_pdf_temporal' por 'generar_pdf_termino_indefinido'
    procesar_y_guardar_contrato(datos, "Término Indefinido", generar_pdf_termino_indefinido)
    return redirect("/")

#@app.route("/create/teletrabajo", methods=["POST"])
#def create_teletrabajo():
    datos = request.form.to_dict()
    # Cambia 'generar_pdf_temporal' por 'generar_pdf_teletrabajo'
    procesar_y_guardar_contrato(datos, "Teletrabajo", generar_pdf_temporal)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)