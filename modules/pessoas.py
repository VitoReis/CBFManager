import streamlit as st
from database.connection import get_db
from database.models import get_collections
from bson import ObjectId

db = get_db()
collections = get_collections(db)


def cadastrar_pessoa():
    login_pessoa = st.text_input("Login do Usuario:")
    senha_pessoa = st.text_input("Senha do Usuario:", type="password")
    tipo_pessoa = st.selectbox("Tipo de Usuario:", ["Administrador", "Usuario"])

    if st.button("Cadastrar Usuario"):
        pessoa_existente = collections["pessoas"].find_one({"login": login_pessoa})
        if pessoa_existente:
            st.error(f"Já existe um pessoa com o nome {login_pessoa}.")
        else:
            collections["pessoas"].insert_one(
                {
                    "login": login_pessoa,
                    "senha": senha_pessoa,
                    "tipo": (
                        "administrador" if tipo_pessoa == "Administrador" else "usuario"
                    ),
                }
            )
            st.success(f"'{login_pessoa}' foi cadastrado!")


def deletar_pessoa():
    st.subheader("Deletar Usuario")
    pessoas = collections["pessoas"].find()
    if pessoas:
        lista_pessoas = [
            f"{pessoa['login']} - (ID: {pessoa['_id']})" for pessoa in pessoas
        ]

        pessoa_selecionada = st.selectbox("Selecione o pessoa", lista_pessoas)

        if st.button("Deletar Usuario"):
            pessoa_id = pessoa_selecionada.split(" (ID: ")[1].strip(")")
            try:
                collections["pessoas"].delete_one({"_id": ObjectId(pessoa_id)})
                st.success("Usuario deletado com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao deletar: {e}")
    else:
        st.info("Não há usuários cadastrados")
