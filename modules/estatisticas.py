import streamlit as st
from database.connection import get_db
from database.models import get_collections
from bson import ObjectId

db = get_db()
collections = get_collections(db)

def registrar_estatisticas():
    st.header("Registrar Estatística de Jogador")

    jogadores = list(collections["jogadores"].find())
    jogos = list(collections["jogos"].find())

    if not jogadores:
        st.error("Não há jogadores cadastrados. Cadastre jogadores primeiro.")
        return

    if not jogos:
        st.error("Não há jogos cadastrados. Cadastre jogos primeiro.")
        return

    lista_jogadores = [f"{jogador['nome']} (ID: {jogador['_id']})" for jogador in jogadores]
    lista_jogos = [f"{jogo['data']} - {jogo['local']} (ID: {jogo['_id']})" for jogo in jogos]

    jogador_selecionado = st.selectbox("Escolha o Jogador:", lista_jogadores)
    jogo_selecionado = st.selectbox("Escolha o Jogo:", lista_jogos)

    jogador_id = jogador_selecionado.split(" (ID: ")[1].strip(")")
    jogo_id = jogo_selecionado.split(" (ID: ")[1].strip(")")

    jogador_id = ObjectId(jogador_id)
    jogo_id = ObjectId(jogo_id)

    gols = st.number_input("Gols Marcados:", min_value=0, step=1)
    cartoes = st.number_input("Cartões Recebidos:", min_value=0, step=1)

    if st.button("Registrar Estatística"):
        estatistica = {
            "jogo_id": jogo_id,
            "jogador_id": jogador_id,
            "gols": gols,
            "cartoes": cartoes
        }
        collections["estatisticas"].insert_one(estatistica)
        st.success("Estatística registrada com sucesso!")

    # TABELA DE ESTATISTICAS
    st.subheader("Estatísticas Registradas")
    estatisticas = list(collections["estatisticas"].find())

    if estatisticas:
        dados_tabela = []
        for estatistica in estatisticas:
            jogador = collections["jogadores"].find_one({"_id": estatistica["jogador_id"]})
            jogo = collections["jogos"].find_one({"_id": estatistica["jogo_id"]})

            jogador_nome = jogador["nome"] if jogador else "Jogador não encontrado"
            jogo_data = jogo["data"] if jogo else "Data não encontrada"
            jogo_local = jogo["local"] if jogo else "Local não encontrado"

            dados_tabela.append({
                "Jogador": jogador_nome,
                "Jogo": f"{jogo_data} - {jogo_local}",
                "Gols": estatistica["gols"],
                "Cartões": estatistica["cartoes"]
            })

        st.dataframe(dados_tabela)
    else:
        st.info("Nenhuma estatística registrada ainda.")
