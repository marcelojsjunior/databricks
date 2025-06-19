import pandas as pd
import plotly.express as px
import streamlit as st

# Carregando os dados do CSV hospedado no GitHub
url = "https://raw.githubusercontent.com/marcelojsjunior/databricks/main/transacoes_token.csv"
df = pd.read_csv(url)
df["data"] = pd.to_datetime(df["data"])

st.title("📊 Top 20 - Métricas de Tokens negociados em DEX por dia")

# 1. Selecionar os 20 tokens com mais total_trades no período
top_tokens = (
    df.groupby("nome_token")["total_trades"]
    .sum()
    .sort_values(ascending=False)
    .head(20)
    .index
    .tolist()
)

df_top = df[df["nome_token"].isin(top_tokens)]

# 2. Selectbox para o token
token = st.selectbox("🔎 Selecione o token", sorted(df_top["nome_token"].unique()))

# 3. Selectbox para a métrica
metricas_legiveis = {
    "Volume em USD": "volume_total_usd",
    "Total de Trades": "total_trades",
    "Média de Tokens por Transação": "media_quantia_token"
}
metrica_legivel = st.selectbox("📈 Selecione a métrica", list(metricas_legiveis.keys()))
metrica = metricas_legiveis[metrica_legivel]

# 4. Filtrar dados
df_filtrado = df_top[df_top["nome_token"] == token].sort_values("data")

# 5. Gráfico com range slider
fig = px.line(
    df_filtrado,
    x="data",
    y=metrica,
    color="direcao",
    markers=True,
    title=f"{metrica_legivel} por dia – {token}",
    template="plotly_white"
)

fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=[
                dict(count=7, label="7d", step="day", stepmode="backward"),
                dict(count=14, label="14d", step="day", stepmode="backward"),
                dict(count=30, label="30d", step="day", stepmode="backward"),
                dict(step="all", label="Tudo")
            ]
        ),
        rangeslider=dict(visible=True),
        type="date"
    )
)

st.plotly_chart(fig, use_container_width=True)

import pandas as pd
import plotly.express as px
import streamlit as st

# Carrega os dados da tabela Silver exportada como CSV no GitHub
url = "https://raw.githubusercontent.com/marcelojsjunior/databricks/main/analise_rede.csv"
df = pd.read_csv(url)
df["data"] = pd.to_datetime(df["data"])

st.title("🌐 Análise por Rede – Volume e Transações em DEX")

# Selectbox da métrica
metricas_legiveis = {
    "Volume em USD": "volume_total_usd",
    "Total de Trades": "total_trades"
}
metrica_legivel = st.selectbox("📊 Selecione a métrica", list(metricas_legiveis.keys()))
metrica = metricas_legiveis[metrica_legivel]

# Filtro por granularidade: data ou nome_dia
granularidade = st.radio("🗂️ Visualizar por", ["Dia (data)", "Dia da Semana (nome_dia)"])

if granularidade == "Dia (data)":
    df_plot = df.sort_values("data")
    eixo_x = "data"
else:
    dias_ordem = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    df_plot = (
        df.groupby(["nome_dia", "rede"])[metrica]
        .sum()
        .reset_index()
        .sort_values("nome_dia", key=lambda x: [dias_ordem.index(d) for d in x])
    )
    eixo_x = "nome_dia"

# Gráfico
fig = px.line(
    df_plot,
    x=eixo_x,
    y=metrica,
    color="rede",
    markers=True,
    title=f"{metrica_legivel} por {'dia' if granularidade == 'Dia (data)' else 'dia da semana'} – por rede",
    template="plotly_white"
)

fig.update_xaxes(rangeslider_visible=True)

st.plotly_chart(fig, use_container_width=True)
