from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os

def generar_pdf_receta(receta):
    # Crear directorio si no existe
    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'recetas')
    os.makedirs(pdf_dir, exist_ok=True)
    
    # Ruta del archivo PDF
    pdf_filename = f'receta_{receta.id}.pdf'
    pdf_path = os.path.join(pdf_dir, pdf_filename)
    
    # Crear el documento PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        alignment=1,
        spaceAfter=30
    )
    elements.append(Paragraph('Receta Médica', title_style))
    elements.append(Paragraph(f'Fecha: {receta.fecha_creacion.strftime("%d/%m/%Y")}', styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Información del paciente
    elements.append(Paragraph('Información del Paciente:', styles['Heading2']))
    elements.append(Paragraph(f'Nombre: {receta.cliente.nombre} {receta.cliente.apellido}', styles['Normal']))
    elements.append(Paragraph(f'Edad: {receta.cliente.edad} años', styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Medicamentos
    elements.append(Paragraph('Medicamentos Recetados:', styles['Heading2']))
    
    # Lista de medicamentos en línea
    for med in receta.medicamentoreceta_set.all():
        med_text = f"{med.cantidad} {med.medicamento.nombre} cada {med.frecuencia}"
        if med.instrucciones:
            med_text += f" - {med.instrucciones}"
        elements.append(Paragraph(f"• {med_text}", styles['Normal']))
        elements.append(Spacer(1, 10))
    
    # Notas
    if receta.notas:
        elements.append(Spacer(1, 20))
        elements.append(Paragraph('Notas Adicionales:', styles['Heading2']))
        elements.append(Paragraph(receta.notas, styles['Normal']))
    
    # Firma del doctor
    elements.append(Spacer(1, 40))
    elements.append(Paragraph(f'Dr. {receta.doctor.get_full_name()}', styles['Normal']))
    elements.append(Paragraph(receta.doctor.email, styles['Normal']))
    
    # Generar PDF
    doc.build(elements)
    return pdf_path

def enviar_receta_email(receta, pdf_path):
    asunto = f'Receta Médica - {receta.cliente}'
    mensaje = f"""
    Estimado/a {receta.cliente.nombre},

    Adjunto encontrará su receta médica del {receta.fecha_creacion.strftime('%d/%m/%Y')}.

    Saludos cordiales,
    {receta.doctor.get_full_name()}
    """
    
    send_mail(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        [receta.cliente.email],
        fail_silently=False,
        attachments=[(os.path.basename(pdf_path), open(pdf_path, 'rb').read(), 'application/pdf')]
    )