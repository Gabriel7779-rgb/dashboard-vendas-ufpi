import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Vendas", page_icon="📊", layout="wide")
st.title("📊 Dashboard Analítico de Vendas")
st.caption("Projeto acadêmico demonstrativo | Introdução à Visualização da Informação")
st.info("Os dados deste projeto são fictícios e foram criados apenas para fins acadêmicos.")

@st.cache_data
def carregar_dados():
    dados = pd.read_csv("vendas.csv", parse_dates=["data"])
    dados["mes"] = dados["data"].dt.to_period("M").astype(str)
    return dados

df = carregar_dados()

st.sidebar.header("Filtros")
data_min, data_max = df["data"].min().date(), df["data"].max().date()
periodo = st.sidebar.date_input("Período", value=(data_min, data_max),
                                min_value=data_min, max_value=data_max)
regioes = st.sidebar.multiselect("Região", sorted(df["regiao"].unique()),
                                 default=sorted(df["regiao"].unique()))
categorias = st.sidebar.multiselect("Categoria", sorted(df["categoria"].unique()),
                                    default=sorted(df["categoria"].unique()))

if isinstance(periodo, (tuple, list)) and len(periodo) == 2:
    inicio, fim = pd.Timestamp(periodo[0]), pd.Timestamp(periodo[1])
else:
    inicio, fim = pd.Timestamp(data_min), pd.Timestamp(data_max)

filtrado = df[
    df["data"].between(inicio, fim) &
    df["regiao"].isin(regioes) &
    df["categoria"].isin(categorias)
].copy()

if filtrado.empty:
    st.warning("Nenhum registro corresponde aos filtros selecionados. Ajuste os filtros na barra lateral.")
    st.stop()

total_vendas = filtrado["vendas"].sum()
total_pedidos = filtrado["pedido_id"].nunique()
ticket_medio = total_vendas / total_pedidos if total_pedidos else 0

m1, m2, m3 = st.columns(3)
m1.metric("Vendas totais", f"R$ {total_vendas:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
m2.metric("Quantidade de pedidos", f"{total_pedidos:,}".replace(",", "."))
m3.metric("Valor médio por pedido", f"R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.subheader("Visões coordenadas")
st.write("Use os filtros laterais para atualizar simultaneamente os gráficos e a tabela. Também é possível selecionar pontos/barras para destacar os registros correspondentes.")

mensal = filtrado.groupby("mes", as_index=False)["vendas"].sum()
fig_linha = px.line(mensal, x="mes", y="vendas", markers=True,
                    title="1. Evolução mensal das vendas",
                    labels={"mes":"Mês", "vendas":"Vendas (R$)"})
fig_linha.update_traces(line=dict(width=3), marker=dict(size=8))
fig_linha.update_layout(hovermode="x unified")
eventos_linha = st.plotly_chart(fig_linha, use_container_width=True,
                                on_select="rerun", selection_mode="points",
                                key="grafico_mensal")

por_categoria = filtrado.groupby("categoria", as_index=False)["vendas"].sum().sort_values("vendas", ascending=False)
fig_barra = px.bar(por_categoria, x="categoria", y="vendas",
                   title="2. Vendas por categoria",
                   labels={"categoria":"Categoria", "vendas":"Vendas (R$)"},
                   color="categoria", color_discrete_sequence=px.colors.qualitative.Safe)
fig_barra.update_layout(showlegend=False)
eventos_barra = st.plotly_chart(fig_barra, use_container_width=True,
                                on_select="rerun", selection_mode="points",
                                key="grafico_categoria")

# Cross-filter selected category or month where the Plotly selection API exposes points.
detalhes = filtrado.copy()
try:
    pontos = eventos_barra.selection.points
    if pontos:
        categorias_selecionadas = {p.get("x") for p in pontos if p.get("x") is not None}
        if categorias_selecionadas:
            detalhes = detalhes[detalhes["categoria"].isin(categorias_selecionadas)]
except Exception:
    pass

try:
    pontos = eventos_linha.selection.points
    if pontos:
        meses_selecionados = {p.get("x") for p in pontos if p.get("x") is not None}
        if meses_selecionados:
            detalhes = detalhes[detalhes["mes"].isin(meses_selecionados)]
except Exception:
    pass

st.subheader("3. Detalhamento sob demanda")
st.caption("A tabela respeita os filtros laterais e, quando suportado pela seleção do gráfico, os pontos e barras selecionados.")
busca = st.text_input("Buscar produto ou número do pedido", placeholder="Ex.: Fone Bluetooth ou P0001")
if busca:
    detalhes = detalhes[
        detalhes["produto"].str.contains(busca, case=False, na=False) |
        detalhes["pedido_id"].str.contains(busca, case=False, na=False)
    ]

colunas = ["pedido_id", "data", "regiao", "categoria", "produto", "quantidade", "valor_unitario", "vendas"]
st.dataframe(detalhes[colunas].sort_values("data", ascending=False),
             use_container_width=True, hide_index=True,
             column_config={
                 "data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
                 "valor_unitario": st.column_config.NumberColumn("Valor unitário", format="R$ %.2f"),
                 "vendas": st.column_config.NumberColumn("Vendas", format="R$ %.2f"),
             })
st.caption(f"Registros exibidos: {len(detalhes)} de {len(df)} registros originais.")

with st.expander("Sobre o projeto e os princípios de visualização"):
    st.markdown("""
    - **Visão geral:** série temporal das vendas mensais.
    - **Distribuição categórica:** barras ordenadas por valor vendido.
    - **Detalhes sob demanda:** tabela filtrável e busca por pedido/produto.
    - **Visões coordenadas:** filtros comuns atualizam os três componentes; seleção de pontos/barras também restringe a tabela.
    - **Acessibilidade:** paleta qualitativa, rótulos explícitos, contraste e ausência de dependência exclusiva da cor.
    - **Data-Ink Ratio:** elementos decorativos reduzidos para priorizar os dados.
    """)
