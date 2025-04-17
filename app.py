import streamlit as st

st.set_page_config(page_title="CBF Manager", page_icon="./assets/CBF.png")

from modules import usuarios, jogadores, equipes, jogos, estatisticas
from database.connection import get_db
from database.models import get_collections


with st.spinner("Conectando ao banco de dados..."):
    db = get_db()
    collections = get_collections(db)
    usuarios_collection = db["usuarios"]

if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = None

if not st.session_state.logado:
    st.title("🔐 Login - CBF Manager")

    login = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        with st.spinner("Verificando credenciais..."):
            usuario = usuarios_collection.find_one({"login": login, "senha": senha})
        if usuario:
            st.success(f"✅ Bem-vindo, {usuario['login']}!")
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.rerun()
        else:
            st.error("🚫 Usuário ou senha inválidos")

else:
    st.sidebar.success(
        f"👤 Logado como: {st.session_state.usuario['login']} ({st.session_state.usuario['tipo']})"
    )

    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.session_state.usuario = None
        st.rerun()

    st.title("⚽ CBF Manager")

    if st.session_state.usuario["tipo"] == "admin":
        page = st.sidebar.selectbox(
            "📋 Menu do Administrador",
            [
                "Cadastrar Usuario",
                "Deletar Usuario",
                "Cadastrar Jogador",
                "Deletar Jogador",
                "Cadastrar Equipe",
                "Deletar Equipe",
                "Cadastrar Jogo",
                "Deletar Jogo",
                "Cadastrar Estatísticas",
                "Deletar Estatísticas",
            ],
        )

        if page == "Cadastrar Usuario":
            usuarios.cadastrar_usuario()
        elif page == "Deletar Usuario":
            usuarios.deletar_usuario()
        elif page == "Cadastrar Jogador":
            jogadores.cadastrar_jogador()
        elif page == "Deletar Jogador":
            jogadores.deletar_jogador()
        elif page == "Cadastrar Equipe":
            equipes.cadastrar_equipe()
        elif page == "Deletar Equipe":
            equipes.deletar_equipe()
        elif page == "Cadastrar Jogo":
            jogos.cadastrar_jogo()
        elif page == "Deletar Jogo":
            jogos.deletar_jogo()
        elif page == "Cadastrar Estatísticas":
            estatisticas.cadastrar_estatisticas()
        elif page == "Deletar Estatísticas":
            estatisticas.deletar_estatisticas()

    elif st.session_state.usuario["tipo"] == "usuario":
        page = st.sidebar.selectbox(
            "📋 Menu do Usuário",
            [
                "Visualizar Jogadores",
                "Visualizar Equipes",
                "Visualizar Jogos",
                "Visualizar Estatísticas",
            ],
        )

        if page == "Visualizar Jogadores":
            jogadores.visualizar_jogador()
        elif page == "Visualizar Equipes":
            equipes.visualizar_equipe()
        elif page == "Visualizar Jogos":
            jogos.visualizar_jogo()
        elif page == "Visualizar Estatísticas":
            estatisticas.visualizar_estatisticas()
