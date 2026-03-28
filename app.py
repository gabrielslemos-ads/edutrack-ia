import streamlit as st

# Configuração da Página (Título na aba do navegador)
st.set_page_config(page_title="EduTrack AI", page_icon="🎓")

# Título Principal
st.title("🎓 EduTrack AI")

# Sidebar (Menu Lateral)
st.sidebar.header("Menu")
menu_option = st.sidebar.radio("Navegar", ["Dashboard", "Disciplinas", "Tarefas"])

# Conteúdo Dinâmico
if menu_option == "Dashboard":
    st.write("Bem-vindo ao seu assistente acadêmico!")
    st.info("Conecte ao Xano para ver seus dados reais.")
    
    # Exemplo de Métrica Visual
    col1, col2 = st.columns(2)
    col1.metric("Disciplinas Ativas", "0")
    col2.metric("Tarefas Pendentes", "0")

elif menu_option == "Disciplinas":
    st.subheader("Minhas Disciplinas")

    # Adicionar nova disciplina
    with st.form("new_subject_form", clear_on_submit=True):
        st.write("Adicionar nova disciplina")
        subject_name = st.text_input("Nome da Disciplina")
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            from services.xano import add_subject
            result = add_subject(subject_name)
            if "error" in result:
                st.error(result["error"])
            else:
                st.success(f"Disciplina '{subject_name}' adicionada!")

    # Listar disciplinas
    from services.xano import get_subjects
    subjects = get_subjects()
    if "error" in subjects:
        st.error(subjects["error"])
    elif subjects:
        for subject in subjects:
            st.write(subject.get("name", "Nome não disponível"))
    else:
        st.write("Nenhuma disciplina encontrada.")

elif menu_option == "Tarefas":
    st.subheader("Gerenciamento de Tarefas")
    st.checkbox("Exemplo: Estudar Streamlit")