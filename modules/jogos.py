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


def editar_jogo():
    st.header("Editar Jogo")
    st.subheader(
        "Editar um jogo irá deletar todas as estatísticas relacionadas ao mesmo"
    )

    with st.spinner("Carregando jogos..."):
        jogos = list(collections["jogos"].find())

    if not jogos:
        st.info("Nenhum jogo cadastrado ainda.")
        return

    opcoes = [
        {
            "label": f"{j['data']} {j['hora']} - {j['local']} | {j['nome_equipe1']} vs {j['nome_equipe2']}",
            "id": j["_id"],
            "data": j["data"],
            "hora": j["hora"],
            "local": j["local"],
            "equipe1": j["nome_equipe1"],
            "equipe2": j["nome_equipe2"],
        }
        for j in jogos
    ]

    labels = [j["label"] for j in opcoes]
    escolha = st.selectbox("Selecione o jogo para editar:", labels)
    selecionado = next(j for j in opcoes if j["label"] == escolha)

    try:
        hora_formatada = datetime.datetime.strptime(
            selecionado["hora"], "%H:%M:%S"
        ).time()
    except ValueError:
        hora_formatada = datetime.datetime.strptime(selecionado["hora"], "%H:%M").time()

    data_jogo = st.date_input(
        "Data do Jogo:",
        datetime.datetime.strptime(selecionado["data"], "%Y-%m-%d").date(),
    )
    hora_jogo = st.time_input("Hora do Jogo:", hora_formatada)
    local_jogo = st.text_input("Local do Jogo:", value=selecionado["local"])

    with st.spinner("Carregando equipes..."):
        equipes = list(collections["equipes"].find())
    nomes_equipes = [e["nome"] for e in equipes]

    equipe1 = st.selectbox(
        "Equipe 1:", nomes_equipes, index=nomes_equipes.index(selecionado["equipe1"])
    )
    equipe2 = st.selectbox(
        "Equipe 2:", nomes_equipes, index=nomes_equipes.index(selecionado["equipe2"])
    )

    if equipe1 == equipe2:
        st.error("A Equipe 1 e a Equipe 2 não podem ser a mesma.")
        return

    if st.button("Salvar Alterações"):
        with st.spinner("Atualizando jogo..."):
            # CASCADE
            collections["estatisticas"].delete_many({"jogo_id": selecionado["id"]})

            collections["jogos"].update_one(
                {"_id": selecionado["id"]},
                {
                    "$set": {
                        "data": str(data_jogo),
                        "hora": str(hora_jogo),
                        "local": local_jogo,
                        "nome_equipe1": equipe1,
                        "nome_equipe2": equipe2,
                    }
                },
            )
        st.success("Jogo atualizado e estatísticas relacionadas deletadas com sucesso!")
