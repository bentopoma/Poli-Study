import streamlit as st

st.set_page_config(
    page_title="PoliStudy",
    page_icon="📚"
)

st.title("📚 PoliStudy")

st.write(
    "Uma plataforma pessoal para organizar "
    "minhas matérias, provas e estudos."
)

st.subheader("Minhas matérias")

materia = st.text_input("Nome da matéria")

dificuldade = st.slider(
    "Dificuldade da matéria",
    min_value=1,
    max_value=5,
    value=3
)

horas = st.number_input(
    "Meta de horas de estudo por semana",
    min_value=0.0,
    step=0.5
)

if st.button("Adicionar matéria"):
    if materia:
        st.success(
            f"{materia} adicionada! "
            f"Dificuldade: {dificuldade}/5 | "
            f"Meta: {horas}h/semana"
        )
    else:
        st.warning("Digite o nome da matéria.")