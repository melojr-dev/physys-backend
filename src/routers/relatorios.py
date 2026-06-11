from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from src.database import get_db
from src import models
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
from datetime import datetime

router = APIRouter()

@router.get("/{sessao_id}/pdf")
def gerar_relatorio_pdf(sessao_id: int, db: Session = Depends(get_db)):
    sessao = db.query(models.Sessao).filter(models.Sessao.id == sessao_id).first()
    if not sessao:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

    paciente = db.query(models.Paciente).filter(models.Paciente.id == sessao.paciente_id).first()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle('titulo', parent=styles['Title'],
                                  fontSize=20, textColor=colors.HexColor('#1a73e8'),
                                  spaceAfter=6)
    subtitulo_style = ParagraphStyle('subtitulo', parent=styles['Heading2'],
                                     fontSize=13, textColor=colors.HexColor('#333333'),
                                     spaceBefore=12, spaceAfter=4)
    normal_style = ParagraphStyle('normal', parent=styles['Normal'],
                                  fontSize=11, leading=16)

    story = []

    # Cabeçalho
    story.append(Paragraph("PhySys — Relatório de Avaliação", titulo_style))
    story.append(Paragraph(f"Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}", normal_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1a73e8')))
    story.append(Spacer(1, 0.4*cm))

    # Dados do paciente
    story.append(Paragraph("Dados do Paciente", subtitulo_style))
    dados_paciente = [
        ["Nome", paciente.nome if paciente else "—"],
        ["Data de Nascimento", paciente.data_nascimento or "—"],
        ["Sexo", paciente.sexo or "—"],
        ["Diagnóstico", paciente.diagnostico or "—"],
    ]
    t = Table(dados_paciente, colWidths=[5*cm, 12*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0fe')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.4*cm))

    # Dados da sessão
    story.append(Paragraph("Dados da Sessão", subtitulo_style))
    data_sessao = sessao.criado_em.strftime('%d/%m/%Y às %H:%M') if sessao.criado_em else "—"
    dados_sessao = [
        ["Movimento", sessao.movimento or "—"],
        ["Lado", sessao.lado.capitalize() if sessao.lado else "—"],
        ["Data", data_sessao],
        ["Duração", f"{sessao.duracao:.1f}s" if sessao.duracao else "—"],
        ["FPS", f"{sessao.fps:.1f}" if sessao.fps else "—"],
        ["Hardware", sessao.hardware or "—"],
    ]
    t2 = Table(dados_sessao, colWidths=[5*cm, 12*cm])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0fe')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t2)
    story.append(Spacer(1, 0.4*cm))

    # Resultados ADM
    story.append(Paragraph("Resultados — ADM (Amplitude de Movimento)", subtitulo_style))
    dados_adm = [
        ["Métrica", "Valor"],
        ["ADM Máxima", f"{sessao.adm_max:.1f}°" if sessao.adm_max else "—"],
        ["ADM Média", f"{sessao.adm_media:.1f}°" if sessao.adm_media else "—"],
        ["ADM Mínima", f"{sessao.adm_min:.1f}°" if sessao.adm_min else "—"],
        ["Desvio Padrão", f"{sessao.adm_desvio:.1f}°" if sessao.adm_desvio else "—"],
        ["Velocidade Pico", f"{sessao.velocidade_pico:.1f}°/s" if sessao.velocidade_pico else "—"],
        ["Velocidade Média", f"{sessao.velocidade_media:.1f}°/s" if sessao.velocidade_media else "—"],
        ["Total de Repetições", str(sessao.total_reps) if sessao.total_reps is not None else "—"],
        ["Outliers Corrigidos", str(sessao.outliers_corrigidos) if sessao.outliers_corrigidos is not None else "—"],
        ["Qualidade", sessao.label_qualidade or "—"],
    ]
    t3 = Table(dados_adm, colWidths=[8*cm, 9*cm])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t3)

    # Observações
    if sessao.notas:
        story.append(Spacer(1, 0.4*cm))
        story.append(Paragraph("Observações", subtitulo_style))
        story.append(Paragraph(sessao.notas, normal_style))

    doc.build(story)
    buffer.seek(0)

    nome_arquivo = f"relatorio_sessao_{sessao_id}.pdf"
    return StreamingResponse(buffer, media_type="application/pdf",
                             headers={"Content-Disposition": f"attachment; filename={nome_arquivo}"})
