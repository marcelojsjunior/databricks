import pandas as pd
import plotly.express as px
import streamlit as st

url = "https://raw.githubusercontent.com/marcelojsjunior/databricks/main/transacoes_token.csv"
df = pd.read_csv(url)
df["data"] = pd.to_datetime(df["data"])

st.title("📊 Top 20 - Métricas de Tokens negociados em DEX por dia")

top_tokens = (
    df.groupby("nome_token")["total_trades"]
    .sum()
    .sort_values(ascending=False)
    .head(20)
    .index
    .tolist()
)

df_top = df[df["nome_token"].isin(top_tokens)]

token = st.selectbox("🔎 Selecione o token", sorted(df_top["nome_token"].unique()))
metrica = st.selectbox("📈 Selecione a métrica", {
    "Volume em USD": "volume_total_usd",
    "Total de Trades": "total_trades",
    "Média de Tokens por Transação": "media_quantia_token"
})

df_filtrado = df_top[df_top["nome_token"] == token].sort_values("data")


fig = px.line(
    df_filtrado,
    x="data",
    y=metrica,
    color="direcao",
    markers=True,
    title=f"{metrica.replace('_', ' ').capitalize()} por dia – {token}",
    template="plotly_white"
)


fig.update_xaxes(nticks=len(df_filtrado["data"].unique()))


st.plotly_chart(fig, use_container_width=True)
