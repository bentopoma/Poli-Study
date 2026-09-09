from datetime import datetime
import json
import os
import uuid
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
            for ativ in dados["atividades"]:
                if "id" not in ativ:
                    ativ["id"] = uuid.uuid4().hex[:8]
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
    for idx, item in enumerate(dados["materias"]):
        qtd_vinculadas = sum(
            1 for a in dados["atividades"] if a.get("materia") == item["nome"]
        )
        col_info, col_del = st.columns([5, 1])
        with col_info:
            st.write(
                f"- **{item['nome']}** — "
                f"Dificuldade: {item['dificuldade']}/5 | "
                f"Meta: {item['horas_semanais']}h/semana"
            )
        with col_del:
            if st.button("🗑️ Excluir", key=f"del_mat_{idx}"):
                if qtd_vinculadas == 0:
                    dados["materias"] = [
                        m for m in dados["materias"] if m["nome"] != item["nome"]
                    ]
                    salvar_dados(dados)
                    st.rerun()
                else:
                    st.session_state["confirmar_exclusao_materia"] = item["nome"]
                    st.rerun()

        if st.session_state.get("confirmar_exclusao_materia") == item["nome"]:
            st.warning(
                f"⚠️ Essa matéria possui {qtd_vinculadas} atividade(s) vinculada(s). "
                "Deseja excluir ela mesmo assim?"
            )
            col_conf_sim, col_conf_nao = st.columns([3, 1])
            with col_conf_sim:
                if st.button(
                    "Sim, excluir matéria e atividades",
                    key=f"conf_sim_{idx}",
                    type="primary"
                ):
                    dados["materias"] = [
                        m for m in dados["materias"] if m["nome"] != item["nome"]
                    ]
                    dados["atividades"] = [
                        a for a in dados["atividades"] if a.get("materia") != item["nome"]
                    ]
                    st.session_state.pop("confirmar_exclusao_materia", None)
                    salvar_dados(dados)
                    st.rerun()
            with col_conf_nao:
                if st.button("Cancelar", key=f"conf_nao_{idx}"):
                    st.session_state.pop("confirmar_exclusao_materia", None)
                    st.rerun()

st.divider()
st.subheader("Nova atividade")

if not dados["materias"]:
    st.warning("Cadastre ao menos uma matéria antes de adicionar atividades.")
else:
    nome_atividade = st.text_input("Nome da atividade")
    nomes_materias = [m["nome"] for m in dados["materias"]]
    materia_selecionada = st.selectbox("Matéria associada", options=nomes_materias)
    tipo_selecionado = st.selectbox(
        "Tipo de atividade",
        options=["Prova", "Trabalho", "Tarefa"]
    )
    data_selecionada = st.date_input(
        "Data da atividade",
        format="DD/MM/YYYY"
    )
    importancia_selecionada = st.slider(
        "Importância da atividade",
        min_value=1,
        max_value=5,
        value=3
    )

    if st.button("Adicionar atividade"):
        nome_ativ_limpo = nome_atividade.strip()
        if nome_ativ_limpo:
            nova_atividade = {
                "id": uuid.uuid4().hex[:8],
                "nome": nome_ativ_limpo,
                "materia": materia_selecionada,
                "tipo": tipo_selecionado,
                "data": data_selecionada.strftime("%Y-%m-%d"),
                "importancia": importancia_selecionada
            }
            dados["atividades"].append(nova_atividade)
            salvar_dados(dados)
            st.success(
                f"Atividade '{nome_ativ_limpo}' adicionada! "
                f"Tipo: {tipo_selecionado} | "
                f"Matéria: {materia_selecionada}"
            )
            st.rerun()
        else:
            st.warning("Digite o nome da atividade.")

st.divider()
st.subheader("Atividades cadastradas")

if not dados["atividades"]:
    st.info("Nenhuma atividade cadastrada ainda.")
else:
    for ativ in dados["atividades"]:
        try:
            data_formatada = datetime.strptime(
                ativ["data"], "%Y-%m-%d"
            ).strftime("%d/%m/%Y")
        except (ValueError, TypeError):
            data_formatada = str(ativ.get("data", ""))

        col_ativ_info, col_ativ_del = st.columns([5, 1])
        with col_ativ_info:
            st.write(
                f"- **{ativ['nome']}** ({ativ['tipo']}) — "
                f"Matéria: {ativ['materia']} | "
                f"Data: {data_formatada} | "
                f"Importância: {ativ['importancia']}/5"
            )
        with col_ativ_del:
            if st.button("🗑️ Excluir", key=f"del_ativ_{ativ['id']}"):
                dados["atividades"] = [
                    a for a in dados["atividades"] if a["id"] != ativ["id"]
                ]
                salvar_dados(dados)
                st.rerun()

st.divider()
st.subheader("Limpar semestre")
st.caption(
    "Esta ação apagará permanentemente todas as matérias e atividades cadastradas."
)
confirmar_limpeza = st.checkbox(
    "Tenho certeza de que desejo apagar todas as matérias e atividades."
)
if st.button("Limpar semestre", type="primary", disabled=not confirmar_limpeza):
    dados["materias"] = []
    dados["atividades"] = []
    salvar_dados(dados)
    st.session_state.pop("confirmar_exclusao_materia", None)
    st.success("Todas as matérias e atividades foram apagadas com sucesso!")
    st.rerun()
