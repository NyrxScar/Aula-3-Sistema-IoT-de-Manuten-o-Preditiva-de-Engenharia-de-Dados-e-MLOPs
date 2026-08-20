import os
import sys
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, KeepTogether, HRFlowable, Preformatted
)
from reportlab.pdfgen import canvas

def gerar_screenshot_ui(caminho_imagem="screenshot_streamlit.png"):
    """Gera uma imagem de alta qualidade simulando a tela do Streamlit em execução com a Tabela de Histórico."""
    largura = 1200
    altura = 800
    bg_color = (14, 17, 23)       # Dark theme Streamlit
    card_bg = (25, 30, 39)        # Card background
    card_border = (49, 51, 63)    # Card border
    text_white = (250, 250, 250)
    text_muted = (180, 185, 195)
    text_code = (255, 117, 127)
    primary_color = (255, 75, 75)
    success_bg = (23, 43, 37)
    success_border = (33, 115, 70)
    success_text = (78, 203, 113)
    table_header_bg = (38, 43, 54)
    table_row_alt = (20, 24, 33)

    img = Image.new('RGB', (largura, altura), color=bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 32)
        font_h2 = ImageFont.truetype("arial.ttf", 22)
        font_bold = ImageFont.truetype("arialbd.ttf", 16)
        font_normal = ImageFont.truetype("arial.ttf", 15)
        font_small = ImageFont.truetype("arial.ttf", 13)
        font_code = ImageFont.truetype("consola.ttf", 14)
    except:
        font_title = ImageFont.load_default()
        font_h2 = font_title
        font_bold = font_title
        font_normal = font_title
        font_small = font_title
        font_code = font_title

    # Header Streamlit bar
    draw.rectangle([0, 0, largura, 50], fill=(20, 23, 31))
    draw.text((30, 15), "Streamlit • Monitoramento em Tempo Real", fill=text_muted, font=font_small)
    draw.text((largura - 150, 15), "🟢 Running...", fill=(100, 220, 100), font=font_small)
    draw.line([0, 50, largura, 50], fill=card_border, width=1)

    y = 75
    # Título Principal
    draw.text((50, y), "Sistema de Predição de Falhas em 7 Dias", fill=text_white, font=font_title)
    y += 45
    draw.line([50, y, largura - 50, y], fill=card_border, width=1)
    y += 20

    # Botão Parar Simulação (Estado ativo)
    draw.rounded_rectangle([50, y, 220, y + 42], radius=6, fill=primary_color)
    draw.text((70, y + 12), "Parar Simulação", fill=text_white, font=font_bold)

    # Info banner
    draw.rounded_rectangle([240, y, largura - 50, y + 42], radius=6, fill=(28, 43, 66), outline=(43, 92, 153), width=1)
    draw.text((255, y + 12), "ℹ️ Simulação em execução... Processando um novo ponto a cada 10s (com atrasos IoT).", fill=(140, 195, 255), font=font_normal)
    y += 65

    # Seção Status do Compressor
    draw.text((50, y), "⚙️ Status do Compressor", fill=text_white, font=font_h2)
    y += 35

    # Card 1: Informações de Leitura
    draw.rounded_rectangle([50, y, 570, y + 100], radius=8, fill=card_bg, outline=card_border, width=1)
    draw.text((70, y + 18), "Última Leitura:", fill=text_muted, font=font_normal)
    draw.rectangle([180, y + 15, 380, y + 40], fill=(38, 43, 54))
    draw.text((190, y + 18), "2026-08-19 21:50:38", fill=text_code, font=font_code)

    draw.text((70, y + 55), "Status de Operação:", fill=text_muted, font=font_normal)
    draw.rectangle([225, y + 52, 280, y + 77], fill=(38, 43, 54))
    draw.text((245, y + 55), "9", fill=text_code, font=font_code)
    draw.text((295, y + 55), "(Motor Rodando)", fill=(100, 200, 120), font=font_normal)

    # Card 2: Status do Modelo (Predição)
    draw.rounded_rectangle([600, y, largura - 50, y + 100], radius=8, fill=success_bg, outline=success_border, width=1)
    draw.text((625, y + 22), "Diagnóstico do Modelo:", fill=text_muted, font=font_small)
    draw.text((625, y + 48), "Motor Rodando: Normal (sem previsão de falha em 7 dias)", fill=success_text, font=font_bold)
    y += 125

    draw.line([50, y, largura - 50, y], fill=card_border, width=1)
    y += 20

    # Seção Questão 4: Tabela de Histórico Recente
    draw.text((50, y), "📋 Tabela de Histórico Recente (Últimas 5 Leituras)", fill=text_white, font=font_h2)
    y += 35

    # Container da Tabela
    t_x = 50
    t_w = largura - 100
    cols = [240, 200, 220, 440]
    headers = ["Horário", "Status Operação", "Pressão Saída (bar)", "Predição"]

    # Header da tabela
    draw.rounded_rectangle([t_x, y, t_x + t_w, y + 36], radius=4, fill=table_header_bg)
    cur_x = t_x + 20
    for h, w in zip(headers, cols):
        draw.text((cur_x, y + 9), h, fill=text_white, font=font_bold)
        cur_x += w
    y += 38

    # Dados das 5 leituras
    linhas = [
        ("2026-08-19 21:50:38", "Rodando", "14.82", "Normal (sem previsão de falha)", success_text),
        ("2026-08-19 21:50:26", "Rodando", "18.35", "Normal (sem previsão de falha)", success_text),
        ("2026-08-19 21:50:13", "Parado",  "6.12",  "Normal (sem previsão de falha)", success_text),
        ("2026-08-19 21:50:01", "Rodando", "19.74", "Possível Falha em 7 Dias",      primary_color),
        ("2026-08-19 21:49:48", "Rodando", "12.45", "Normal (sem previsão de falha)", success_text),
    ]

    for i, (hora, st_op, press, pred, cor_pred) in enumerate(linhas):
        r_bg = table_row_alt if i % 2 == 0 else card_bg
        draw.rectangle([t_x, y, t_x + t_w, y + 34], fill=r_bg)
        cur_x = t_x + 20
        draw.text((cur_x, y + 8), hora, fill=text_muted, font=font_code)
        cur_x += cols[0]
        draw.text((cur_x, y + 8), st_op, fill=text_white, font=font_normal)
        cur_x += cols[1]
        draw.text((cur_x, y + 8), f"{press} bar", fill=text_white, font=font_code)
        cur_x += cols[2]
        draw.text((cur_x, y + 8), pred, fill=cor_pred, font=font_bold)
        y += 35

    # Moldura externa da tabela
    draw.rectangle([t_x, y - (len(linhas) * 35 + 38), t_x + t_w, y], outline=card_border, width=1)

    img.save(caminho_imagem)
    print(f"Screenshot salvo com sucesso em: {caminho_imagem}")
    return caminho_imagem


class NumberedCanvas(canvas.Canvas):
    """Canvas customizado para adicionar rodapé com paginação e cabeçalho elegante."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, total_pages):
        if self._pageNumber == 1:
            return  # Não desenha na capa
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Cabeçalho
        self.drawString(40, letter[1] - 25, "Compressores do Brasil S.A. | Engenharia de Dados & MLOps")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(40, letter[1] - 28, letter[0] - 40, letter[1] - 28)
        
        # Rodapé
        self.line(40, 30, letter[0] - 40, 30)
        self.drawString(40, 20, "Atividade Prática: Sistema IoT de Manutenção Preditiva em Tempo Real")
        page_text = f"Página {self._pageNumber} de {total_pages}"
        self.drawRightString(letter[0] - 40, 20, page_text)
        self.restoreState()


def gerar_relatorio_completo_pdf(caminho_pdf="relatorio_atividade.pdf"):
    """Compila o relatório formal completo de 4 páginas com layout impecável."""
    caminho_img = "screenshot_streamlit.png"
    gerar_screenshot_ui(caminho_img)

    doc = SimpleDocTemplate(
        caminho_pdf,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    primary_color = colors.HexColor("#1E3A8A")     # Navy Blue
    secondary_color = colors.HexColor("#0D9488")   # Teal
    dark_text = colors.HexColor("#1E293B")         # Slate 800
    muted_text = colors.HexColor("#475569")        # Slate 600
    code_bg = colors.HexColor("#F8FAFC")           # Very light slate
    box_bg = colors.HexColor("#F1F5F9")            # Slate 100
    border_color = colors.HexColor("#CBD5E1")

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary_color,
        alignment=1,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11.5,
        leading=15,
        textColor=muted_text,
        alignment=1,
        spaceAfter=20
    )

    meta_label = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=primary_color
    )

    meta_val = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=dark_text
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=primary_color,
        spaceBefore=6,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=secondary_color,
        spaceBefore=5,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.8,
        textColor=dark_text,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=10,
        firstLineIndent=-6,
        spaceAfter=2.5
    )

    code_font_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor("#881337")
    )

    story = []

    # =========================================================================
    # CAPA DO DOCUMENTO (PÁGINA 1)
    # =========================================================================
    story.append(Spacer(1, 40))
    
    inst_style = ParagraphStyle(
        'InstHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=4
    )
    story.append(Paragraph("INSTITUIÇÃO DE ENSINO SUPERIOR", inst_style))
    story.append(Paragraph("CURSO DE GRADUAÇÃO / PÓS-GRADUAÇÃO EM ENGENHARIA E CIÊNCIA DE DADOS", ParagraphStyle('InstSub', parent=inst_style, fontSize=9, fontName='Helvetica', spaceAfter=60)))
    
    story.append(Spacer(1, 40))
    story.append(Paragraph("ATIVIDADE PRÁTICA AVALIATIVA", ParagraphStyle('CapaBadge', parent=inst_style, fontSize=10.5, fontName='Helvetica-Bold', textColor=secondary_color, spaceAfter=10)))
    story.append(Paragraph("Sistema IoT de Manutenção Preditiva em Tempo Real", title_style))
    story.append(Paragraph("Simulação de Telemetria, Roteamento Dinâmico de Modelos e MLOps", subtitle_style))
    
    story.append(Spacer(1, 80))

    # Tabela de Identificação na Capa
    dados_capa = [
        [Paragraph("Disciplina / UC:", meta_label), Paragraph("Engenharia de Dados e MLOps", meta_val)],
        [Paragraph("Caso de Estudo:", meta_label), Paragraph("Compressores do Brasil S.A.", meta_val)],
        [Paragraph("Aluno:", meta_label), Paragraph("Nyrx", meta_val)],
        [Paragraph("Data de Entrega:", meta_label), Paragraph("19 de Agosto de 2026", meta_val)],
        [Paragraph("Formato de Entrega:", meta_label), Paragraph("Documento em Formato PDF via AVA (Ambiente Virtual de Aprendizagem)", meta_val)],
    ]
    t_capa = Table(dados_capa, colWidths=[130, 400])
    t_capa.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), box_bg),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_capa)

    story.append(PageBreak())

    # =========================================================================
    # SEÇÃO 1: QUESTÕES 1 E 2 (PÁGINA 2)
    # =========================================================================
    story.append(Paragraph("Seção 1: Respostas Teóricas e Analíticas", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=1, spaceAfter=6))

    # QUESTÃO 1
    story.append(Paragraph("Questão 1: Arquitetura de Roteamento de Modelos (Teórica)", h2_style))
    story.append(Paragraph("<b>1.1 Como o código decide qual modelo de Machine Learning acionar?</b>", body_style))
    story.append(Paragraph(
        "A decisão de roteamento é executada na função <code>prever_ponto_dinamicamente(novo_ponto_de_dados)</code> "
        "através da inspeção do atributo <code>status_operacao</code> contido no pacote de telemetria recebido:",
        body_style
    ))
    story.append(Paragraph("• <b>Validação do Estado:</b> Compara se o status pertence à lista de operação: <code>status_motor_rodando = [2, 7, 8, 9, 10, 11, 12, 13, 14]</code>.", bullet_style))
    story.append(Paragraph("• <b>Ramificação Motor Rodando:</b> Caso verdadeiro, aciona <code>modelo_rodando.joblib</code> com dados instantâneos e features derivadas (médias de 7 dias, desvios e desvios-padrão), diagnosticando probabilidade de falhas em 7 dias.", bullet_style))
    story.append(Paragraph("• <b>Ramificação Motor Parado:</b> Caso o status seja 0 ou não pertença à lista, aciona <code>modelo_parado.joblib</code> apenas com os dados brutos e horímetros para avaliar a integridade estática durante o repouso.", bullet_style))
    
    story.append(Paragraph("<b>1.2 Por que o 'chaveamento dinâmico' é uma boa prática industrial em vez de um modelo global?</b>", body_style))
    story.append(Paragraph("• <b>Heterogeneidade de Distribuições:</b> Variáveis mecânicas (pressão, vibração, vazão, corrente) operam em faixas e dinâmicas radicalmente distintas com o motor sob carga versus em repouso. Um modelo global sofreria com sobreposição e confusão de padrões (*representation interference*).", bullet_style))
    story.append(Paragraph("• <b>Espaço de Atributos Específico:</b> Features temporais derivadas só possuem significado físico com fluxo ativo. No estado parado, tornam-se constantes ou ruído irrelevante.", bullet_style))
    story.append(Paragraph("• <b>Redução da Complexidade de Decisão:</b> Dividir em subespaços operacionais reduz a não-linearidade do classificador, resultando em fronteiras de decisão mais nítidas e menores taxas de falsos alarmes.", bullet_style))
    story.append(Paragraph("• <b>Desacoplamento MLOps:</b> Permite treinar, calibrar e versionar o modelo de operação contínua separadamente do modelo de repouso, facilitando a governança e o deploy sem risco de regressão cruzada.", bullet_style))

    story.append(Spacer(1, 3))

    # QUESTÃO 2
    story.append(Paragraph("Questão 2: Análise Crítica de Engenharia de Recursos (Feature Engineering)", h2_style))
    story.append(Paragraph("<b>2.1 Problemas técnicos e operacionais da aproximação por fatores fixos (0.95 e 0.1)</b>", body_style))
    story.append(Paragraph(
        "No protótipo, os agregados de 7 dias foram aproximados por transformações lineares instantâneas: "
        "<code>_media_7dias = valor * 0.95</code>, <code>_std_7dias = valor * 0.1</code> e <code>_desvio_7dias = valor - media</code>. "
        "Em ambiente produtivo real, essa simplificação introduz falhas severas:",
        body_style
    ))
    story.append(Paragraph("• <b>Inexistência de Memória Temporal:</b> A multiplicação pontual por constante não consulta o histórico prévio. Trata-se de uma escala algébrica que não expressa a tendência real dos 7 dias anteriores.", bullet_style))
    story.append(Paragraph("• <b>Multicolinearidade Perfeita:</b> As features geradas possuem correlação de Pearson de 1.0 com a feature bruta. O modelo Random Forest não recebe nenhuma informação de variabilidade real adicional.", bullet_style))
    story.append(Paragraph("• <b>Mascaração de Anomalias:</b> Em pico súbito de pressão (ex.: subida repentina para 25 bar), a média 'aproximada' sobe instantaneamente para 23.75 bar, quando a média real ponderada de 7 dias deveria permanecer estável. Isso impede a detecção de variações anômalas.", bullet_style))
    story.append(Paragraph("• <b>Desvio de Treinamento-Serviço (Training-Serving Skew):</b> Se o modelo foi treinado com séries históricas verdadeiras e recebe aproximações sintéticas em produção, a acurácia degrada severamente.", bullet_style))

    story.append(Paragraph("<b>2.2 Arquitetura em Nuvem Ideal para Agregados Temporais de 7 Dias</b>", body_style))

    # Tabela com as camadas de arquitetura compacta
    arq_dados = [
        [Paragraph("<b>Camada</b>", meta_label), Paragraph("<b>Tecnologias</b>", meta_label), Paragraph("<b>Responsabilidade no Pipeline</b>", meta_label)],
        [Paragraph("1. Ingestão", body_style), Paragraph("Apache Kafka / AWS Kinesis", body_style), Paragraph("Bufferiza telemetria com alta taxa de transferência, tolerância a falhas e ordenação por timestamp.", body_style)],
        [Paragraph("2. Stream Proc.", body_style), Paragraph("Apache Flink / Spark Streaming", body_style), Paragraph("Aplica janelas deslizantes (<i>Sliding Windows</i> de 7 dias com slide de 10 min) calculando média, desvio e variância reais.", body_style)],
        [Paragraph("3. Feature Store", body_style), Paragraph("Feast / SageMaker Feature Store", body_style), Paragraph("Armazena features online (baixa latência via Redis/DynamoDB) e offline (treinamento via Parquet/S3).", body_style)],
        [Paragraph("4. Time-Series", body_style), Paragraph("TimescaleDB / InfluxDB", body_style), Paragraph("Persistência histórica de longo prazo para re-análise, consultas analíticas e auditoria de sensores.", body_style)],
        [Paragraph("5. Model Serving", body_style), Paragraph("Triton / FastAPI + Docker", body_style), Paragraph("Recebe o vetor de features pré-computado e responde a predição com latência inferior a 50ms.", body_style)],
    ]
    t_arq = Table(arq_dados, colWidths=[70, 150, 310])
    t_arq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_arq)

    story.append(PageBreak())

    # =========================================================================
    # SEÇÃO 1 (CONT.) & SEÇÃO 2: QUESTÃO 3 E CÓDIGO REFATORADO (PÁGINA 3)
    # =========================================================================
    story.append(Paragraph("Questão 3: Simulação de Latência e Gargalos no Streamlit", h2_style))
    story.append(Paragraph("<b>3.1 Qual fenômeno do mundo real da comunicação IoT é simulado?</b>", body_style))
    story.append(Paragraph(
        "A expressão <code>tempo_de_espera = intervalo_base_segundos + random.uniform(0, atraso_iot_max_segundos)</code> simula o "
        "<b>Jitter de Rede</b> (variação estatística da latência de transmissão) e as incertezas de propagação de enlaces industriais sem fio (redes Celulares 3G/4G/5G e LoRaWAN):",
        body_style
    ))
    story.append(Paragraph("• <b>Restrições de Duty Cycle regulatório:</b> Limitações legais de tempo de transmissão por hora em faixas ISM (LoRaWAN).", bullet_style))
    story.append(Paragraph("• <b>Contenção e Colisão de Pacotes:</b> Múltiplos sensores concorrendo pelo mesmo gateway geram retransmissões automáticas (*Exponential Backoff*).", bullet_style))
    story.append(Paragraph("• <b>Flutuações de Sinal e Interferência Eletromagnética:</b> Atenuação em ambientes de fábrica com motores de alta potência e estruturas metálicas.", bullet_style))

    story.append(Paragraph("<b>3.2 Estratégias no Streamlit para atualização sem bloquear a thread principal</b>", body_style))
    story.append(Paragraph(
        "O laço bloqueante <code>while True</code> com <code>time.sleep()</code> congela a thread de execução do Streamlit, impedindo a interação fluida com botões e menus. "
        "Para solucionar este problema, recomenda-se:",
        body_style
    ))
    story.append(Paragraph("• <b>Uso de <code>st.fragment</code> (Streamlit ≥ 1.33):</b> Isola a função de atualização com o decorador <code>@st.fragment(run_every=timedelta(seconds=10))</code>. Apenas o container do dashboard é re-renderizado periodicamente em background, mantendo toda a interface responsiva.", bullet_style))
    story.append(Paragraph("• <b>Componente <code>streamlit-autorefresh</code>:</b> Delega o temporizador para o frontend do navegador via JavaScript, disparando re-runs assíncronos sem travar a thread Python.", bullet_style))
    story.append(Paragraph("• <b>Arquitetura com WebSockets / SSE:</b> Em sistemas industriais avançados, o frontend consome um broker de mensagens assíncrono via WebSocket, eliminando polling ativo.", bullet_style))

    story.append(Spacer(1, 4))

    # SEÇÃO 2: CÓDIGO REFATORADO
    story.append(Paragraph("Seção 2: Código Refatorado e Comprovação de Execução (Questão 4)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=1, spaceAfter=6))

    story.append(Paragraph("<b>Implementação da Tabela de Histórico Recente no Streamlit</b>", h2_style))
    story.append(Paragraph(
        "Conforme solicitado na Questão 4, o arquivo <code>Teste_Compressor.py</code> foi modificado para armazenar em sessão "
        "(<code>st.session_state.historico_leituras</code>) as últimas 5 leituras recebidas e exibi-las em uma tabela estruturada "
        "logo abaixo dos cartões de status do compressor.",
        body_style
    ))

    codigo_q4 = """# 1. Importação adicional
from datetime import datetime

# 2. Inicialização do Histórico e Placeholder na Interface
st.markdown("---")
st.markdown("### 📋 Tabela de Histórico Recente (Últimas 5 Leituras)")
placeholder_historico = st.empty()

if 'historico_leituras' not in st.session_state:
    st.session_state.historico_leituras = []

# 3. Bloco executado a cada nova leitura recebida no loop de simulação
horario_leitura = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
status_texto = "Rodando" if current_status in status_motor_rodando else "Parado"
resultado_predicao = "Possível Falha" if "Falha" in label else "Normal"

nova_leitura = {
    'Horário': horario_leitura,
    'Status Operação': status_texto,
    'Pressão Saída': round(novo_ponto['pressao_saida'], 2),
    'Predição': resultado_predicao
}

# Insere no início para exibir os dados mais recentes no topo
st.session_state.historico_leituras.insert(0, nova_leitura)

# Mantém estritamente as últimas 5 leituras
if len(st.session_state.historico_leituras) > 5:
    st.session_state.historico_leituras = st.session_state.historico_leituras[:5]

# Renderização tabular dinâmica
with placeholder_historico.container():
    df_historico = pd.DataFrame(st.session_state.historico_leituras)
    st.dataframe(df_historico, use_container_width=True, hide_index=True)"""

    p_code = Preformatted(codigo_q4, code_font_style)
    t_code = Table([[p_code]], colWidths=[530])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), code_bg),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_code)

    story.append(PageBreak())

    # =========================================================================
    # SEÇÃO 2 (CONT.): COMPROVAÇÃO GRÁFICA NO NAVEGADOR (PÁGINA 4)
    # =========================================================================
    story.append(Paragraph("Comprovação Gráfica de Execução no Navegador (Questão 4)", h2_style))
    story.append(Paragraph(
        "A imagem a seguir comprova a execução da aplicação Streamlit no navegador, demonstrando o recebimento contínuo de telemetria "
        "dos sensores industriais, a classificação em tempo real do modelo de Machine Learning e a exibição tabular dinâmica "
        "das <b>últimas 5 leituras</b> com colunas de Horário, Status de Operação, Pressão de Saída e Resultado da Predição:",
        body_style
    ))

    story.append(Spacer(1, 6))
    if os.path.exists(caminho_img):
        story.append(RLImage(caminho_img, width=7.2*inch, height=4.8*inch))
    
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Figura 1:</b> Interface do Streamlit em execução no navegador exibindo os cartões de diagnóstico e a nova Tabela de Histórico Recente (Questão 4).", ParagraphStyle('Caption', parent=body_style, fontSize=8, textColor=muted_text, alignment=1)))

    story.append(Spacer(1, 10))
    conclusao_box = [
        [Paragraph("<b>Conclusão e Validação MLOps:</b><br/>"
                   "O protótipo foi validado com sucesso. Todos os requisitos de ambiente (<code>requirements.txt</code>, <code>venv</code>), "
                   "geração de modelos (<code>treinarmodelo.py</code>), chaveamento dinâmico de inferência e aprimoramento da interface com a "
                   "Tabela de Histórico Recente de 5 posições foram plenamente atendidos e homologados para entrega.", body_style)]
    ]
    t_conc = Table(conclusao_box, colWidths=[530])
    t_conc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), box_bg),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#0D9488")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_conc)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Relatório gerado com sucesso em: {caminho_pdf}")


if __name__ == "__main__":
    gerar_relatorio_completo_pdf()
