import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# 1. Configuração da página para ocupar a tela inteira (layout wide)
st.set_page_config(page_title="Dashboard PETR4", layout="wide", page_icon="📈")

# Estilo global refinado dos gráficos com Seaborn
sns.set_theme(style="whitegrid", font_scale=1.0)
palette_petr4 = sns.color_palette(["#008060", "#1f77b4", "#ff7f0e"])

# Cabeçalho principal
st.title("📊 Painel de Análise Financeira — PETR4 & Mercado B3")
st.caption("Acompanhamento histórico de resultados trimestrais da Petrobras e visão setorial da B3.")

# Definição das abas com nomes explicativos
tab1, tab2 = st.tabs(["📈 Histórico PETR4", "🏢 Visão de Mercado (B3)"])

# ==========================================
# ABA 1: PETROBRAS (PETR4)
# ==========================================
with tab1:
    df = pd.read_excel('PETR4_evolucao.xlsx')
    
    # Filtragem dos dados de lucro
    linhas = df['conta'] == 'lucro'
    colunas = ['trimestre', 'valor']
    dados = df[linhas][colunas].copy()
    
    # Conversão do lucro para Milhões de Reais (elimina o 1e8 feio do eixo Y)
    dados['lucro_milhoes'] = dados['valor'] / 1e6

    # Métricas de destaque (KPIs executivos)
    col1, col2, col3 = st.columns(3)
    lucro_recente = dados['lucro_milhoes'].iloc[-1]
    lucro_anterior = dados['lucro_milhoes'].iloc[-2]
    variacao = ((lucro_recente - lucro_anterior) / abs(lucro_anterior)) * 100
    pico_historico = dados['lucro_milhoes'].max()

    with col1:
        st.metric(
            label="Lucro Mais Recente",
            value=f"R$ {lucro_recente:,.0f} Mi".replace(",", "."),
            delta=f"{variacao:.1f}% vs tri anterior"
        )
    with col2:
        st.metric(
            label="Pico Histórico Trimestral",
            value=f"R$ {pico_historico:,.0f} Mi".replace(",", ".")
        )
    with col3:
        st.metric(
            label="Trimestres Mapeados",
            value=len(dados)
        )

    st.markdown("---")

    # Gráfico de Lucro em alta resolução
    fig1, ax1 = plt.subplots(figsize=(12, 5))
    sns.lineplot(
        data=dados,
        x='trimestre',
        y='lucro_milhoes',
        color='#008060',
        linewidth=2.5,
        marker='o',
        markersize=5,
        ax=ax1
    )
    
    # Preenchimento sombreado sob a curva
    ax1.fill_between(dados['trimestre'], dados['lucro_milhoes'], alpha=0.15, color='#008060')
    
    ax1.set_title("Evolução Histórica do Lucro Líquido (R$ Milhões)", fontsize=14, pad=15, weight='bold')
    ax1.set_xlabel("Trimestre", fontsize=11, labelpad=10)
    ax1.set_ylabel("Lucro (R$ Milhões)", fontsize=11, labelpad=10)
    
    # Rotação e espaçamento dos trimestres para evitar texto sobreposto
    ax1.tick_params(axis='x', rotation=45)
    # Exibe rótulos com espaçamento limpo caso haja muitos trimestres
    for idx, label in enumerate(ax1.xaxis.get_ticklabels()):
        if idx % 2 != 0 and len(dados) > 20:
            label.set_visible(False)

    st.pyplot(fig1)

    # Tabela com expansor colapsável para não poluir a tela
    with st.expander("📋 Ver Tabela Completa de Dados"):
        st.dataframe(df, use_container_width=True)

# ==========================================
# ABA 2: PLANILHÃO B3
# ==========================================
with tab2:
    try:
        df_planilhao = pd.read_excel('planilhao_b3.xlsx')
        
        st.subheader("Concentração Setorial na B3")
        
        # Agrupamento por setor
        df_size = df_planilhao.groupby('setor').size().sort_values(ascending=False)

        col_left, col_right = st.columns([2, 1])

        with col_left:
            # Gráfico de barras horizontal (mais elegante e legível para categorias)
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            sns.barplot(
                x=df_size.values,
                y=df_size.index,
                palette="crest",
                ax=ax2
            )
            ax2.set_title("Número de Empresas Listadas por Setor", fontsize=13, pad=12, weight='bold')
            ax2.set_xlabel("Quantidade de Companhias", fontsize=11)
            ax2.set_ylabel("Setor", fontsize=11)
            st.pyplot(fig2)

        with col_right:
            st.markdown("#### Resumo")
            st.dataframe(
                df_size.reset_index().rename(columns={0: 'Empresas', 'setor': 'Setor'}),
                use_container_width=True,
                height=350
            )

        with st.expander("📋 Ver Base Completa do Planilhão"):
            st.dataframe(df_planilhao, use_container_width=True)

    except Exception as e:
        st.info("Carregando ou arquivo `planilhao_b3.xlsx` não encontrado.")