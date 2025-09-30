# pdf_generators_laboral/obra_labor_pdf.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
import os

def generar_pdf_obra_labor(datos):
    """
    Genera un archivo PDF para un Contrato Individual de Trabajo por Obra o Labor.

    Args:
        datos (dict): Un diccionario con los datos del formulario.
    """
    try:
        # --- 1. CONFIGURACIÓN DE RUTA (CORREGIDO) ---
        # Obtiene la ruta del directorio donde está este script (pdf_generators_laboral)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Sube un nivel para llegar a la raíz del proyecto (contract_lab_automation)
        project_root = os.path.dirname(script_dir)
        # Define el directorio de PDFs de forma segura dentro de la raíz del proyecto
        output_dir = os.path.join(project_root, "pdfs_laboral")
      
        os.makedirs(output_dir, exist_ok=True)

        # Define el nombre del archivo PDF
        nombre_trabajador = datos.get('contractor_name', 'trabajador').replace(' ', '_')
        numero_contrato = datos.get('contract_number', 'SNC')
        nombre_archivo = f"Contrato_Obra_Labor_{numero_contrato}_{nombre_trabajador}.pdf"
        filepath = os.path.join(output_dir, nombre_archivo)

        # Crea el objeto canvas
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        
        # --- 2. ESTILOS ---
        styles = getSampleStyleSheet()
        style_body = ParagraphStyle(
            'Body',
            parent=styles['BodyText'],
            alignment=TA_JUSTIFY,
            fontSize=10,
            leading=14
        )
        style_bold = ParagraphStyle(
            'Bold',
            parent=style_body,
            fontName='Helvetica-Bold'
        )
        style_title = ParagraphStyle(
            'TitleCustom',
            parent=styles['h1'],
            fontName='Helvetica-Bold',
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=20
        )
        # Estilos para la tabla de datos
        cell_style_label = ParagraphStyle('CellLabel', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8)
        cell_style_value = ParagraphStyle('CellValue', parent=styles['Normal'], fontSize=8, wordWrap='CJK')

        # --- FUNCIÓN AUXILIAR PARA PAGINACIÓN ---
        page_number = 1
        def new_page():
            nonlocal page_number
            c.setFont("Helvetica", 9)
            c.drawString(inch, 0.75 * inch, f"Página {page_number}")
            c.showPage()
            page_number += 1
            c.setFont("Helvetica", 9)
            return height - inch

        # --- 3. PÁGINA 1: TÍTULO Y TABLA DE VARIABLES ---
        p_title = Paragraph("CONTRATO INDIVIDUAL DE TRABAJO POR OBRA O LABOR", style_title)
        p_title.wrapOn(c, width - 2 * inch, height)
        p_title.drawOn(c, inch, height - inch * 1.2)

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
            [Paragraph("<b>Duración de la Obra:</b>", cell_style_label), Paragraph(datos.get('final_time', ''), cell_style_value)],
            [Paragraph("<b>Fecha de Inicio:</b>", cell_style_label), Paragraph(datos.get('start_date', ''), cell_style_value)],
            [Paragraph("<b>Nombre del Proyecto o Centro de Costos:</b>", cell_style_label), Paragraph(datos.get('project_name', ''), cell_style_value)],
            [Paragraph("<b>Lugar de Ejecución:</b>", cell_style_label), Paragraph(datos.get('project_city', ''), cell_style_value)],
            [Paragraph("<b>Salario Mensual:</b>", cell_style_label), Paragraph(datos.get('salary', ''), cell_style_value)],
            [Paragraph("<b>Frecuencia de Pago:</b>", cell_style_label), Paragraph(datos.get('payment_frequency', ''), cell_style_value)],
        ]
        
        # AJUSTE DE ANCHO DE COLUMNAS: La suma debe ser <= 6.5 pulgadas (ancho de página 8.5 - 2 de márgenes)
        table = Table(data_for_table, colWidths=[2.3 * inch, 4.2 * inch])
        
        # AJUSTE DE ESTILOS DE TABLA
        table.setStyle(TableStyle([
            # Estilos generales
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            
            # Estilos de borde
            ('GRID', (0,0), (-1,-1), 0.5, colors.darkgrey),   # Rejilla interna más visible
            ('BOX', (0,0), (-1,-1), 1.5, colors.black),      # Borde exterior grueso y negro
            
            # Estilo de fondo para la columna de etiquetas
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F0F0F0')),
        ]))
        
        table.wrapOn(c, width - 2 * inch, height)
        table_height = table._height
        table.drawOn(c, inch, height - inch * 1.5 - table_height)
        
        y_position = height - inch * 2 - table_height - 40


        intro_text = "Las partes identificadas plenamente en el presente contrato laboral deciden de mutuo acuerdo, libre y voluntariamente, pactar y cumplir las siguientes condiciones contractuales, de acuerdo a la normatividad laboral colombiana."

        p_intro = Paragraph(intro_text, style_body)
        p_intro.wrapOn(c, width - 2 * inch, height)
        p_intro.drawOn(c, inch, y_position)

        y_position = new_page()

    
        # --- 4. CLÁUSULAS DEL CONTRATO ---
        
        def draw_paragraph(text, style):
            nonlocal y_position
            p = Paragraph(text, style)
            p_width, p_height = p.wrapOn(c, width - 2 * inch, y_position)
            if p_height > y_position - inch: # Si no cabe, nueva página
                y_position = new_page()
            p.drawOn(c, inch, y_position - p_height)
            y_position -= (p_height + 10)

        # Texto de las cláusulas (adaptado del PDF)
        draw_paragraph(f"Entre el <b>EMPLEADOR</b> ({datos.get('employer_name','')}) y el <b>TRABAJADOR</b> ({datos.get('contractor_name','')}), de las condiciones mencionadas en el cuadro general al inicio del contrato, las partes identificados como aparecen al pie de sus firmas, se ha celebrado el presente contrato individual de trabajo por duración de la obra o labor contratada, regido además por las siguientes cláusulas:", style_body)
        
        clausulas = [
            ("PRIMERA: OBJETO.", "EI TRABAJADOR se compromete a colocar al servicio del empleador toda su capacidad normal de trabajo, en forma exclusiva y personal, en el desempeño de las funciones que se le asignen, y especialmente las relacionadas con el cargo y en las labores anexas y complementarias del mismo, de conformidad con las leyes, los reglamentos, las órdenes y las instrucciones generales o particulares que se le impartan, observando en su desempeño la buena fe, el cuidado y diligencia necesarios, durante el tiempo que para su especialidad de trabajo lo requiera la ejecución de la obra ya mencionada, y cuando este finalizada, automáticamente dará por terminado el presente contrato."),
            ("SEGUNDA: DURACIÓN DEL CONTRATO.", "El presente contrato se celebra por el tiempo que dure la realización de la obra o labor contratada, de acuerdo con las condiciones generales que se señalan al inicio del presente contrato."),
            ("TERCERA: PERÍODO DE PRUEBA.", "EI presente contrato queda sujeto a un período de prueba equivalente a la quinta parte de duración del presente contrato, sin que sea superior a dos (2) meses contados a partir de la fecha de la iniciación de la relación laboral, plazo durante el cual cualquiera de las partes podrá darlo por terminado unilateralmente sin previo aviso y sin lugar al pago de indemnización. Si vencido el período de prueba EL TRABAJADOR continuare prestando sus servicios con la aceptación expresa o tácita de EL EMPLEADOR, la duración del contrato será por el tiempo que dure la realización de la obra o labor contratada, mientras subsistan las causas que le dieron origen y la materia del trabajo."),
            ("CUARTA: LUGAR PRESTACIÒN DEL SERVICIO.", "El servicio antedicho lo prestará EL TRABAJADOR en el lugar determinado en el cuadro general del presente contrato, en todo caso, EL EMPLEADOR queda facultado para trasladar a EL TRABAJADOR a otras ciudades u oficios y asignarle otras funciones, siempre y cuando tales cambios y traslados no impliquen desmejora de las condiciones laborales de EL TRABAJADOR. Los gastos que se originen con el traslado serán cubiertos por EL EMPLEADOR de conformidad con el numeral 8 del Artículo 57 del C.S.T.  EL EMPLEADO se obliga a aceptar los cambios de oficio que decida EL EMPLEADOR dentro de su poder subordinante, siempre que se respeten las condiciones laborales del TRABAJADOR y no le causen perjuicios.  Todo ello sin que se afecte el honor, la dignidad y los derechos mínimos de EL TRABAJADOR, de conformidad con el Artículo 23 del C.S.T., modificado por el Artículo 1º de la Ley 50/90, y demás normas concordantes.."),
            ("QUINTA: JORNADA DE TRABAJO.", "EL TRABAJADOR laborará durante las horas diarias que como jornada ordinaria le señale EL EMPLEADOR de acuerdo con el Reglamento Interno de Trabajo, sin exceder las horas semanales establecidas en la Ley 2101 de 2021 que este aplicando el EMPLEADOR, en cualquiera de los turnos u horarios correspondientes a su oficio y además durante el tiempo extraordinario que LA EMPRESA le exija de acuerdo con la Ley. La labor en tiempo suplementario, siempre que le haya sido previamente autorizado por LA EMPRESA, le será cubierta a la tarifa legal definida por la ley colombiana."),
            ("PARÀGRAFO PRIMERO:", "El servicio antedicho lo prestará EL TRABAJADOR en el lugar determinado en el cuadro general del presente contrato, en todo caso, EL EMPLEADOR queda facultado para trasladar a EL TRABAJADOR a otras ciudades u oficios y asignarle otras funciones, siempre y cuando tales cambios y traslados no impliquen desmejora de las condiciones laborales de EL TRABAJADOR. Los gastos que se originen con el traslado serán cubiertos por EL EMPLEADOR de conformidad con el numeral 8 del Artículo 57 del C.S.T.  EL EMPLEADO se obliga a aceptar los cambios de oficio que decida EL EMPLEADOR dentro de su poder subordinante, siempre que se respeten las condiciones laborales del TRABAJADOR y no le causen perjuicios.  Todo ello sin que se afecte el honor, la dignidad y los derechos mínimos de EL TRABAJADOR, de conformidad con el Artículo 23 del C.S.T., modificado por el Artículo 1º de la Ley 50/90, y demás normas concordantes."),
            ("PARÀGRAFO SEGUNDO:", "EL TRABAJADOR prestará sus servicios durante todos los días laborables de cada semana y descansará el domingo; pero si por razón de su oficio debe trabajar habitualmente en domingos, tomará un día de descanso compensatorio por cada semana completa de labor, en uno cualquiera de los días laborables de la semana siguiente."),
            ("SEXTA: SALARIO.", "El salario determinado en el cuadro general al inicio del presente contrato fue acordado voluntaria y conscientemente por las partes, y cumple con todas las condiciones laborales, incluyendo todas las prestaciones sociales que por ley se estipulen. ."),
            ("PARÀGRAFO PRIMERO:", "SEGURIDAD SOCIAL. - EL EMPLEADOR pagará la parte que le corresponda de las cotizaciones al sistema de seguridad social en pensiones, salud y riesgos profesionales, igualmente podrá descontar a EL EMPLEADO la parte de las cotizaciones que por ley a él le corresponde sufragar.."),
            ("PARÀGRAFO SEGUNDO:", "VIATICOS. - EL EMPLEADOR reconocerá al empleado los viáticos accidentales y los gastos de representación, que se puedan generar y sea previamente acordado por las partes mediante documento escrito que deberá estar adicionado al presente contrato."),
            ("SEPTIMA: OBLIGACIONES DE EL TRABAJADOR.", "El trabajador se obliga a: 1. A no atender durante las horas de trabajo ocupaciones o asuntos diferentes a los que le encomiende EL EMPLEADOR. 2. Abstenerse de cualquier actitud en los compromisos comerciales, personales o en las relaciones sociales, que pueda afectar en forma nociva la reputación del empleador. 3. No solicitar préstamos especiales o ayuda económica a los clientes del empleador aprovechándose de su cargo u oficio o aceptarles donaciones de cualquier clase sin la previa autorización escrita del empleador. 4. No retirar de las instalaciones donde funcione la empresa elementos, máquinas y útiles de propiedad del empleador sin su autorización escrita. 5. No presentar cuentas de gastos ficticias o reportar como cumplidas visitas o tareas no efectuadas. 6. No autorizar o ejecutar sin ser de su competencia, operaciones que afecten los intereses del empleador o negociar bienes y/o mercancías del empleador en provecho propio. 7. No retener dinero o hacer efectivos cheques recibidos para el empleador. 8. Utilizar adecuadamente los implementos de seguridad que EL EMPLEADOR tenga establecidos como tal. 9. A trabajar todo el tiempo que sea necesario para cumplir cabalmente sus deberes. 10. A prestar sus servicios en cualquier otro empleo, cargo u oficio a donde lo promueva EL EMPLEADOR, ya sea en la sede inicial del trabajo o en cualquier otra, donde desarrolle su objeto social; dentro de su poder subordinante, siempre que se respeten las condiciones laborales EL EMPLEADO y no se le causen perjuicios. 11. A guardar confidencialidad sobre todo a la vinculación laboral y sobre la información a la cual tenga acceso por el desempeño de sus funciones. 12. A no ofrecer sus servicios o experiencia profesional a título personal, en competencia con los servicios o productos que presta o fabrique EL EMPLEADOR. 13. A no prestar directa e indirectamente sus servicios laborales a otros empleadores, sin autorización. 14. A no utilizar los recursos humanos, físicos, financieros e información en general de EL EMPLEADOR para beneficio propio o de terceros. 15. Aplicar las políticas, los reglamentos, las normas y procedimientos de EL EMPLEADOR. 16. Asistir a las capacitaciones a las que sea enviado por EL EMPLEADOR. 17. Sólo instalar software que cuenten con la debida licencia de uso en los computadores de la empresa. 18. No dar a conocer a personas no autorizadas la clave personal de acceso a los sistemas de cómputo de EL EMPLEADOR. 19. Cumplir con el RIT, Manuales, directrices, politicas y demas documentos de conducta y desarrollo de funciones emitidos por el empleador, y que el TRABAJADOR reconoce ser conocidos. 20. A cumplir las ordenes impartidas por su jefe y el personal de seguridad y salud en el trabajo. La violación de cualquiera de estas obligaciones será considerada como grave para efectos de la terminación unilateral del presente contrato de trabajo con justa causa."), 
            ("PARÀGRAFO PRIMERO:", ". La violación de cualquiera de las anteriores obligaciones y prohibiciones será considerada como grave para efectos de la terminación unilateral del presente contrato de trabajo con justa causa."),
            ("OCTAVA: DERECHOS Y DEBERES.", "Al TRABAJADOR se le aplicara los derechos y deberes establecidos en el Código Sustantivo del Trabajo Colombiano, el RIT y Directrices del empleador."),
            ("NOVENA: PAGOS NO SALARIALES.", "Los dineros que el TRABAJADOR reciba ocasionalmente o en forma habitual, o por mera liberalidad, por concepto de primas, alimentación, viáticos, bonificación por las tareas, participación de utilidades no constituirán salario, ni se computarán como factor salarial de acuerdo a los artículos 15 y 16 de la Ley 50/90, ya que se entiende que dichos pagos son un medio para facilitar la prestación del servicio y para desempeñar a cabalidad las funciones."),
            ("DÉCIMA: AUTORIZACIÓN DE DESCUENTOS.", "EL TRABAJADOR autoriza expresamente a EL EMPLEADOR para que, durante el desarrollo del contrato, o al finalizar el mismo, deduzca y compense de las sumas que le correspondan por concepto de salarios, prestaciones e indemnizaciones de carácter laboral, las cantidades y saldos pendientes a su cargo y a favor de ella, por razón de préstamos personales o de vivienda, valor de facturas por suministro de medicina, alimentos, víveres o mercancías que haya recibido a crédito, o por cualquiera otra causa que represente una deuda generada por el TRABAJADOR a favor del EMPLEADOR."),
            ("DÉCIMA PRIMERA: REGLAMENTOS.", "Hace parte de este contrato el reglamento interno del trabajo, manual de funciones y procesos establecidos para el cargo, indicaciones del personal de SST, directrices del empleador y demas documentos similares."),
            ("DÉCIMA SEGUNDA: DOMICILIO Y NOTIFICACIONES.", "EI TRABAJADOR declara expresamente que fue notificado y acepta que la dirección y número telefónico suministrados por él mismo en el presente contrato de trabajo es su domicilio y residencia principal, y que a mencionadas direcciones, correos electronicos o numero telefonico, se le puede enviar cualquier correspondencia o notificaciòn que fuere necesaria. En caso de traslado  o mudanza de dirección por parte del trabajador, este informará por escrito dentro de los cinco (5) primeros días hábiles a la fecha en que se produzca su traslado."),
            ("DÉCIMA TERCERA: TRATAMIENTO DE DATOS.", "En virtud de lo dispuesto en la Ley 1581 de 2012 y demás normas concordantes, el trabajador autoriza de manera libre, expresa y voluntaria al empleador para que realice el tratamiento de sus datos personales, los cuales serán utilizados exclusivamente para fines relacionados con la gestión laboral de la compañía."),
            ("DÉCIMA CUARTA: INTEGRALIDAD DEL CONTRATO.", "EI presente contrato reemplaza en su integridad y deja sin efecto cualquiera otro contrato verbal o escrito celebrado entre las partes con anterioridad."),
            ("DÉCIMA QUINTA: MODIFICACIONES.", "Las modificaciones al presente contrato podrán elaborarse en una hoja anexa a este documento, la cual hará parte del mismo y donde deberán consignarse los nombres y firmas de las partes contratantes, su documento de identidad y fecha en que se efectué la modificación."),
            ("DÉCIMA SEXTA: CONFIDENCIALIDAD.", "EL TRABAJADOR, en virtud de la suscripción del presente contrato se compromete a llevar a cabo las tareas asignadas de acuerdo con los más altos estándares de confidencialidad y competencia ética. Así mismo, se compromete a no revelar directa o indirectamente a ninguna persona, ni durante la vigencia del contrato, ni después de su terminación, ninguna información que hubiese obtenido durante la ejecución de este y que no sea de dominio público, excepto con el permiso explícito y por escrito del EMPLEADOR. EL TRABAJADOR no deberá publicar, ni permitir que se publique, ni divulgue información relacionada con compradores, clientes, proveedores o contratistas. Como las labores propias del cargo exigen el manejo de información y materiales CONFIDENCIALES de EL EMPLEADOR, EL TRABAJADOR se compromete en mantener en ABSOLUTA RESERVA todo dato de EL EMPLEADOR y sus clientes.  EL TRABAJADOR en el caso de hacer dejación de su cargo se obliga a entregar la información confidencial y técnica conocida por este en el ejercicio de sus funciones y que no ha guardado copia alguna en archivos o medios magnéticos o electrónicos.  Igualmente se obliga a mantener en reserva la información confidencial de EL EMPLEADOR y de sus clientes en el ejercicio de sus actividades, ya que declaran reconocer las disposiciones legales pertinentes acerca de las eventuales responsabilidades a su cargo por dar a conocer o utilizar en cualquier forma dichas informaciones. La violación de estas obligaciones se considera como grave a la luz del procedimiento disciplinario sin perjuicio de las acciones legales a que haya lugar. Lo anterior, de conformidad con la ley 1581 del 2012 y demás normas concordantes."),
            ("DÉCIMA SEPTIMA: INTERPRETACIÒN", "Este contrato ha sido redactado estrictamente de acuerdo con la Ley y la Jurisprudencia y será interpretado de buena fe y en consonancia con el C.S.T. El presente contrato ha sido discutido libremente por las partes, las cuales aprueban todas las estipulaciones que lo conforman y en consecuencia para constancia se firma en dos o más ejemplares del mismo tenor y valor, ante testigos, un ejemplar de los cuales recibe EL TRABAJADOR en este acto."),
            ("PARÁGRAFO PRIMERO: CONTROVERSIAS.", "En caso de presentarse alguna controversia entre las partes, esta será sometida a la justicia ordinaria de Colombia.."),
            ("DÉCIMA OCTAVA: FIRMA.", "El presente contrato ha sido discutido libremente por las partes, las cuales aprueban todas las estipulaciones que lo conforman y en consecuencia para constancia se firma en dos o más ejemplares del mismo tenor y valor. Firman las partes:")
        ]

        for titulo, texto in clausulas:
            draw_paragraph(f"<b>{titulo}</b> {texto}", style_body)

        # --- 5. FIRMAS ---
        if y_position < 3 * inch:
            y_position = new_page()
        
        y_position -= 1.5 * inch # Espacio para las firmas
        c.setFont("Helvetica", 10)
        c.drawString(1.5 * inch, y_position, "___________________________________")
        c.drawString(1.5 * inch, y_position - 15, "FIRMA DEL EMPLEADOR")
        c.drawString(1.5 * inch, y_position - 30, datos.get('employer_name', ''))

        c.drawString(5 * inch, y_position, "___________________________________")
        c.drawString(5 * inch, y_position - 15, "FIRMA Y CÉDULA DEL TRABAJADOR")
        c.drawString(5 * inch, y_position - 30, datos.get('contractor_name', ''))
        c.drawString(5 * inch, y_position - 45, f"C.C. {datos.get('contractor_id', '')}")

        # --- 6. ANEXOS Y DECLARACIÓN JURAMENTADA ---
        y_position = new_page()
        draw_paragraph("<b>ANEXO 1 AL CONTRATO DE TRABAJO</b>", style_bold)
        draw_paragraph("<b>ASUNTO: REQUISITOS PARA SU VINCULACIÓN AL SISTEMA DE SEGURIDAD SOCIAL</b>", style_bold)
        anexo_text = "1. Tres (3) fotocopias ampliadas legibles de la cedula de ciudadanía. 2. Certificado de afiliación EPS a la que pertenece. 3. Certificado de Fondo de pensión al que pertenece. 4. Tres (3) fotocopias de la cedula del cónyuge o compañero (a) permanente. 5. Dos (2) certificados de matrimonio registrado ante notaria o declaración extra juicio. 6. Dos (2) registros civiles de cada uno de los hijos. 7. Un (1) certificado de estudio original para cada uno de los hijos mayores de 12 años. 8. Cuando los hijos son mayores de 18 años es necesario: 2 certificados de estudio originales, 2 registros civiles, dos (2) fotocopias de la cédula (solo para EPS). 9. Para afiliar padres mayores de 60 años: registro civil de nacimiento del Trabajador, fotocopias de cedula de los padres, certificado de supervivencia y certificado de dependencia económica ante notaria. 10. Si es soltero puede afiliar a los padres a la EPS y Caja de compensación es necesario: Registro civil de nacimiento del trabajador, fotocopias de la cedula de los padres y certificado extra juicio de dependencia económica y supervivencia ante notaria. Certifico que fui notificado de estos requisitos, por lo tanto, es mi responsabilidad presentar dicha documentación y en caso de no hacerlo, mi empleador queda exonerado de cualquier reclamación."
        draw_paragraph(anexo_text, style_body)
        
        draw_paragraph("<b>DECLARACIÓN JURAMENTADA DEL TRABAJADOR:</b>", style_bold)
        declaracion_text = "El trabajador declara expresamente que asistió a la charla de inducción y Salud Ocupacional donde se le explican: el reglamento interno de trabajo, el reglamento de higiene y seguridad industrial, matriz de riesgos laborales de la empresa, las normas, procedimientos y cuidados inherentes a su cargo. De igual manera declara que recibió por parte de la empresa los elementos de protección personal requeridos para desarrollar su cargo y que recibió la capacitación respectiva acerca de su uso. Declara que está obligado a utilizarlos y que cualquier accidente de trabajo que ocurra por no utilizarlos correrá por su cuenta y a riesgo propio, en tanto la empresa quedará exonerada y no tendrá ninguna responsabilidad."
        draw_paragraph(declaracion_text, style_body)

        y_position -= 1.5 * inch
        c.drawString(3 * inch, y_position, "___________________________________")
        c.drawString(3 * inch, y_position - 15, "FIRMA Y CÉDULA DEL TRABAJADOR")

        # --- 7. GUARDAR EL PDF ---
        c.setFont("Helvetica", 9)
        c.drawString(inch, 0.75 * inch, f"Página {page_number}")

          # Añadir la frase de copyright en la esquina inferior derecha de la última página
        copyright_text = "© 2015 HEBITECH. All rights reserved."
        c.setFont("Helvetica", 8) # Arial 8 solicitado, usando Helvetica como alternativa estándar
        c.drawRightString(width - inch, 0.5 * inch, copyright_text) # 0.5 inch desde el borde inferior
        

        c.save()
        print(f"✅ PDF de Contrato de Obra o Labor generado exitosamente en: {filepath}")

    except Exception as e:
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"Error al generar el PDF de Obra o Labor: {e}")
        import traceback
        print(traceback.format_exc())
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

# Ejemplo de uso:
if __name__ == '__main__':
    datos_ejemplo = {
        'contract_number': '004p',
        'contract_date': '08/07/2025',
        'employer_name': 'INGEURBANISMO SAS',
        'employer_nit': '900.474.198-8',
        'legal_representative': 'ELIANA MARIA ARBELAEZ ALZATE',
        'legal_representative_id': '1.038.407.657',
        'employer_address': 'Km 4, Vía Llanogrande - Don Diego, Rionegro',
        'contractor_name': 'Prueba Pérez',
        'contractor_id': '1.123.000.000',
        'city_birth': 'Medellín',
        'date_birth': '1990-05-20',
        'contractor_address': 'Calle 10 # 43A-30, Medellín',
        'contractor_phone': '3101234567',
        'contractor_email': 'prueba.perez@trabajador.com',
        'name_number_emergency': 'Maria Lopez - 3159876543',
        'workers_position': 'Ayudante de Obra',
        'activity': 'Actividades de construcción de la Torre 3.',
        'final_time': 'Hasta llegar el 30% de la obra mencionada de acuerdo al acta de avance de obra',
        'project_name': 'Proyecto EBANO',
        'project_city': 'Rionegro, Antioquia',
        'salary': 'DOS MILLONES QUINIENTOS MIL PESOS M/CTE ($2.500.000)',
        'payment_frequency': 'Quincenal',
        'start_date': '2025-08-01',
    }
    generar_pdf_obra_labor(datos_ejemplo)