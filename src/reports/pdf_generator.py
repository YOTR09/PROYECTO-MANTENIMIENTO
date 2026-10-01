import os
import html
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from typing import List, Dict, Any

def _safe_str(val: Any) -> str:
    """Escapa caracteres especiales XML/HTML para inserción segura en Paragraphs."""
    if val is None:
        return ""
    return html.escape(str(val))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo_empresa_light.png")

def _crear_encabezado_pdf(elementos, titulo_reporte: str, subtitulo: str = ""):
    styles = getSampleStyleSheet()
    
    header_data = []
    logo_img = None
    if os.path.exists(LOGO_PATH):
        try:
            logo_img = Image(LOGO_PATH, width=160, height=40)
        except Exception:
            logo_img = None

    style_title = ParagraphStyle(
        "HeaderTitle",
        parent=styles["Heading1"],
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#1E3A8A"),
        fontName="Helvetica-Bold"
    )

    style_sub = ParagraphStyle(
        "HeaderSub",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#4B5563")
    )

    style_meta = ParagraphStyle(
        "HeaderMeta",
        parent=styles["Normal"],
        fontSize=8,
        leading=11,
        alignment=2, # Right
        textColor=colors.HexColor("#6B7280")
    )

    ahora_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    texto_centro = f"<b>{_safe_str(titulo_reporte)}</b><br/><font size=8>{_safe_str(subtitulo)}</font>"
    texto_derecha = f"<b>Empresa:</b> Brisas del Palmar<br/><b>Emisión:</b> {ahora_str}<br/><b>Sistema:</b> Control de Flota"

    col1 = logo_img if logo_img else Paragraph("<b>BRISAS DEL PALMAR</b>", style_title)
    col2 = Paragraph(texto_centro, style_title)
    col3 = Paragraph(texto_derecha, style_meta)

    header_table = Table([[col1, col2, col3]], colWidths=[170, 360, 220])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-1), 1.5, colors.HexColor("#1E3A8A")),
    ]))
    elementos.append(header_table)
    elementos.append(Spacer(1, 15))

class PDFReportGenerator:

    # ---------------- REPORTE 1: FICHA TÉCNICA DE FLOTA ----------------
    @staticmethod
    def generar_reporte_flota(vehiculos: List[Dict[str, Any]], ruta_destino: str):
        doc = SimpleDocTemplate(
            ruta_destino,
            pagesize=landscape(letter),
            leftMargin=30,
            rightMargin=30,
            topMargin=30,
            bottomMargin=30
        )
        elementos = []
        _crear_encabezado_pdf(
            elementos,
            "FICHA TÉCNICA Y ESTADO DE FLOTA VEHICULAR",
            "Relación oficial de unidades de transporte público activas y asignadas"
        )

        headers = ["Unidad", "Placa", "Marca y Modelo", "Año", "Odómetro Actual", "Socio Propietario", "Cédula", "Estado"]
        data = [headers]

        for v in vehiculos:
            data.append([
                v.get("numero_unidad", ""),
                v.get("placa", ""),
                v.get("marca_modelo", ""),
                str(v.get("ano") or "-"),
                f"{v.get('kilometraje_actual', 0):,} km",
                v.get("socio_nombre", ""),
                v.get("socio_cedula", ""),
                v.get("status", "Activo")
            ])

        col_widths = [65, 75, 175, 45, 105, 160, 80, 75]
        tabla = Table(data, colWidths=col_widths, repeatRows=1)
        
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8.5),
            ('ALIGN', (0, 1), (1, -1), 'CENTER'),
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),
            ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
            ('ALIGN', (6, 1), (7, -1), 'CENTER'),
        ])

        for i in range(1, len(data)):
            bg = colors.HexColor("#F8FAFC") if i % 2 == 0 else colors.white
            style.add('BACKGROUND', (0, i), (-1, i), bg)
            estado_val = data[i][7]
            if estado_val == "En Taller":
                style.add('TEXTCOLOR', (7, i), (7, i), colors.HexColor("#D97706"))
            elif estado_val == "Inactivo":
                style.add('TEXTCOLOR', (7, i), (7, i), colors.HexColor("#DC2626"))
            else:
                style.add('TEXTCOLOR', (7, i), (7, i), colors.HexColor("#16A34A"))

        tabla.setStyle(style)
        elementos.append(tabla)

        # Resumen al pie
        elementos.append(Spacer(1, 15))
        styles = getSampleStyleSheet()
        resumen_txt = f"<b>Total de unidades registradas:</b> {len(vehiculos)} | <b>Activas:</b> {sum(1 for v in vehiculos if v.get('status') == 'Activo')} | <b>En Taller:</b> {sum(1 for v in vehiculos if v.get('status') == 'En Taller')}"
        elementos.append(Paragraph(resumen_txt, styles["Normal"]))

        doc.build(elementos)

    # ---------------- REPORTE 2: PLAN PREVENTIVO Y ALERTAS ----------------
    @staticmethod
    def generar_reporte_preventivo(programaciones: List[Dict[str, Any]], ruta_destino: str):
        doc = SimpleDocTemplate(
            ruta_destino,
            pagesize=landscape(letter),
            leftMargin=30,
            rightMargin=30,
            topMargin=30,
            bottomMargin=30
        )
        elementos = []
        _crear_encabezado_pdf(
            elementos,
            "PLAN DE MANTENIMIENTO PREVENTIVO Y SEMAFORIZACIÓN",
            "Control y proyección de vencimientos por kilometraje y fecha límite"
        )

        headers = ["Unidad", "Placa", "Rutina de Mantenimiento", "Odómetro Actual", "Próx. Servicio Km", "Próx. Fecha", "Diagnóstico / Alerta", "Semáforo"]
        data = [headers]

        for p in programaciones:
            km_prox = f"{p.get('km_proximo_servicio', 0):,} km" if p.get('km_proximo_servicio') else "N/A"
            fecha_prox = p.get('fecha_proximo_servicio') or "N/A"
            estado_badge = p.get('estado', 'Al Día')
            resumen_alerta = p.get('resumen_alerta', '')

            data.append([
                p.get("numero_unidad", ""),
                p.get("placa", ""),
                p.get("tipo_nombre", ""),
                f"{p.get('kilometraje_actual', 0):,} km",
                km_prox,
                fecha_prox,
                resumen_alerta,
                estado_badge
            ])

        col_widths = [60, 70, 185, 95, 95, 80, 120, 75]
        tabla = Table(data, colWidths=col_widths, repeatRows=1)

        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 1), (1, -1), 'CENTER'),
            ('ALIGN', (3, 1), (4, -1), 'RIGHT'),
            ('ALIGN', (5, 1), (5, -1), 'CENTER'),
            ('ALIGN', (7, 1), (7, -1), 'CENTER'),
        ])

        for i in range(1, len(data)):
            estado_val = data[i][7]
            if estado_val == "Vencido":
                style.add('BACKGROUND', (0, i), (-1, i), colors.HexColor("#FEE2E2"))
                style.add('TEXTCOLOR', (7, i), (7, i), colors.HexColor("#991B1B"))
                style.add('FONTNAME', (7, i), (7, i), 'Helvetica-Bold')
            elif estado_val == "Por Vencer":
                style.add('BACKGROUND', (0, i), (-1, i), colors.HexColor("#FEF3C7"))
                style.add('TEXTCOLOR', (7, i), (7, i), colors.HexColor("#92400E"))
                style.add('FONTNAME', (7, i), (7, i), 'Helvetica-Bold')
            else:
                bg = colors.HexColor("#F8FAFC") if i % 2 == 0 else colors.white
                style.add('BACKGROUND', (0, i), (-1, i), bg)
                style.add('TEXTCOLOR', (7, i), (7, i), colors.HexColor("#166534"))

        tabla.setStyle(style)
        elementos.append(tabla)

        elementos.append(Spacer(1, 15))
        styles = getSampleStyleSheet()
        vencidos_c = sum(1 for p in programaciones if p.get("estado") == "Vencido")
        por_vencer_c = sum(1 for p in programaciones if p.get("estado") == "Por Vencer")
        al_dia_c = sum(1 for p in programaciones if p.get("estado") == "Al Día")
        resumen_txt = f"<b>Resumen de Alertas Preventivas:</b> 🔴 Vencidos: <b>{vencidos_c}</b> | 🟡 Por Vencer: <b>{por_vencer_c}</b> | 🟢 Al Día: <b>{al_dia_c}</b>"
        elementos.append(Paragraph(resumen_txt, styles["Normal"]))

        doc.build(elementos)

    # ---------------- REPORTE 4: DIRECTORIO DE SOCIOS ----------------
    @staticmethod
    def generar_reporte_socios(socios_con_unidades: List[Dict[str, Any]], ruta_destino: str):
        doc = SimpleDocTemplate(
            ruta_destino,
            pagesize=letter,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        elementos = []
        _crear_encabezado_pdf(
            elementos,
            "DIRECTORIO INSTITUCIONAL DE SOCIOS PROPIETARIOS",
            "Registro de afiliados y distribución de unidades operativas"
        )

        headers = ["Cédula / RIF", "Nombre Completo", "Teléfono", "Estado", "Unidades Asignadas"]
        data = [headers]

        for s in socios_con_unidades:
            unidades_str = s.get("unidades_resumen") or "Ninguna"
            data.append([
                s.get("cedula", ""),
                s.get("nombre_completo", ""),
                s.get("telefono") or "-",
                s.get("estado", "Activo"),
                unidades_str
            ])

        col_widths = [85, 170, 95, 60, 130]
        tabla = Table(data, colWidths=col_widths, repeatRows=1)

        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8.5),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (2, 1), (3, -1), 'CENTER'),
        ])

        for i in range(1, len(data)):
            bg = colors.HexColor("#F8FAFC") if i % 2 == 0 else colors.white
            style.add('BACKGROUND', (0, i), (-1, i), bg)

        tabla.setStyle(style)
        elementos.append(tabla)

        elementos.append(Spacer(1, 15))
        styles = getSampleStyleSheet()
        resumen_txt = f"<b>Total de Socios Registrados:</b> {len(socios_con_unidades)} | <b>Activos:</b> {sum(1 for s in socios_con_unidades if s.get('estado') == 'Activo')}"
        elementos.append(Paragraph(resumen_txt, styles["Normal"]))

        doc.build(elementos)
