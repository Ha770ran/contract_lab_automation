# pdf_generators_laboral/termino_indefinido_pdf.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
import os

def generar_pdf_termino_indefinido(datos):
    """
    Genera un archivo PDF para un Contrato Individual de Trabajo a Término Indefinido.

    Args:
        datos (dict): Un diccionario con los datos del formulario.
    """
    try:
        # --- 1. CONFIGURACIÓN DEL DOCUMENTO ---
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        output_dir = os.path.join(project_root, "pdfs_laboral")
        os.makedirs(output_dir, exist_ok=True)

        nombre_trabajador = datos.get('contractor_name', 'trabajador').replace(' ', '_')
        numero_contrato = datos.get('contract_number', 'SNC')
        nombre_archivo = f"Contrato_Termino_Indefinido_{numero_contrato}_{nombre_trabajador}.pdf"
        filepath = os.path.join(output_dir, nombre_archivo)

        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        
        # --- 2. ESTILOS ---
        styles = getSampleStyleSheet()
        style_body = ParagraphStyle('Body', parent=styles['BodyText'], alignment=TA_JUSTIFY, fontSize=9, leading=12)
        style_bold = ParagraphStyle('Bold', parent=style_body, fontName='Helvetica-Bold')
        style_title = ParagraphStyle('TitleCustom', parent=styles['h1'], fontName='Helvetica-Bold', fontSize=12, alignment=TA_CENTER, spaceAfter=20)
        cell_style_label = ParagraphStyle('CellLabel', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8)
        cell_style_value = ParagraphStyle('CellValue', parent=styles['Normal'], fontSize=8, wordWrap='CJK')

        # --- FUNCIÓN AUXILIAR PARA PAGINACIÓN ---
        page_number = 1
        def new_page():
            nonlocal page_number
            c.setFont("Helvetica", 8)
            c.drawString(inch, 0.75 * inch, f"Página {page_number}")
            c.showPage()
            page_number += 1
            c.setFont("Helvetica", 8)
            return height - inch

        # --- 3. PÁGINA 1: TÍTULO Y TABLA DE VARIABLES ---
        p_title = Paragraph("CONTRATO INDIVIDUAL DE TRABAJO A TÉRMINO INDEFINIDO", style_title)
        p_title.wrapOn(c, width - 2 * inch, height)
        p_title.drawOn(c, inch, height - inch * 1.2)

        # Se mantienen las 23 variables para consistencia con los otros formularios
        data_for_table = [
            [Paragraph("<b>Número de Contrato:</b>", cell_style_label), Paragraph(datos.get('contract_number', ''), cell_style_value)],
            [Paragraph("<b>Fecha del Contrato:</b>", cell_style_label), Paragraph(datos.get('contract_date', ''), cell_style_value)],
            [Paragraph("<b>Nombre del Empleador:</b>", cell_style_label), Paragraph(datos.get('employer_name', ''), cell_style_value)],
            [Paragraph("<b>NIT del Empleador:</b>", cell_style_label), Paragraph(datos.get('employer_nit', ''), cell_style_value)],
            [Paragraph("<b>Representante Legal:</b>", cell_style_label), Paragraph(datos.get('legal_representative', ''), cell_style_value)],
            [Paragraph("<b>Cédula Rep. Legal:</b>", cell_style_label), Paragraph(datos.get('legal_representative_id', ''), cell_style_value)],
            [Paragraph("<b>Dirección del Empleador:</b>", cell_style_label), Paragraph(datos.get('employer_address', ''), cell_style_value)],
            [Paragraph("<b>Nombre del Trabajador:</b>", cell_style_label), Paragraph(datos.get('contractor_name', ''), cell_style_value)],
            [Paragraph("<b>Cédula del Trabajador:</b>", cell_style_label), Paragraph(datos.get('contractor_id', ''), cell_style_value)],
            [Paragraph("<b>Lugar Nacimiento:</b>", cell_style_label), Paragraph(datos.get('city_birth', ''), cell_style_value)],
            [Paragraph("<b>Fecha Nacimiento:</b>", cell_style_label), Paragraph(datos.get('date_birth', ''), cell_style_value)],
            [Paragraph("<b>Dirección del Trabajador:</b>", cell_style_label), Paragraph(datos.get('contractor_address', ''), cell_style_value)],
            [Paragraph("<b>Teléfono del Trabajador:</b>", cell_style_label), Paragraph(datos.get('contractor_phone', ''), cell_style_value)],
            [Paragraph("<b>Email del Trabajador:</b>", cell_style_label), Paragraph(datos.get('contractor_email', ''), cell_style_value)],
            [Paragraph("<b>Contacto de Emergencia:</b>", cell_style_label), Paragraph(datos.get('name_number_emergency', ''), cell_style_value)],
            [Paragraph("<b>Cargo del Trabajador:</b>", cell_style_label), Paragraph(datos.get('workers_position', ''), cell_style_value)],
            [Paragraph("<b>Actividad a Realizar:</b>", cell_style_label), Paragraph(datos.get('activity', ''), cell_style_value)],
            [Paragraph("<b>Duración del Contrato:</b>", cell_style_label), Paragraph("INDEFINIDO", cell_style_value)], # Valor fijo para este contrato
            [Paragraph("<b>Fecha de Inicio:</b>", cell_style_label), Paragraph(datos.get('start_date', ''), cell_style_value)],
            [Paragraph("<b>Nombre del Proyecto o Centro de Costos:</b>", cell_style_label), Paragraph(datos.get('project_name', ''), cell_style_value)],
            [Paragraph("<b>Lugar de Ejecución:</b>", cell_style_label), Paragraph(datos.get('project_city', ''), cell_style_value)],
            [Paragraph("<b>Salario Mensual:</b>", cell_style_label), Paragraph(datos.get('salary', ''), cell_style_value)],
            [Paragraph("<b>Frecuencia de Pago:</b>", cell_style_label), Paragraph(datos.get('payment_frequency', ''), cell_style_value)],
        ]
        
        table = Table(data_for_table, colWidths=[2.3 * inch, 4.2 * inch])
        table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.darkgrey),
            ('BOX', (0,0), (-1,-1), 1.5, colors.black),
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F0F0F0')),
        ]))
        
        table.wrapOn(c, width - 2 * inch, height)
        table_height = table._height
        table.drawOn(c, inch, height - inch * 1.5 - table_height)
        
        y_position = height - inch * 2 - table_height - 40

        intro_text = "Las partes identificadas plenamente en el presente contrato laboral deciden de mutuo acuerdo, libre y voluntariamente, pactar y cumplir las siguientes condiciones contractuales, de acuerdo con la normatividad laboral colombiana."
        p_intro = Paragraph(intro_text, style_body)
        p_intro.wrapOn(c, width - 2 * inch, height)
        p_intro.drawOn(c, inch, y_position)

        y_position = new_page()

        # --- 4. CLÁUSULAS DEL CONTRATO ---
        
        def draw_paragraph(text, style):
            nonlocal y_position
            p = Paragraph(text, style)
            p_width, p_height = p.wrapOn(c, width - 2 * inch, y_position)
            if p_height > y_position - inch:
                y_position = new_page()
            p.drawOn(c, inch, y_position - p_height)
            y_position -= (p_height + 10)

        draw_paragraph(f"Entre el <b>EMPLEADOR</b> ({datos.get('employer_name','')}) y el <b>TRABAJADOR</b> ({datos.get('contractor_name','')}), de las condiciones mencionadas en el cuadro general al inicio del contrato, las partes identificadas como aparecen al pie de sus firmas, se ha celebrado el presente contrato individual de trabajo a término indefinido, regido además por las siguientes cláusulas:", style_body)
        
        clausulas = [
            ("PRIMERA: OBJETO.", "El TRABAJADOR se compromete a colocar al servicio del empleador toda su capacidad normal de trabajo, en forma exclusiva y personal, en el desempeño de las funciones que se le asignen, y especialmente las relacionadas con el cargo y en las labores anexas y complementarias del mismo, de conformidad con las leyes, los reglamentos, las órdenes y las instrucciones generales o particulares que se le impartan, observando en su desempeño la buena fe, el cuidado y diligencia necesarios."),
            ("SEGUNDA: DURACIÓN DEL CONTRATO.", "El presente contrato de trabajo es a término indefinido, pero podrá darse por terminado por cualquiera de las partes, cumpliendo con las exigencias y formalidades que la ley laboral colombiana ha establecido para el efecto."),
            ("TERCERA: PERÍODO DE PRUEBA.", "El presente contrato queda sujeto a un período de prueba de dos (2) meses contados a partir de la fecha de la iniciación de la relación laboral, plazo durante el cual cualquiera de las partes podrá darlo por terminado unilateralmente sin previo aviso y sin lugar al pago de indemnización."),
            ("CUARTA: LUGAR DE PRESTACIÓN DEL SERVICIO.", f"El servicio antedicho lo prestará EL TRABAJADOR en el lugar determinado en el cuadro general del presente contrato ({datos.get('project_city', '')}). En todo caso, EL EMPLEADOR queda facultado para trasladar a EL TRABAJADOR a otras ciudades u oficios y asignarle otras funciones, siempre y cuando tales cambios y traslados no impliquen desmejora de las condiciones laborales de EL TRABAJADOR. Los gastos que se originen con el traslado serán cubiertos por EL EMPLEADOR."),
            ("QUINTA: JORNADA DE TRABAJO.", "EL TRABAJADOR laborará durante las horas diarias que como jornada ordinaria le señale EL EMPLEADOR de acuerdo con el Reglamento Interno de Trabajo, sin exceder las horas semanales establecidas en la Ley 2101 de 2021 que este aplicando el EMPLEADOR. La labor en tiempo suplementario, siempre que le haya sido previamente autorizado por LA EMPRESA, le será cubierta a la tarifa legal definida por la ley colombiana."),
            ("SEXTA: SALARIO.", f"El salario determinado en el cuadro general al inicio del presente contrato ({datos.get('salary', '')}) fue acordado voluntaria y conscientemente por las partes, y cumple con todas las condiciones laborales, incluyendo todas las prestaciones sociales que por ley se estipulen.<br/><br/><b>PARÁGRAFO PRIMERO: SEGURIDAD SOCIAL.</b> - EL EMPLEADOR pagará la parte que le corresponda de las cotizaciones al sistema de seguridad social en pensiones, salud y riesgos profesionales, igualmente podrá descontar a EL EMPLEADO la parte de las cotizaciones que por ley a él le corresponde sufragar."),
            ("SEPTIMA: OBLIGACIONES DEL TRABAJADOR.", "El trabajador se obliga a: 1. A no atender durante las horas de trabajo ocupaciones o asuntos diferentes a los que le encomiende EL EMPLEADOR. 2. Abstenerse de cualquier actitud en los compromisos comerciales, personales o en las relaciones sociales, que pueda afectar en forma nociva la reputación del empleador. 3. No solicitar préstamos especiales o ayuda económica a los clientes del empleador aprovechándose de su cargo u oficio o aceptarles donaciones de cualquier clase sin la previa autorización escrita del empleador. 4. No retirar de las instalaciones donde funcione la empresa elementos, máquinas y útiles de propiedad del empleador sin su autorización escrita. 5. No presentar cuentas de gastos ficticias o reportar como cumplidas visitas o tareas no efectuadas. 6. No autorizar o ejecutar sin ser de su competencia, operaciones que afecten los intereses del empleador o negociar bienes y/o mercancías del empleador en provecho propio. 7. No retener dinero o hacer efectivos cheques recibidos para el empleador. 8. Utilizar adecuadamente los implementos de seguridad que EL EMPLEADOR tenga establecidos como tal. 9. A trabajar todo el tiempo que sea necesario para cumplir cabalmente sus deberes. 10. A prestar sus servicios en cualquier otro empleo, cargo u oficio a donde lo promueva EL EMPLEADOR, ya sea en la sede inicial del trabajo o en cualquier otra, donde desarrolle su objeto social; dentro de su poder subordinante, siempre que se respeten las condiciones laborales EL EMPLEADO y no se le causen perjuicios. 11. A guardar confidencialidad sobre todo a la vinculación laboral y sobre la información a la cual tenga acceso por el desempeño de sus funciones. 12. A no ofrecer sus servicios o experiencia profesional a título personal, en competencia con los servicios o productos que presta o fabrique EL EMPLEADOR. 13. A no prestar directa e indirectamente sus servicios laborales a otros empleadores, sin autorización. 14. A no utilizar los recursos humanos, físicos, financieros e información en general de EL EMPLEADOR para beneficio propio o de terceros. 15. Aplicar las políticas, los reglamentos, las normas y procedimientos de EL EMPLEADOR. 16. Asistir a las capacitaciones a las que sea enviado por EL EMPLEADOR. 17. Sólo instalar software que cuenten con la debida licencia de uso en los computadores de la empresa. 18. No dar a conocer a personas no autorizadas la clave personal de acceso a los sistemas de cómputo de EL EMPLEADOR. 19. Cumplir con el RIT, Manuales, directrices, politicas y demas documentos de conducta y desarrollo de funciones emitidos por el empleador, y que el TRABAJADOR reconoce ser conocidos. 20. A cumplir las ordenes impartidas por su jefe y el personal de seguridad y salud en el trabajo. La violación de cualquiera de estas obligaciones será considerada como grave para efectos de la terminación unilateral del presente contrato de trabajo con justa causa."),
            ("OCTAVA: DERECHOS Y DEBERES.", "Al TRABAJADOR se le aplicarán los derechos y deberes establecidos en el Código Sustantivo del Trabajo Colombiano, el RIT y Directrices del empleador."),
            ("NOVENA: PAGOS NO SALARIALES.", "Los dineros que el TRABAJADOR reciba ocasionalmente o por mera liberalidad, por concepto de primas, alimentación, viáticos, o bonificaciones no constituirán salario, ni se computarán como factor salarial de acuerdo con los artículos 15 y 16 de la Ley 50/90."),
            ("DÉCIMA: AUTORIZACIÓN DE DESCUENTOS.", "EL TRABAJADOR autoriza expresamente a EL EMPLEADOR para que, durante el desarrollo del contrato, o al finalizar el mismo, deduzca y compense de las sumas que le correspondan por concepto de salarios y prestaciones, las cantidades y saldos pendientes a su cargo y a favor de ella."),
            ("DÉCIMA PRIMERA: REGLAMENTOS.", "Hace parte de este contrato el reglamento interno del trabajo, manual de funciones y procesos establecidos para el cargo, indicaciones del personal de SST, y directrices del empleador."),
            ("DÉCIMA SEGUNDA: DOMICILIO Y NOTIFICACIONES.", "EI TRABAJADOR declara y acepta que la dirección y correo electrónico suministrados en el presente contrato es su domicilio principal, y que a dichas direcciones se le puede enviar cualquier correspondencia o notificación que fuere necesaria. El trabajador se compromete a informar por escrito cualquier cambio de dirección."),
            ("DÉCIMA TERCERA: TRATAMIENTO DE DATOS.", "En virtud de la Ley 1581 de 2012, el trabajador autoriza de manera libre y voluntaria al empleador para que realice el tratamiento de sus datos personales, los cuales serán utilizados exclusivamente para fines relacionados con la gestión laboral."),
            ("DÉCIMA CUARTA: INTEGRALIDAD DEL CONTRATO.", "El presente contrato reemplaza en su integridad y deja sin efecto cualquiera otro contrato verbal o escrito celebrado entre las partes con anterioridad."),
            ("DÉCIMA QUINTA: MODIFICACIONES.", "Las modificaciones al presente contrato deberán constar por escrito en un documento anexo, firmado por las partes."),
            ("DÉCIMA SEXTA: CONFIDENCIALIDAD.", "EL TRABAJADOR se compromete a mantener en ABSOLUTA RESERVA toda información de EL EMPLEADOR y sus clientes a la que tenga acceso, y a no revelarla durante la vigencia del contrato ni después de su terminación."),
            ("DÉCIMA SEPTIMA: INTERPRETACIÓN Y CONTROVERSIAS.", "Este contrato ha sido redactado de acuerdo con la Ley y la Jurisprudencia y será interpretado de buena fe. En caso de presentarse alguna controversia, esta será sometida a la justicia ordinaria de Colombia."),
            ("DÉCIMA OCTAVA: ACEPTACIÓN.", "El presente contrato ha sido discutido libremente por las partes, las cuales aprueban todas las estipulaciones que lo conforman y en consecuencia para constancia se firma en dos o más ejemplares del mismo tenor y valor. Firman las partes:"),
        ]

        for titulo, texto in clausulas:
            draw_paragraph(f"<b>{titulo}</b> {texto}", style_body)

        # --- 5. FIRMAS ---
        if y_position < 3 * inch:
            y_position = new_page()
        
        y_position -= 1.0 * inch
        c.setFont("Helvetica", 10)
        c.drawString(1.5 * inch, y_position, "___________________________________")
        c.drawString(1.5 * inch, y_position - 15, "FIRMA DEL EMPLEADOR")
        c.drawString(1.5 * inch, y_position - 30, f"NOMBRE: {datos.get('legal_representative', datos.get('employer_name', ''))}")
        c.drawString(1.5 * inch, y_position - 45, f"C.C.: {datos.get('legal_representative_id', datos.get('employer_nit', ''))}")

        c.drawString(5 * inch, y_position, "___________________________________")
        c.drawString(5 * inch, y_position - 15, "FIRMA DEL TRABAJADOR")
        c.drawString(5 * inch, y_position - 30, f"NOMBRE: {datos.get('contractor_name', '')}")
        c.drawString(5 * inch, y_position - 45, f"C.C.: {datos.get('contractor_id', '')}")

        # --- 6. ANEXOS Y DECLARACIÓN JURAMENTADA ---
        y_position = new_page()
        draw_paragraph("<b>ANEXO 1 AL CONTRATO DE TRABAJO</b>", style_bold)
        draw_paragraph("<b>ASUNTO: REQUISITOS PARA SU VINCULACIÓN AL SISTEMA DE SEGURIDAD SOCIAL.</b>", style_bold)
        anexo_text = "Certifico que fui notificado de los requisitos para la afiliación al Sistema de Seguridad Social (EPS, AFP, CCF) y es mi responsabilidad presentar dicha documentación. En caso de no hacerlo, mi empleador queda exonerado de cualquier reclamación."
        draw_paragraph(anexo_text, style_body)
        
        draw_paragraph("<b>DECLARACIÓN JURAMENTADA DEL TRABAJADOR:</b>", style_bold)
        declaracion_text = "El trabajador declara expresamente que asistió a la charla de inducción donde se le explican el reglamento interno de trabajo, el reglamento de higiene y seguridad industrial, y las normas, procedimientos y cuidados inherentes a su cargo. De igual manera declara que recibió por parte de la empresa los elementos de protección personal requeridos y la capacitación respectiva acerca de su uso, y que está obligado a utilizarlos. Cualquier accidente de trabajo que ocurra por no utilizarlos correrá por su cuenta y riesgo."
        draw_paragraph(declaracion_text, style_body)

        y_position -= 1.0 * inch
        c.drawString(2.75 * inch, y_position, "___________________________________")
        c.drawString(2.75 * inch, y_position - 15, "FIRMA Y CÉDULA DEL TRABAJADOR")

        # --- 7. GUARDAR EL PDF ---
        c.setFont("Helvetica", 8)
        c.drawString(inch, 0.75 * inch, f"Página {page_number}")
        
        # Añadir la frase de copyright en la esquina inferior derecha de la última página
        copyright_text = "© 2015 HEBITECH. All rights reserved."
        c.setFont("Helvetica", 8) # Arial 8 solicitado, usando Helvetica como alternativa estándar
        c.drawRightString(width - inch, 0.5 * inch, copyright_text) # 0.5 inch desde el borde inferior
        
        c.save()
        print(f"✅ PDF de Contrato a Término Indefinido generado exitosamente en: {filepath}")

    except Exception as e:
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"Error al generar el PDF de Término Indefinido: {e}")
        import traceback
        print(traceback.format_exc())
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

# Ejemplo de uso:
if __name__ == '__main__':
    datos_ejemplo = {
        'contract_number': 'CI-2025-088',
        'contract_date': '2025-09-15',
        'employer_name': 'INGEURBANISMO SAS',
        'employer_nit': '900474198-8',
        'legal_representative': 'ELIANA MARIA ARBELAEZ ALZATE',
        'legal_representative_id': '1.038.407.657',
        'employer_address': 'Km 4, Vía Llanogrande - Don Diego, Rionegro',
        'contractor_name': 'Carlos Ramirez',
        'contractor_id': '71.777.888',
        'city_birth': 'Bogotá',
        'date_birth': '1985-02-10',
        'contractor_address': 'Carrera 15 # 80-20, Bogotá',
        'contractor_phone': '3118887766',
        'contractor_email': 'carlos.ramirez@example.com',
        'name_number_emergency': 'Lucia Fernandez - 3125554433',
        'workers_position': 'Director Administrativo',
        'activity': 'Coordinación general de las áreas administrativas y financieras de la compañía.',
        'project_name': 'Administración Central',
        'project_city': 'Rionegro, Antioquia',
        'salary': 'SEIS MILLONES DE PESOS M/CTE ($6.000.000)',
        'payment_frequency': 'Mensual',
        'start_date': '2025-10-01',
        # La variable 'final_time' no es necesaria aquí ya que la duración es indefinida.
        # Se omite del diccionario de ejemplo para este tipo de contrato.
    }
    generar_pdf_termino_indefinido(datos_ejemplo)