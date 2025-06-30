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

    lista_equipes = ["Nenhuma"] + [equipe["nome"] for equipe in equipes]
    equipe_selecionada = st.selectbox("Equipe:", lista_equipes)

    numero_jogador = st.number_input("Número do Jogador:", min_value=1, step=1)

    if st.button("Cadastrar Jogador"):
        nome_equipe = None if equipe_selecionada == "Nenhuma" else equipe_selecionada

        with st.spinner("Verificando jogador existente..."):
            filtro = {
                "nome": nome_jogador,
                "numero": numero_jogador,
                "nome_equipe": nome_equipe,
            }
            jogador_existente = collections["jogadores"].find_one(filtro)

        if jogador_existente:
            msg = f"Já existe um jogador com o número {numero_jogador}"
            msg += f" na equipe '{nome_equipe}'." if nome_equipe else " sem equipe."
            st.error(msg)
        else:
            with st.spinner("Cadastrando jogador..."):
                doc = {
                    "nome": nome_jogador,
                    "numero": numero_jogador,
                    "nome_equipe": nome_equipe,
                }
                collections["jogadores"].insert_one(doc)

            st.success(f"Jogador '{nome_jogador}' cadastrado com sucesso!")


def deletar_jogador():
    st.header("Deletar Jogador")

    with st.spinner("Carregando jogadores..."):
        jogadores = list(collections["jogadores"].find())

    if not jogadores:
        st.info("Nenhum jogador cadastrado ainda.")
        return

    lista_jogadores = [
        f"{j['nome']} | Nº {j['numero']} | {j.get('nome_equipe', 'Nenhuma')} (ID: {j['_id']})"
        for j in jogadores
    ]

    jogador_selecionado = st.selectbox(
        "Escolha um jogador para deletar:", lista_jogadores
    )

    if st.button("Deletar"):
        jogador_id_str = jogador_selecionado.split("(ID: ")[1].strip(")")
        jogador_id = ObjectId(jogador_id_str)

        try:
            with st.spinner("Deletando jogador e estatísticas relacionadas..."):
                # CASCADE ESTATISTICA
                collections["estatisticas"].delete_many({"jogador_id": jogador_id})

                collections["jogadores"].delete_one({"_id": jogador_id})

            st.success("Jogador e estatísticas relacionadas deletados com sucesso!")
            st.rerun()

        except Exception as e:
            st.error(f"Erro ao deletar: {e}")


def visualizar_jogador():
    st.subheader("Jogadores Cadastrados")

    with st.spinner("Carregando jogadores..."):
        jogadores = list(collections["jogadores"].find())

    if jogadores:
        dados_tabela = []
        for j in jogadores:
            nome_equipe = j.get("nome_equipe")
            if not nome_equipe:
                nome_equipe = "Nenhuma"

            dados_tabela.append(
                {
                    "Nome": j["nome"],
                    "Número": j["numero"],
                    "Equipe": nome_equipe,
                    "ID": str(j["_id"]),
                }
            )

        st.table(dados_tabela)
    else:
        st.info("Nenhum jogador cadastrado ainda.")


def editar_jogador():
    st.header("Editar Jogador")

    with st.spinner("Carregando jogadores..."):
        jogadores = list(collections["jogadores"].find())

    if not jogadores:
        st.info("Nenhum jogador cadastrado ainda.")
        return

    opcoes = [
        {
            "label": f"{j['nome']} | Nº {j['numero']} | {j.get('nome_equipe', 'Nenhuma')}",
            "id": j["_id"],
            "nome": j["nome"],
            "numero": j["numero"],
            "nome_equipe": j.get("nome_equipe", "Nenhuma"),
        }
        for j in jogadores
    ]

    labels = [j["label"] for j in opcoes]
    escolha = st.selectbox("Selecione o jogador para editar:", labels)
    selecionado = next(j for j in opcoes if j["label"] == escolha)

    nome = st.text_input("Nome do Jogador:", value=selecionado["nome"])
    numero = st.number_input(
        "Número do Jogador:", min_value=1, value=selecionado["numero"], step=1
    )

    with st.spinner("Carregando equipes..."):
        equipes = list(collections["equipes"].find())

    lista_equipes = ["Nenhuma"] + [e["nome"] for e in equipes]
    equipe = st.selectbox(
        "Equipe:", lista_equipes, index=lista_equipes.index(selecionado["nome_equipe"])
    )

    nome_equipe = None if equipe == "Nenhuma" else equipe

    if st.button("Salvar Alterações"):
        with st.spinner("Atualizando jogador..."):
            collections["jogadores"].update_one(
                {"_id": selecionado["id"]},
                {"$set": {"nome": nome, "numero": numero, "nome_equipe": nome_equipe}},
            )
        st.success("Jogador atualizado com sucesso!")
