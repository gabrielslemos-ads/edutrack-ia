import streamlit as st
import requests

# ====================================
# CONFIG
# ====================================

ME_URL = "https://x8ki-letl-twmt.n7.xano.io/api:CbFADjgb/auth/me"

st.set_page_config(
    page_title="Perfil",
    page_icon="👤",
    layout="centered"
)

# =========================================
# VALIDA LOGIN
# =========================================

if "auth_token" not in st.session_state:
    st.session_state.auth_token = None

if not st.session_state.auth_token:
    st.warning("Faça login para acessar esta página.")
    st.stop()

# ====================================
# HEADER TOKEN
# ====================================

headers = {
    "Authorization": f"Bearer {st.session_state.auth_token}"
}

# ====================================
# REQUEST
# ====================================

response = requests.get(
    ME_URL,
    headers=headers
)

# ====================================
# TELA
# ====================================

st.title("👤 Perfil")

if response.status_code == 200:

    dados = response.json()

    st.success("Usuário autenticado!")

    st.subheader("Informações do Usuário")

    st.write(f"Nome: {dados.get('name')}")
    st.write(f"Email: {dados.get('email')}")
    st.write(f"ID: {dados.get('id')}")

else:

    st.error("Erro ao carregar perfil.")