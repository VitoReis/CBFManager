import streamlit as st
from database.connection import get_db
from database.models import get_collections

db = get_db()
collections = get_collections(db)

def cadastrar_equipe():
    st.header("Cadastrar Equipe")
    nome_equipe = st.text_input("Nome da Equipe:")

    if st.button("Cadastrar Equipe"):
        equipe_existente = collections["equipes"].find_one({"nome": nome_equipe})
        if equipe_existente:
            st.error(f"Já existe uma equipe com o nome {nome_equipe}.")
        else:
            collections["equipes"].insert_one({"nome": nome_equipe})
            st.success(f"Equipe {nome_equipe} cadastrada!")

    # TABELA DE EQUIPES
    st.subheader("Equipes Cadastradas")
    equipes = list(collections["equipes"].find())

    if equipes:
        dados_tabela = [{"Nome da Equipe": equipe["nome"]} for equipe in equipes]
        st.dataframe(dados_tabela)
    else:
        st.info("Nenhuma equipe cadastrada ainda.")