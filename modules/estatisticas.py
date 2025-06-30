import streamlit as st
from database.connection import get_db
from database.models import get_collections
from bson import ObjectId

with st.spinner("Conectando ao banco de dados..."):
    db = get_db()
    collections = get_collections(db)


def cadastrar_estatisticas():
    st.header("Cadastrar Estatística de Jogador")

    with st.spinner("Carregando jogadores e jogos..."):
        jogadores = list(collections["jogadores"].find())
        jogos = list(collections["jogos"].find())

    if not jogadores:
        st.error("Não há jogadores cadastrados. Cadastre jogadores primeiro.")
        return

    if not jogos:
        st.error("Não há jogos cadastrados. Cadastre jogos primeiro.")
        return

    lista_jogadores = [
        f"{jogador['nome']} (ID: {jogador['_id']})" for jogador in jogadores
    ]
    lista_jogos = [
        f"{jogo['data']} - {jogo['local']} (ID: {jogo['_id']})" for jogo in jogos
    ]

    jogador_selecionado = st.selectbox("Escolha o Jogador:", lista_jogadores)
    jogo_selecionado = st.selectbox("Escolha o Jogo:", lista_jogos)

    jogador_id = ObjectId(jogador_selecionado.split(" (ID: ")[1].strip(")"))
    jogo_id = ObjectId(jogo_selecionado.split(" (ID: ")[1].strip(")"))

    gols = st.number_input("Gols Marcados:", min_value=0, step=1)
    cartoes = st.number_input("Cartões Recebidos:", min_value=0, step=1)

    if st.button("Cadastrar"):
        filtro = {"jogador_id": jogador_id, "jogo_id": jogo_id}
        with st.spinner("Verificando estatística existente..."):
            estat_existente = collections["estatisticas"].find_one(filtro)

        if estat_existente:
            novo_gols = estat_existente["gols"] + gols
            novo_cartoes = estat_existente["cartoes"] + cartoes

            with st.spinner("Atualizando estatística..."):
                collections["estatisticas"].update_one(
                    filtro,
                    {"$set": {"gols": novo_gols, "cartoes": novo_cartoes}},
                )
            st.success("Estatística atualizada com sucesso!")
        else:
            nova_estatistica = {
                "jogo_id": jogo_id,
                "jogador_id": jogador_id,
                "gols": gols,
                "cartoes": cartoes,
            }
            with st.spinner("Cadastrando nova estatística..."):
                collections["estatisticas"].insert_one(nova_estatistica)
            st.success("Estatística cadastrada com sucesso!")


def deletar_estatisticas():
    st.header("Deletar Estatística de Jogador")

    with st.spinner("Carregando estatísticas..."):
        estatisticas = list(collections["estatisticas"].find())

    if not estatisticas:
        st.info("Nenhuma estatística registrada ainda.")
        return

    opcoes = []
    for estat in estatisticas:
        with st.spinner("Buscando informações..."):
            jogador = collections["jogadores"].find_one({"_id": estat["jogador_id"]})
            jogo = collections["jogos"].find_one({"_id": estat["jogo_id"]})

        jogador_nome = jogador["nome"] if jogador else "Desconhecido"
        jogo_data = jogo["data"] if jogo else "Data?"
        jogo_local = jogo["local"] if jogo else "Local?"

        opcoes.append(
            {
                "label": f"{jogador_nome} - {jogo_data} em {jogo_local} "
                f"(Gols: {estat['gols']}, Cartões: {estat['cartoes']})",
                "id": estat["_id"],
            }
        )

    opcoes_labels = [op["label"] for op in opcoes]
    escolha = st.selectbox("Escolha uma estatística para deletar:", opcoes_labels)

    if st.button("Deletar"):
        selecionado = next(op for op in opcoes if op["label"] == escolha)
        with st.spinner("Deletando estatística..."):
            collections["estatisticas"].delete_one({"_id": selecionado["id"]})
        st.success("Estatística deletada com sucesso!")
        st.rerun()


def visualizar_estatisticas():
    st.subheader("Estatísticas Registradas")

    with st.spinner("Carregando estatísticas..."):
        estatisticas = list(collections["estatisticas"].find())

    if estatisticas:
        dados_tabela = []
        for estatistica in estatisticas:
            with st.spinner("Buscando informações de jogador e jogo..."):
                jogador = collections["jogadores"].find_one(
                    {"_id": estatistica["jogador_id"]}
                )
                jogo = collections["jogos"].find_one({"_id": estatistica["jogo_id"]})

            jogador_nome = jogador["nome"] if jogador else "Jogador não encontrado"
            jogo_data = jogo["data"] if jogo else "Data não encontrada"
            jogo_local = jogo["local"] if jogo else "Local não encontrado"

            dados_tabela.append(
                {
                    "Jogador": jogador_nome,
                    "Jogo": f"{jogo_data} - {jogo_local}",
                    "Gols": estatistica["gols"],
                    "Cartões": estatistica["cartoes"],
                }
            )

        st.table(dados_tabela)
    else:
        st.info("Nenhuma estatística registrada ainda.")


def editar_estatisticas():
    st.header("Editar Estatística de Jogador")

    with st.spinner("Carregando estatísticas..."):
        estatisticas = list(collections["estatisticas"].find())

    if not estatisticas:
        st.info("Nenhuma estatística registrada ainda.")
        return

    opcoes = []
    for estat in estatisticas:
        jogador = collections["jogadores"].find_one({"_id": estat["jogador_id"]})
        jogo = collections["jogos"].find_one({"_id": estat["jogo_id"]})

        jogador_nome = jogador["nome"] if jogador else "Desconhecido"
        jogo_info = f"{jogo['data']} - {jogo['local']}" if jogo else "Jogo desconhecido"

        opcoes.append(
            {
                "label": f"{jogador_nome} - {jogo_info}",
                "id": estat["_id"],
                "gols": estat["gols"],
                "cartoes": estat["cartoes"],
            }
        )

    labels = [op["label"] for op in opcoes]
    escolha = st.selectbox("Escolha a estatística para editar:", labels)
    selecionado = next(op for op in opcoes if op["label"] == escolha)

    gols = st.number_input(
        "Gols Marcados:", min_value=0, value=selecionado["gols"], step=1
    )
    cartoes = st.number_input(
        "Cartões Recebidos:", min_value=0, value=selecionado["cartoes"], step=1
    )

    if st.button("Salvar Alterações"):
        with st.spinner("Atualizando estatística..."):
            collections["estatisticas"].update_one(
                {"_id": selecionado["id"]},
                {"$set": {"gols": gols, "cartoes": cartoes}},
            )
        st.success("Estatística atualizada com sucesso!")
