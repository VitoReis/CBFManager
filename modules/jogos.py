import streamlit as st
import datetime
from database.connection import get_db
from database.models import get_collections
from bson import ObjectId

with st.spinner("Conectando ao banco de dados..."):
    db = get_db()
    collections = get_collections(db)


def cadastrar_jogo():
    st.header("Cadastrar Jogo")

    data_jogo = st.date_input("Data do Jogo:", datetime.date.today())
    hora_jogo = st.time_input("Hora do Jogo:", datetime.time(19, 0))
    local_jogo = st.text_input("Local do Jogo:")

    with st.spinner("Carregando equipes..."):
        equipes = list(collections["equipes"].find())

    if not equipes:
        st.error("Não há equipes cadastradas. Cadastre equipes primeiro.")
        return

    lista_equipes = [equipe["nome"] for equipe in equipes]

    nome_equipe1 = st.selectbox("Escolha a Equipe 1:", lista_equipes)
    nome_equipe2 = st.selectbox("Escolha a Equipe 2:", lista_equipes)

    if nome_equipe1 == nome_equipe2:
        st.error("A Equipe 1 e a Equipe 2 não podem ser a mesma.")
        return

    if st.button("Cadastrar Jogo"):
        with st.spinner("Verificando se o jogo já existe..."):
            jogo_existente = collections["jogos"].find_one(
                {
                    "$or": [
                        {"nome_equipe1": nome_equipe1, "nome_equipe2": nome_equipe2},
                        {"nome_equipe1": nome_equipe2, "nome_equipe2": nome_equipe1},
                    ],
                    "data": str(data_jogo),
                    "hora": str(hora_jogo),
                }
            )
        if jogo_existente:
            st.error(
                "Já existe um jogo registrado entre essas equipes nessa data e hora."
            )
        else:
            jogo = {
                "data": str(data_jogo),
                "hora": str(hora_jogo),
                "local": local_jogo,
                "nome_equipe1": nome_equipe1,
                "nome_equipe2": nome_equipe2,
            }
            with st.spinner("Cadastrando jogo..."):
                collections["jogos"].insert_one(jogo)
            st.success(
                f"Jogo entre {nome_equipe1} e {nome_equipe2} cadastrado com sucesso!"
            )


def deletar_jogo():
    st.header("Deletar Jogo")

    with st.spinner("Carregando jogos..."):
        jogos = list(collections["jogos"].find())

    if not jogos:
        st.info("Nenhum jogo cadastrado ainda.")
        return

    opcoes_jogos = [
        f"{j['data']} {j['hora']} - {j['local']} | {j.get('nome_equipe1', 'Desconhecida')} vs {j.get('nome_equipe2', 'Desconhecida')} (ID: {j['_id']})"
        for j in jogos
    ]

    jogo_selecionado = st.selectbox("Escolha o jogo para deletar:", opcoes_jogos)

    if st.button("Deletar"):
        jogo_id_str = jogo_selecionado.split("(ID: ")[1].strip(")")
        jogo_id = ObjectId(jogo_id_str)

        try:
            with st.spinner("Deletando jogo e estatísticas associadas..."):
                # CASCADE ESTATISTICA
                collections["estatisticas"].delete_many({"jogo_id": jogo_id})

                collections["jogos"].delete_one({"_id": jogo_id})

            st.success("Jogo e suas estatísticas associadas deletados com sucesso!")
            st.rerun()

        except Exception as e:
            st.error(f"Erro ao deletar o jogo: {e}")


def visualizar_jogo():
    st.subheader("Jogos Cadastrados")

    with st.spinner("Carregando jogos..."):
        jogos = list(collections["jogos"].find())

    if jogos:
        dados_tabela = [
            {
                "Data": jogo["data"],
                "Hora": jogo["hora"],
                "Local": jogo["local"],
                "Equipe 1": jogo.get("nome_equipe1", "Desconhecida"),
                "Equipe 2": jogo.get("nome_equipe2", "Desconhecida"),
            }
            for jogo in jogos
        ]

        st.table(dados_tabela)
    else:
        st.info("Nenhum jogo cadastrado ainda.")
