
import streamlit as st

# LISTAR DISCIPLINAS
from services.xano import get_subjects

subjects = get_subjects()

# TRATAMENTO DE ERRO
if isinstance(subjects, dict) and "error" in subjects:

    st.error(subjects["error"])

# SE EXISTIREM DISCIPLINAS
elif subjects:

    st.subheader("Lista de Disciplinas")

    st.dataframe(
        subjects,
        use_container_width=True
    )

# SE NÃO EXISTIR NADA
else:

    st.write("Nenhuma disciplina encontrada.")