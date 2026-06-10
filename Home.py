import streamlit as st
import requests
from datetime import datetime

# ====================================
# CONFIGURAÇÃO DA PÁGINA
# ====================================

st.set_page_config(
    page_title="EduTrack AI",
    page_icon="🎓",
    layout="wide"
)

# ====================================
# BLOQUEIO DE ACESSO
# ====================================

if "auth_token" not in st.session_state:
    st.warning("Faça login para acessar o sistema.")
    st.stop()

if st.session_state.auth_token is None:
    st.warning("Faça login para acessar o sistema.")
    st.stop()

# ====================================
# APIs XANO
# ====================================

TASKS_URL = "https://x8ki-letl-twmt.n7.xano.io/api:gwA9KAfL/tasks"

SUBJECTS_URL = "https://x8ki-letl-twmt.n7.xano.io/api:gwA9KAfL/subjects"

headers = {
    "Authorization": f"Bearer {st.session_state.auth_token}"
}

# ====================================
# BUSCAR DISCIPLINAS
# ====================================

disciplinas = []

response_subjects = requests.get(
    SUBJECTS_URL,
    headers=headers
)

if response_subjects.status_code == 200:

    disciplinas = response_subjects.json()
    total_disciplinas = len(disciplinas)

else:

    total_disciplinas = 0

# ====================================
# BUSCAR TAREFAS
# ====================================

tarefas = []

response_tasks = requests.get(
    TASKS_URL,
    headers=headers
)

if response_tasks.status_code == 200:

    tarefas = response_tasks.json()

else:

    tarefas = []

# ====================================
# MÉTRICAS
# ====================================

total_tarefas = len(tarefas)

tarefas_pendentes = len([
    tarefa for tarefa in tarefas
    if tarefa["status"] == "pending"
])

tarefas_concluidas = len([
    tarefa for tarefa in tarefas
    if tarefa["status"] == "completed"
])

hoje = datetime.now().date()

tarefas_atrasadas = len([
    tarefa for tarefa in tarefas
    if tarefa["status"] != "completed"
    and datetime.strptime(
        tarefa["deadline"],
        "%Y-%m-%d"
    ).date() < hoje
])

if total_tarefas > 0:

    percentual_progresso = (
        tarefas_concluidas / total_tarefas
    )

else:

    percentual_progresso = 0

# ====================================
# SIDEBAR
# ====================================

st.sidebar.title("🎓 EduTrack AI")

st.sidebar.markdown("---")

menu_opcao = st.sidebar.radio(
    "Navegação",
    [
        "🏠 Dashboard",
        "📚 Disciplinas",
        "📝 Tarefas",
        "👤 Perfil"
    ]
)

st.sidebar.markdown("---")

if st.sidebar.button("🚪 Sair"):

    st.session_state.auth_token = None
    st.session_state.usuario_id = None

    st.switch_page("pages/0_Login.py")

# ====================================
# NAVEGAÇÃO
# ====================================

if menu_opcao == "📚 Disciplinas":
    st.switch_page("pages/1_Disciplinas.py")

if menu_opcao == "📝 Tarefas":
    st.switch_page("pages/2_Tarefas.py")

if menu_opcao == "👤 Perfil":
    st.switch_page("pages/3_Perfil.py")

# ====================================
# CABEÇALHO
# ====================================

st.title("🎓 EduTrack AI")

st.caption(
    "Sistema acadêmico para gerenciamento de disciplinas e tarefas."
)

st.success(
    "Bem-vindo ao seu painel acadêmico!"
)

# ====================================
# CARDS
# ====================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "📚 Disciplinas",
        total_disciplinas
    )

with col2:

    st.metric(
        "📝 Pendentes",
        tarefas_pendentes
    )

with col3:

    st.metric(
        "⚠️ Em Atraso",
        tarefas_atrasadas
    )

with col4:

    st.metric(
        "✅ Concluídas",
        tarefas_concluidas
    )

# ====================================
# PROGRESSO
# ====================================

st.markdown("## 📈 Progresso Geral")

st.progress(percentual_progresso)

st.write(
    f"{percentual_progresso * 100:.0f}% das tarefas concluídas"
)

# ====================================
# PRÓXIMAS ENTREGAS
# ====================================

st.markdown("## ⏳ Próximas Entregas")

tarefas_ordenadas = sorted(
    tarefas,
    key=lambda x: x["deadline"]
)

proximas_tarefas = [
    tarefa
    for tarefa in tarefas_ordenadas
    if tarefa["status"] != "completed"
][:5]

if proximas_tarefas:

    for tarefa in proximas_tarefas:

        st.info(
            f"""
            **{tarefa['title']}**

            Prazo: {tarefa['deadline']}

            Status: {tarefa['status']}
            """
        )

else:

    st.success(
        "Nenhuma tarefa pendente encontrada."
    )