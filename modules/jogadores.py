import streamlit as st
from database.connection import get_db
from database.models import get_collections
from bson import ObjectId

with st.spinner("Conectando ao banco de dados..."):
    db = get_db()
    collections = get_collections(db)


def cadastrar_jogador():
    st.header("Cadastrar Jogador")
    nome_jogador = st.text_input("Nome do Jogador:")

    with st.spinner("Carregando equipes..."):
        equipes = list(collections["equipes"].find())

    if not equipes:
        st.error("Não há equipes cadastradas. Cadastre uma equipe primeiro.")
        return

    lista_equipes = [f"{equipe['nome']} (ID: {equipe['_id']})" for equipe in equipes]
    equipe_selecionada = st.selectbox("Equipe:", lista_equipes)

    equipe_id = equipe_selecionada.split(" (ID: ")[1].strip(")")
    equipe_id = ObjectId(equipe_id)

    numero_jogador = st.number_input("Número do Jogador:", min_value=1, step=1)

    if st.button("Cadastrar"):
        with st.spinner("Verificando jogador existente..."):
            jogador_existente = collections["jogadores"].find_one(
                {"equipe_id": equipe_id, "numero": numero_jogador}
            )
        if jogador_existente:
            st.error(
                f"Já existe um jogador com o número {numero_jogador} na equipe selecionada."
            )
        else:
            with st.spinner("Cadastrando jogador..."):
                collections["jogadores"].insert_one(
                    {
                        "nome": nome_jogador,
                        "equipe_id": equipe_id,
                        "numero": numero_jogador,
                    }
                )
            st.success(f"Jogador {nome_jogador} cadastrado com sucesso na equipe!")


def deletar_jogador():
    st.header("Deletar Jogador")

    with st.spinner("Carregando jogadores..."):
        jogadores = list(db["jogadores"].find())

    lista_jogadores = [
        f"{jogador['nome']} (ID: {jogador['_id']})" for jogador in jogadores
    ]

    jogador_selecionado = st.selectbox("Escolha um jogador:", lista_jogadores)

    if st.button("Deletar"):
        jogador_id = jogador_selecionado.split(" (ID: ")[1].strip(")")
        try:
            with st.spinner("Deletando jogador..."):
                collections["jogadores"].delete_one({"_id": ObjectId(jogador_id)})
            st.success("Jogador deletado com sucesso!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao deletar: {e}")


def visualizar_jogador():
    st.subheader("Jogadores Cadastrados")

    with st.spinner("Carregando jogadores..."):
        jogadores = list(collections["jogadores"].find())

    if jogadores:
        dados_tabela = []

        for jogador in jogadores:
            with st.spinner(f"Carregando equipe do jogador {jogador['nome']}..."):
                equipe = collections["equipes"].find_one({"_id": jogador["equipe_id"]})
            dados_tabela.append(
                {
                    "Nome": jogador["nome"],
                    "Número": jogador["numero"],
                    "Equipe": equipe["nome"] if equipe else "Desconhecida",
                }
            )

        st.dataframe(dados_tabela)
    else:
        st.info("Nenhum jogador cadastrado ainda.")
