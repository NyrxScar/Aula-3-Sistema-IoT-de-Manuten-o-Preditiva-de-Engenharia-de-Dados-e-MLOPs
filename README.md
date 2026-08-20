# Sistema IoT de Manutenção Preditiva em Tempo Real

**Disciplina:** Engenharia de Dados e MLOps  
**Empresa / Caso de Estudo:** Compressores do Brasil S.A.  
**Tecnologias:** Python, Streamlit, Scikit-learn, Joblib, Pandas

---

## 📌 Visão Geral do Projeto

Este projeto implementa e avalia um simulador interativo em **Streamlit** para manutenção preditiva em tempo real de compressores industriais operados pela *Compressores do Brasil S.A.*. O sistema recebe telemetria IoT simulando atrasos de transmissão de redes industriais/celulares (LoRaWAN/3G/4G) e faz o chaveamento dinâmico de inferência entre dois modelos de Machine Learning (Random Forest) pré-treinados:

1. **Modelo de Motor Rodando (`modelo_motor_rodando.joblib`):** Avalia a probabilidade de falhas iminentes em 7 dias com base em dados operacionais e variáveis de engenharia de atributos (médias móveis, desvios).
2. **Modelo de Motor Parado (`modelo_motor_parado.joblib`):** Avalia a integridade do equipamento durante períodos de inatividade e paradas programadas.

---

## 🚀 Estrutura de Arquivos

```
├── .gitignore                      # Configuração de arquivos ignorados pelo Git
├── LICENSE                         # Licença do projeto
├── README.md                       # Documentação completa do projeto
├── requirements.txt                # Dependências necessárias para o projeto
├── treinarmodelo.py                # Script de geração dos modelos sintéticos (.joblib)
├── Teste_Compressor.py             # Aplicação Streamlit com Tabela de Histórico Recente
├── modelo_motor_rodando.joblib     # Modelo treinado para compressor em operação
├── modelo_motor_parado.joblib      # Modelo treinado para compressor parado
├── relatorio_atividade.pdf         # Relatório final formatado em PDF para entrega
└── venv/                           # Ambiente virtual Python
```

---

## 🛠️ Pré-requisitos e Instalação

### 1. Clonar o repositório e acessar a pasta:
```bash
git clone <url-do-repositorio>
cd Aula-3-Sistema-IoT-de-Manuten-o-Preditiva-de-Engenharia-de-Dados-e-MLOPs
```

### 2. Criar e ativar o ambiente virtual (venv):

**No Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**No Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências:
```bash
pip install -r requirements.txt
```

As principais bibliotecas instaladas são:
- `streamlit`: Criação da interface web reativa em tempo real.
- `pandas`: Estruturação e manipulação tabular de dados de sensores e histórico.
- `scikit-learn`: Treinamento e inferência dos modelos RandomForestClassifier.
- `joblib`: Serialização e carregamento dos modelos treinados.

---

## ⚙️ Como Executar o Projeto

### Passo 1: Treinar e Gerar os Modelos (.joblib)
Antes de executar o aplicativo pela primeira vez, execute o script de treinamento:
```bash
python treinarmodelo.py
```
*Saída esperada:*
```text
Gerando modelos de IA...
 Sucesso! Modelos gerados com sucesso na pasta:
   - modelo_motor_rodando.joblib
   - modelo_motor_parado.joblib
```

### Passo 2: Executar o Simulador Streamlit
Inicie o dashboard interativo:
```bash
streamlit run Teste_Compressor.py
```
Acesse o aplicativo no navegador através do endereço: `http://localhost:8501`.

---

## 📋 Resumo das Questões da Atividade

### Questão 1: Arquitetura de Roteamento de Modelos (Teórica)
- **Mecanismo de Decisão:** A função `prever_ponto_dinamicamente()` inspeciona o campo `status_operacao`. Se o valor estiver na lista `status_motor_rodando = [2, 7, 8, 9, 10, 11, 12, 13, 14]`, o modelo `modelo_motor_rodando.joblib` é acionado recebendo features brutas + calculadas de 7 dias. Caso contrário, o `modelo_motor_parado.joblib` é selecionado.
- **Vantagem do Chaveamento:** Contextos operacionais distintos possuem distribuições estatísticas completamente divergentes. Separar os modelos evita confusão nos padrões de decisão, reduz ruído, melhora a acurácia e simplifica a manutenção/retreinamento independente.

### Questão 2: Análise Crítica de Feature Engineering
- **Problemas da Aproximação por Fatores Fixos:** Multiplicar o dado instantâneo por `0.95` ou `0.1` elimina a memória temporal real dos 7 dias anteriores, gera multicolinearidade artificial, mascara anomalias reais e causa degradação de performance por *data drift* em produção.
- **Arquitetura em Nuvem Ideal:** Ingestão via **Apache Kafka / AWS Kinesis** $\rightarrow$ Processamento de Streams com **Apache Flink / Spark Structured Streaming** calculando agregações sobre janelas deslizantes de 7 dias $\rightarrow$ Armazenamento em **Feature Store (Feast / SageMaker)** e banco de séries temporais (**TimescaleDB / InfluxDB**) $\rightarrow$ Inferência no **Model Serving**.

### Questão 3: Simulação de Latência e Gargalos no Streamlit
- **Fenômeno Simulado:** Jitter de rede, latência variável e contenção de canais de transmissão típicos de redes sem fio industriais, celulares (3G/4G/5G) e LoRaWAN (duty cycle, atrasos de gateway e retransmissões).
- **Solução de Não-Bloqueio no Streamlit:** Utilização do decorador `@st.fragment(run_every=timedelta(seconds=10))` (Streamlit $\ge$ 1.33) ou bibliotecas como `streamlit-autorefresh` em substituição ao laço bloqueante `while True` com `time.sleep()`.

### Questão 4: Implementação da Tabela de Histórico Recente
- Implementação de armazenamento no `st.session_state.historico_leituras` contendo as últimas 5 leituras (`Horário`, `Status Operação`, `Pressão Saída`, `Predição`), renderizadas dinamicamente via `st.dataframe()`.

---

## 📄 Relatório em PDF
O relatório completo formatado contendo capa institucional, respostas analíticas detalhadas, trechos de código e comprovação gráfica de execução está disponível no arquivo `relatorio_atividade.pdf`.
