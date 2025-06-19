import pandas as pd
import plotly.express as px
import streamlit as st


url = "https://raw.githubusercontent.com/marcelojsjunior/databricks/main/transacoes_token.csv"

df = pd.read_csv(url)
df["data"] = pd.to_datetime(df["data"])

st.title("📊 Volume de Tokens negociados em DEX")
token = st.selectbox("Selecione o token", df["nome_token"].unique().tolist())
df_filtrado = df[df["nome_token"] == token].sort_values("data")

fig = px.line(
    df_filtrado,
    x="data",
    y="volume_total_usd",
    color="direcao",
    markers=True,
    title=f"Volume por dia – {token}",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)
