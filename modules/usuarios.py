import streamlit as st
from database.connection import get_db
from database.models import get_collections
from bson import ObjectId

db = get_db()
collections = get_collections(db)


def cadastrar_usuario():
    login_usuario = st.text_input("Login do Usuario:")
    senha_usuario = st.text_input("Senha do Usuario:", type="password")
    tipo_usuario = st.selectbox("Tipo de Usuario:", ["Administrador", "Usuario"])

    if st.button("Cadastrar Equipe"):
        usuario_existente = collections["usuarios"].find_one({"login": login_usuario})
        if usuario_existente:
            st.error(f"Já existe um usuario com o nome {login_usuario}.")
        else:
            collections["usuarios"].insert_one(
                {
                    "login": login_usuario,
                    "senha": senha_usuario,
                    "tipo": "admin" if tipo_usuario == "Administrador" else "usuario",
                }
            )
            st.success(f"Usuario '{login_usuario}' cadastrado!")


def deletar_usuario():
    st.subheader("Deletar Usuario")
    usuarios = collections["usuarios"].find()
    if usuarios:
        lista_usuarios = [
            f"{usuario['login']} - (ID: {usuario['_id']})" for usuario in usuarios
        ]

        usuario_selecionado = st.selectbox("Selecione o usuario", lista_usuarios)

        if st.button("Deletar Usuario"):
            usuario_id = usuario_selecionado.split(" (ID: ")[1].strip(")")
            try:
                collections["usuarios"].delete_one({"_id": ObjectId(usuario_id)})
                st.success("Usuario deletado com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao deletar: {e}")
    else:
        st.info("Não há usuários cadastrados")
