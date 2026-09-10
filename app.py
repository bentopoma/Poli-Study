from datetime import date, datetime
import json
import os
import uuid
import streamlit as st
from streamlit_calendar import calendar

ARQUIVO_DADOS = "dados.json"
CORES_TIPO = {
    "Prova": "#E53935",
    "Trabalho": "#FB8C00",
    "Tarefa": "#1E88E5",
}


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


def calcular_urgencia(dias):
    """Calcula a pontuação de urgência (1 a 5) com base na quantidade de dias até o prazo."""
    if dias <= 0:
        return 5.0
    elif dias <= 2:
        return 4.5
    elif dias <= 5:
        return 4.0
    elif dias <= 7:
        return 3.0
    elif dias <= 14:
        return 2.0
    else:
        return 1.0


def gerar_explicacao_prioridade(dias, urgencia, importancia, dificuldade):
    """Gera uma explicação concisa dos fatores que contribuíram para a prioridade."""
    if dias < 0:
        desc_prazo = f"prazo vencido há {abs(dias)} dia(s)"
    elif dias == 0:
        desc_prazo = "prazo vence hoje"
    elif dias <= 2:
        desc_prazo = f"prazo muito próximo ({dias} dia(s))"
    elif dias <= 5:
        desc_prazo = f"prazo próximo ({dias} dia(s))"
    elif dias <= 14:
        desc_prazo = f"prazo em {dias} dias"
    else:
        desc_prazo = f"prazo confortável ({dias} dias)"

    return (
        f"{desc_prazo} (urgência {urgencia:g}/5), "
        f"importância {importancia}/5 e "
        f"dificuldade da matéria {dificuldade}/5."
    )


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

st.divider()
st.subheader("🎯 Prioridades de estudo")

if not dados["atividades"]:
    st.info("Nenhuma atividade cadastrada para priorizar.")
else:
    hoje = date.today()
    materias_dificuldade = {
        m["nome"]: m.get("dificuldade", 3) for m in dados["materias"]
    }

    atividades_priorizadas = []
    for ativ in dados["atividades"]:
        try:
            data_obj = datetime.strptime(ativ["data"], "%Y-%m-%d").date()
            dias = (data_obj - hoje).days
        except (ValueError, TypeError):
            dias = 999

        urgencia = calcular_urgencia(dias)
        dificuldade = materias_dificuldade.get(ativ["materia"], 3)
        importancia = ativ.get("importancia", 3)

        prioridade = (
            0.45 * urgencia
            + 0.35 * importancia
            + 0.20 * dificuldade
        )
        explicacao = gerar_explicacao_prioridade(
            dias, urgencia, importancia, dificuldade
        )

        atividades_priorizadas.append({
            "atividade": ativ,
            "dias": dias,
            "prioridade": prioridade,
            "explicacao": explicacao
        })

    # 1. Atividades atrasadas (dias < 0) aparecem no topo, da mais atrasada para a menos atrasada
    atrasadas = [item for item in atividades_priorizadas if item["dias"] < 0]
    atrasadas.sort(key=lambda x: (x["dias"], -x["prioridade"]))

    # 2. Atividades no prazo seguem o ranking por nota de prioridade decrescente
    nao_atrasadas = [item for item in atividades_priorizadas if item["dias"] >= 0]
    nao_atrasadas.sort(key=lambda x: x["prioridade"], reverse=True)

    atividades_priorizadas = atrasadas + nao_atrasadas

    for item_prio in atividades_priorizadas:
        ativ = item_prio["atividade"]
        dias = item_prio["dias"]
        prioridade = item_prio["prioridade"]
        explicacao = item_prio["explicacao"]

        if dias < 0:
            status_prazo = f"Atrasada há {abs(dias)} dia(s)"
            st.error(
                f"🔴 **[ATRASADA] {ativ['nome']}** ({ativ['tipo']})\n\n"
                f"- **Matéria:** {ativ['materia']}\n"
                f"- **Nota de prioridade:** `{prioridade:.2f} / 5.00`\n"
                f"- **Dias até o prazo:** {status_prazo}\n"
                f"- **Fatores:** {explicacao}"
            )
        else:
            if dias == 0:
                status_prazo = "🟠 Vence hoje"
            elif dias == 1:
                status_prazo = "🗓️ Falta 1 dia"
            else:
                status_prazo = f"🗓️ Faltam {dias} dias"

            st.markdown(
                f"- **{ativ['nome']}** ({ativ['tipo']})\n"
                f"  - **Matéria:** {ativ['materia']}\n"
                f"  - **Nota de prioridade:** `{prioridade:.2f} / 5.00`\n"
                f"  - **Dias até o prazo:** {status_prazo}\n"
                f"  - **Fatores:** {explicacao}"
            )

st.divider()
st.subheader("📅 Calendário acadêmico")

if not dados["atividades"]:
    st.info("Nenhuma atividade cadastrada para exibir no calendário.")
else:
    eventos_calendario = []
    for ativ in dados["atividades"]:
        cor = CORES_TIPO.get(ativ.get("tipo"), "#3788D8")
        eventos_calendario.append({
            "title": f"[{ativ['tipo']}] {ativ['nome']} ({ativ['materia']})",
            "start": ativ["data"],
            "end": ativ["data"],
            "allDay": True,
            "backgroundColor": cor,
            "borderColor": cor,
        })

    opcoes_calendario = {
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,dayGridWeek",
        },
        "initialView": "dayGridMonth",
        "editable": False,
        "selectable": False,
        "locale": "pt-br",
    }

    calendar(
        events=eventos_calendario,
        options=opcoes_calendario,
        key="calendario_academico",
    )

st.divider()
with st.expander("➕ Adicionar atividade"):
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
with st.expander("➕ Adicionar matéria"):
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
            st.rerun()
        else:
            st.warning("Digite o nome da matéria.")

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
st.subheader("Gerenciamento do semestre")
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
