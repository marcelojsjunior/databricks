import pandas as pd
import plotly.express as px
import streamlit as st


## Gráfico 1
url = "https://raw.githubusercontent.com/marcelojsjunior/databricks/main/transacoes_token.csv"
df = pd.read_csv(url)
df["data"] = pd.to_datetime(df["data"])

st.title("Top 20 - Métricas de Tokens negociados em DEX por dia")

top_tokens = (
    df.groupby("nome_token")["total_trades"]
    .sum()
    .sort_values(ascending=False)
    .head(20)
    .index
    .tolist()
)

df_top = df[df["nome_token"].isin(top_tokens)]

token = st.selectbox("Selecione o token", sorted(df_top["nome_token"].unique()))

metricas_legiveis = {
    "Volume em USD": "volume_total_usd",
    "Total de Trades": "total_trades",
    "Média de Tokens por Transação": "media_quantia_token"
}
metrica_legivel = st.selectbox("Selecione a métrica", list(metricas_legiveis.keys()))
metrica = metricas_legiveis[metrica_legivel]

df_filtrado = df_top[df_top["nome_token"] == token].sort_values("data")

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

## Gráfico 2

import pandas as pd
import plotly.express as px
import streamlit as st

url = "https://raw.githubusercontent.com/marcelojsjunior/databricks/main/analise_exchange.csv"
df = pd.read_csv(url)
df["data"] = pd.to_datetime(df["data"])

st.title("Top 20 Exchanges – Métricas por Dia")

top_exchanges = (
    df.groupby("nome_exchange")["total_trades"]
    .sum()
    .sort_values(ascending=False)
    .head(20)
    .index
    .tolist()
)

df_top = df[df["nome_exchange"].isin(top_exchanges)]

exchange = st.selectbox("Selecione a exchange", sorted(df_top["nome_exchange"].unique()))

metricas_legiveis = {
    "Volume em USD": "volume_usd",
    "Total de Trades": "total_trades",
    "Total de Transações": "total_transacoes",
    "Preço Médio em USD": "preco_medio_usd"
}
metrica_legivel = st.selectbox("Selecione a métrica", list(metricas_legiveis.keys()))
metrica = metricas_legiveis[metrica_legivel]

df_filtrado = df_top[df_top["nome_exchange"] == exchange].sort_values("data")

fig = px.line(
    df_filtrado,
    x="data",
    y=metrica,
    color="direcao",
    markers=True,
    title=f"{metrica_legivel} por dia – {exchange}",
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





## Gráfico 3
import pandas as pd
import plotly.express as px
import streamlit as st

url = "https://raw.githubusercontent.com/marcelojsjunior/databricks/main/analise_rede.csv"
df = pd.read_csv(url)
df["data"] = pd.to_datetime(df["data"])

st.title("Análise por Rede – Volume e Transações em DEX")

metricas_legiveis = {
    "Volume em USD": "volume_total_usd",
    "Total de Trades": "total_trades"
}
metrica_legivel = st.selectbox("Selecione a métrica", list(metricas_legiveis.keys()))
metrica = metricas_legiveis[metrica_legivel]

granularidade = st.radio("Visualizar por", ["Dia (data)", "Dia da Semana (nome_dia)"])

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
