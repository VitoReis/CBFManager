import streamlit as st
from database.connection import get_db
from database.models import get_collections
from bson import ObjectId

with st.spinner("Conectando ao banco de dados..."):
    db = get_db()
    collections = get_collections(db)


def cadastrar_equipe():
    st.header("Cadastrar Equipe")
    nome_equipe = st.text_input("Nome da Equipe:")

    if st.button("Cadastrar"):
        with st.spinner("Verificando existência da equipe..."):
            equipe_existente = collections["equipes"].find_one({"nome": nome_equipe})
        if equipe_existente:
            st.error(f"Já existe uma equipe com o nome {nome_equipe}.")
        else:
            with st.spinner("Cadastrando equipe..."):
                collections["equipes"].insert_one({"nome": nome_equipe})
            st.success(f"Equipe {nome_equipe} cadastrada!")


def desassociar_jogadores_da_equipe(equipe_id):
    """Define o campo equipe_id como None para todos os jogadores da equipe deletada."""
    with st.spinner("Desassociando jogadores da equipe..."):
        collections["jogadores"].update_many(
            {"equipe_id": ObjectId(equipe_id)}, {"$set": {"equipe_id": None}}
        )


def deletar_equipe():
    st.header("Deletar Equipe")

    with st.spinner("Carregando equipes..."):
        equipes = list(db["equipes"].find())

    if not equipes:
        st.info("Nenhuma equipe disponível para deletar.")
        return

    lista_equipes = [f"{equipe['nome']} (ID: {equipe['_id']})" for equipe in equipes]
    equipe_selecionada = st.selectbox("Escolha uma equipe:", lista_equipes)

    if st.button("Deletar"):
        equipe_id = equipe_selecionada.split(" (ID: ")[1].strip(")")
        try:
            desassociar_jogadores_da_equipe(ObjectId(equipe_id))
            with st.spinner("Deletando equipe..."):
                collections["equipes"].delete_one({"_id": ObjectId(equipe_id)})
            st.success("Equipe deletada com sucesso!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao deletar: {e}")


def visualizar_equipe():
    st.subheader("Equipes Cadastradas")
    with st.spinner("Carregando dados..."):
        equipes = list(collections["equipes"].find())

    if equipes:
        dados_tabela = [{"Nome da Equipe": equipe["nome"]} for equipe in equipes]
        st.dataframe(dados_tabela)
    else:
        st.info("Nenhuma equipe cadastrada ainda.")
