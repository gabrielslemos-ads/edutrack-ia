import streamlit as st
import requests
from datetime import datetime

# =========================================
# VALIDA LOGIN
# =========================================

if "auth_token" not in st.session_state:
    st.session_state.auth_token = None

if not st.session_state.auth_token:
    st.warning("Faça login para acessar as tarefas.")
    st.stop()

# =========================================
# CONFIG API
# =========================================

TASKS_URL = "https://x8ki-letl-twmt.n7.xano.io/api:gwA9KAfL/tasks"

headers = {
    "Authorization": f"Bearer {st.session_state.auth_token}"
}

# =========================================
# PÁGINA
# =========================================

st.set_page_config(
    page_title="Tarefas",
    page_icon="📝"
)

st.title("📝 Minhas Tarefas")

# =========================================
# NOVA TAREFA
# =========================================

st.subheader("Cadastrar Nova Tarefa")

with st.form("nova_tarefa"):

    title = st.text_input("Título")
    description = st.text_area("Descrição")
    deadline = st.date_input("Prazo")

    status = st.selectbox(
        "Status",
        [
            "pending",
            "in_progress",
            "completed"
        ]
    )

    subject_id = st.number_input(
        "ID da Disciplina",
        min_value=1,
        step=1
    )

    submit = st.form_submit_button("Cadastrar Tarefa")

    if submit:

        payload = {
            "title": title,
            "description": description,
            "deadline": str(deadline),
            "status": status,
            "subject_id": subject_id
        }

        response = requests.post(
            TASKS_URL,
            headers=headers,
            json=payload
        )

        if response.status_code in [200, 201]:

            st.success("Tarefa cadastrada com sucesso!")
            st.rerun()

        else:

            st.error("Erro ao cadastrar tarefa.")
            st.write(response.text)

# =========================================
# LISTAR TAREFAS
# =========================================

st.divider()

st.subheader("Lista de Tarefas")

response = requests.get(
    TASKS_URL,
    headers=headers
)

if response.status_code == 200:

    tarefas = response.json()

    if len(tarefas) == 0:

        st.info("Nenhuma tarefa cadastrada.")

    else:

        for tarefa in tarefas:

            prazo = datetime.strptime(
                tarefa["deadline"],
                "%Y-%m-%d"
            ).date()

            vencida = (
                prazo < datetime.today().date()
                and tarefa["status"] != "completed"
            )

            titulo = tarefa["title"]

            if vencida:
                titulo = f"🔴 {titulo}"

            with st.expander(f"📌 {titulo}"):

                st.write(f"**Descrição:** {tarefa['description']}")
                st.write(f"**Prazo:** {tarefa['deadline']}")
                st.write(f"**Status:** {tarefa['status']}")
                st.write(f"**Disciplina ID:** {tarefa['subject_id']}")

                # =====================================
                # MARCAR COMO CONCLUÍDA
                # =====================================

                if tarefa["status"] != "completed":

                    if st.button(
                        f"Concluir #{tarefa['id']}"
                    ):

                        update_url = f"{TASKS_URL}/{tarefa['id']}"

                        payload = {
                            "status": "completed"
                        }

                        response_update = requests.patch(
                            update_url,
                            headers=headers,
                            json=payload
                        )

                        if response_update.status_code == 200:

                            st.success("Tarefa concluída!")
                            st.rerun()

                        else:

                            st.error("Erro ao concluir tarefa.")

                # =====================================
                # EXCLUIR
                # =====================================

                if st.button(
                    f"Excluir #{tarefa['id']}"
                ):

                    delete_url = f"{TASKS_URL}/{tarefa['id']}"

                    response_delete = requests.delete(
                        delete_url,
                        headers=headers
                    )

                    if response_delete.status_code == 200:

                        st.success("Tarefa excluída!")
                        st.rerun()

                    else:

                        st.error("Erro ao excluir tarefa.")

else:

    st.error("Erro ao carregar tarefas.")
    st.write(response.text)