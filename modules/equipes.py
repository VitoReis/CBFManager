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

    if st.button("Cadastrar Equipe"):
        with st.spinner("Verificando existência da equipe..."):
            equipe_existente = collections["equipes"].find_one({"nome": nome_equipe})
        if equipe_existente:
            st.error(f"Já existe uma equipe com o nome {nome_equipe}.")
        else:
            with st.spinner("Cadastrando equipe..."):
                collections["equipes"].insert_one({"nome": nome_equipe})
            st.success(f"Equipe '{nome_equipe}' cadastrada!")


# CASCADE JOGADORES
def desassociar_jogadores_da_equipe(nome_equipe):
    with st.spinner("Desassociando jogadores da equipe..."):
        collections["jogadores"].update_many(
            {"nome_equipe": nome_equipe}, {"$set": {"nome_equipe": None}}
        )


# CASCADE JOGOS E ESTATISTICAS
def deletar_jogos_da_equipe(nome_equipe):
    with st.spinner("Deletando jogos e estatísticas relacionadas à equipe..."):
        jogos_associados = collections["jogos"].find(
            {"$or": [{"nome_equipe1": nome_equipe}, {"nome_equipe2": nome_equipe}]}
        )

        for jogo in jogos_associados:
            jogo_id = jogo["_id"]
            collections["estatisticas"].delete_many({"jogo_id": jogo_id})
            collections["jogos"].delete_one({"_id": jogo_id})


def deletar_equipe():
    st.header("Deletar Equipe")

    with st.spinner("Carregando equipes..."):
        equipes = list(db["equipes"].find())

    if not equipes:
        st.info("Nenhuma equipe disponível para deletar.")
        return

    lista_nomes_equipes = [equipe["nome"] for equipe in equipes]
    nome_equipe_selecionada = st.selectbox("Escolha uma equipe:", lista_nomes_equipes)

    if st.button("Deletar Equipe"):
        try:
            desassociar_jogadores_da_equipe(nome_equipe_selecionada)
            deletar_jogos_da_equipe(nome_equipe_selecionada)
            with st.spinner("Deletando equipe..."):
                collections["equipes"].delete_one({"nome": nome_equipe_selecionada})
            st.success("Equipe e dados associados deletados com sucesso!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao deletar: {e}")


def visualizar_equipe():
    st.subheader("Equipes Cadastradas")
    with st.spinner("Carregando dados..."):
        equipes = list(collections["equipes"].find())

    if equipes:
        dados_tabela = [
            {"Nome da Equipe": equipe.get("nome", "Desconhecida")} for equipe in equipes
        ]
        st.table(dados_tabela)
    else:
        st.info("Nenhuma equipe cadastrada ainda.")
