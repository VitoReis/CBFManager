import streamlit as st

st.set_page_config(page_title="CBF Manager", page_icon="./assets/CBF.png")

from modules import pessoas, jogadores, equipes, jogos, estatisticas
from database.connection import get_db
from database.models import get_collections


with st.spinner("Conectando ao banco de dados..."):
    db = get_db()
    collections = get_collections(db)
    pessoas_collection = db["pessoas"]

if "logado" not in st.session_state:
    st.session_state.logado = False
if "pessoa" not in st.session_state:
    st.session_state.pessoa = None

if not st.session_state.logado:
    st.title("🔐 Login - CBF Manager")

    login = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        with st.spinner("Verificando credenciais..."):
            pessoa = pessoas_collection.find_one({"login": login, "senha": senha})
        if pessoa:
            st.success(f"✅ Bem-vindo, {pessoa['login']}!")
            st.session_state.logado = True
            st.session_state.pessoa = pessoa
            st.rerun()
        else:
            st.error("🚫 Login ou senha inválidos")

else:
    st.sidebar.success(
        f"👤 Logado como: {st.session_state.pessoa['login']} ({st.session_state.pessoa['tipo']})"
    )

    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.session_state.pessoa = None
        st.rerun()

    st.title("⚽ CBF Manager")

    if st.session_state.pessoa["tipo"] == "administrador":
        page = st.sidebar.selectbox(
            "📋 Menu do Administrador",
            [
                "Cadastrar Pessoa",
                "Deletar Pessoa",
                "Cadastrar Jogador",
                "Editar Jogador",
                "Deletar Jogador",
                "Cadastrar Equipe",
                "Deletar Equipe",
                "Cadastrar Jogo",
                "Editar Jogo",
                "Deletar Jogo",
                "Cadastrar Estatísticas",
                "Editar Estatísticas",
                "Deletar Estatísticas",
            ],
        )

        if page == "Cadastrar Pessoa":
            pessoas.cadastrar_pessoa()
        elif page == "Deletar Pessoa":
            pessoas.deletar_pessoa()
        elif page == "Cadastrar Jogador":
            jogadores.cadastrar_jogador()
        elif page == "Editar Jogador":
            jogadores.editar_jogador()
        elif page == "Deletar Jogador":
            jogadores.deletar_jogador()
        elif page == "Cadastrar Equipe":
            equipes.cadastrar_equipe()
        elif page == "Deletar Equipe":
            equipes.deletar_equipe()
        elif page == "Cadastrar Jogo":
            jogos.cadastrar_jogo()
        elif page == "Editar Jogo":
            jogos.editar_jogo()
        elif page == "Deletar Jogo":
            jogos.deletar_jogo()
        elif page == "Cadastrar Estatísticas":
            estatisticas.cadastrar_estatisticas()
        elif page == "Editar Estatísticas":
            estatisticas.editar_estatisticas()
        elif page == "Deletar Estatísticas":
            estatisticas.deletar_estatisticas()

    elif st.session_state.pessoa["tipo"] == "usuario":
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
