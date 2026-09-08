import json
import os
import streamlit as st

ARQUIVO_DADOS = "dados.json"


def carregar_dados():
    """Carrega os dados do arquivo JSON ou inicializa a estrutura padrão se o arquivo não existir."""
    if not os.path.exists(ARQUIVO_DADOS):
        dados_iniciais = {"materias": [], "atividades": []}
        salvar_dados(dados_iniciais)
        return dados_iniciais

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            if "materias" not in dados:
                dados["materias"] = []
            if "atividades" not in dados:
                dados["atividades"] = []
            return dados
    except (json.JSONDecodeError, OSError):
        dados_recuperados = {"materias": [], "atividades": []}
        salvar_dados(dados_recuperados)
        return dados_recuperados


def salvar_dados(dados):
    """Salva os dados no arquivo JSON com formatação legível."""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


dados = carregar_dados()

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
    nome_limpo = materia.strip()
    if nome_limpo:
        nova_materia = {
            "nome": nome_limpo,
            "dificuldade": dificuldade,
            "horas_semanais": horas
        }
        dados["materias"].append(nova_materia)
        salvar_dados(dados)
        st.success(
            f"{nome_limpo} adicionada! "
            f"Dificuldade: {dificuldade}/5 | "
            f"Meta: {horas}h/semana"
        )
    else:
        st.warning("Digite o nome da matéria.")

st.divider()
st.subheader("Matérias cadastradas")

if not dados["materias"]:
    st.info("Nenhuma matéria cadastrada ainda.")
else:
    for item in dados["materias"]:
        st.write(
            f"- **{item['nome']}** — "
            f"Dificuldade: {item['dificuldade']}/5 | "
            f"Meta: {item['horas_semanais']}h/semana"
        )
