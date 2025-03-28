import streamlit as st
from modules import jogadores, equipes, jogos, estatisticas

st.set_page_config(page_title="CBF Manager", layout="centered")
st.title("Cadastro de Jogos do Campeonato Brasileiro")
page = st.sidebar.selectbox("Escolha uma página", ["Cadastrar Jogador", "Cadastrar Equipe", "Cadastrar Jogo", "Registrar Estatísticas"])

if page == "Cadastrar Jogador":
    jogadores.cadastrar_jogador()
elif page == "Cadastrar Equipe":
    equipes.cadastrar_equipe()
elif page == "Cadastrar Jogo":
    jogos.cadastrar_jogo()
elif page == "Registrar Estatísticas":
    estatisticas.registrar_estatisticas()
