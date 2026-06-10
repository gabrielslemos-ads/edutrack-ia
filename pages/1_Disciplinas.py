import streamlit as st
import requests

# =========================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================

st.set_page_config(
    page_title="Disciplinas",
    page_icon="📚",
    layout="wide"
)

# =========================================
# VALIDA LOGIN
# =========================================

if "auth_token" not in st.session_state:
    st.session_state.auth_token = None

if not st.session_state.auth_token:
    st.warning("Faça login para acessar esta página.")
    st.stop()

# =========================================
# URL API XANO
# =========================================

GET_SUBJECTS_URL = "https://x8ki-letl-twmt.n7.xano.io/api:gwA9KAfL/subjects"

POST_SUBJECTS_URL = "https://x8ki-letl-twmt.n7.xano.io/api:gwA9KAfL/subjects"

# =========================================
# HEADERS AUTH
# =========================================

headers = {
    "Authorization": f"Bearer {st.session_state.auth_token}"
}

# =========================================
# TÍTULO
# =========================================

st.title("📚 Disciplinas")

st.caption("Gerencie suas disciplinas acadêmicas")

# =========================================
# FORMULÁRIO CADASTRO
# =========================================

with st.form("nova_disciplina"):

    nome = st.text_input("Nome da disciplina")

    professor = st.text_input("Professor")

    carga_horaria = st.number_input(
        "Carga Horária",
        min_value=1,
        step=1
    )

    salvar = st.form_submit_button("Cadastrar Disciplina")

    if salvar:

        payload = {
            "name": nome,
            "professor": professor,
            "carga_horaria": carga_horaria
        }

        response = requests.post(
            POST_SUBJECTS_URL,
            json=payload,
            headers=headers
        )

        if response.status_code in [200, 201]:

            st.success("Disciplina cadastrada com sucesso!")

            st.rerun()

        else:

            st.error("Erro ao cadastrar disciplina.")

            st.write(response.text)

# =========================================
# LISTAR DISCIPLINAS
# =========================================

st.divider()

st.subheader("Minhas Disciplinas")

response = requests.get(
    GET_SUBJECTS_URL,
    headers=headers
)

if response.status_code == 200:

    disciplinas = response.json()

    if len(disciplinas) == 0:

        st.info("Nenhuma disciplina cadastrada.")

    else:

        for d in disciplinas:

            with st.container(border=True):

                st.markdown(f"### 📘 {d['name']}")

                st.write(f"👨‍🏫 Professor: {d['professor']}")

                st.write(f"⏰ Carga Horária: {d['carga_horaria']}h")

else:

    st.error("Erro ao carregar disciplinas.")

    st.write(response.text)