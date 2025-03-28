import streamlit as st
import datetime
from database.connection import get_db
from database.models import get_collections
from bson import ObjectId

db = get_db()
collections = get_collections(db)

def cadastrar_jogo():
    st.header("Cadastrar Jogo")

    data_jogo = st.date_input("Data do Jogo:", datetime.date.today())
    hora_jogo = st.time_input("Hora do Jogo:", datetime.time(19, 0))
    local_jogo = st.text_input("Local do Jogo:")

    equipes = list(collections["equipes"].find())
    if not equipes:
        st.error("Não há equipes cadastradas. Cadastre equipes primeiro.")
        return

    lista_equipes = [f"{equipe['nome']} (ID: {equipe['_id']})" for equipe in equipes]

    equipe1_selecionada = st.selectbox("Escolha a Equipe 1:", lista_equipes)
    equipe2_selecionada = st.selectbox("Escolha a Equipe 2:", lista_equipes)

    if equipe1_selecionada == equipe2_selecionada:
        st.error("A Equipe 1 e a Equipe 2 não podem ser a mesma.")

    equipe1_id = equipe1_selecionada.split(" (ID: ")[1].strip(")")
    equipe2_id = equipe2_selecionada.split(" (ID: ")[1].strip(")")

    if st.button("Cadastrar Jogo"):
        if equipe1_id != equipe2_id:
            equipe1_id = ObjectId(equipe1_id)
            equipe2_id = ObjectId(equipe2_id)

            if collections["jogos"].find_one({"$or": [{"equipe1_id": equipe1_id, "equipe2_id": equipe2_id},
                                                      {"equipe1_id": equipe2_id, "equipe2_id": equipe1_id}]}):
                st.error("Já existe um jogo registrado entre essas equipes.")
            else:
                jogo = {
                    "data": str(data_jogo),
                    "hora": str(hora_jogo),
                    "local": local_jogo,
                    "equipe1_id": equipe1_id,
                    "equipe2_id": equipe2_id
                }
                collections["jogos"].insert_one(jogo)
                st.success(
                    f"Jogo entre as equipes {equipe1_selecionada} e {equipe2_selecionada} cadastrado com sucesso!")
        else:
            st.error("As equipes não podem ser a mesma para o jogo.")

    # TABELA DE JOGOS
    st.subheader("Jogos Cadastrados")
    jogos = list(collections["jogos"].find())

    if jogos:
        dados_tabela = []
        for jogo in jogos:
            equipe1 = collections["equipes"].find_one({"_id": jogo["equipe1_id"]})
            equipe2 = collections["equipes"].find_one({"_id": jogo["equipe2_id"]})

            equipe1_nome = equipe1["nome"] if equipe1 else "Equipe não encontrada"
            equipe2_nome = equipe2["nome"] if equipe2 else "Equipe não encontrada"

            dados_tabela.append({
                "Data": jogo["data"],
                "Hora": jogo["hora"],
                "Local": jogo["local"],
                "Equipe 1": equipe1_nome,
                "Equipe 2": equipe2_nome
            })

        st.dataframe(dados_tabela)
    else:
        st.info("Nenhum jogo cadastrado ainda.")
