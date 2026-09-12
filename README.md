# 📚 PoliStudy

O **PoliStudy** é uma plataforma pessoal de organização de estudos desenvolvida em Python com Streamlit para o Processo Seletivo 2026.2 do Poli AI Club.

A aplicação foi pensada para ajudar estudantes a organizar matérias e atividades, visualizar prazos, definir prioridades e planejar melhor o tempo de estudo ao longo do semestre.

## Funcionalidades

### 📊 Visão rápida
Exibe métricas gerais no topo da plataforma:
- atividades pendentes;
- provas nos próximos 7 dias;
- atividades atrasadas;
- atividades concluídas.

### 🎯 Priorização automática
As atividades pendentes são ordenadas automaticamente de acordo com:
- urgência do prazo;
- importância informada pelo usuário;
- dificuldade da matéria.

A pontuação segue a fórmula:

`Prioridade = 0,45 × urgência + 0,35 × importância + 0,20 × dificuldade`

Atividades atrasadas recebem destaque e aparecem antes das demais.

### 🧮 Simulador de notas
Permite simular a nota final de uma disciplina considerando:
- quantidade variável de avaliações;
- provas, trabalhos, atividades ou outros tipos de avaliação;
- pesos diferentes para cada avaliação;
- notas já conhecidas;
- nota final desejada.

O cálculo utiliza **média ponderada**, portanto não depende de média aritmética simples e os pesos não precisam somar 100.

A plataforma também calcula a média necessária nas avaliações restantes para atingir a nota final desejada.

### ⏱️ Plano sugerido de estudos
O usuário informa quantas horas possui disponíveis no dia e quantas atividades deseja incluir no foco.

O PoliStudy distribui o tempo disponível proporcionalmente à prioridade das atividades pendentes, gerando uma sugestão de planejamento diário.

### 📌 Esta semana
Mostra as atividades pendentes com prazo nos próximos 7 dias, organizadas cronologicamente.

### 📅 Calendário acadêmico
Apresenta provas, trabalhos e tarefas em um calendário com visualização mensal e semanal.

As atividades concluídas continuam visíveis no calendário para manter o histórico, mas aparecem com diferenciação visual.

### 📝 Gerenciamento de atividades
É possível:
- cadastrar provas, trabalhos e tarefas;
- definir matéria, data e importância;
- editar atividades;
- excluir atividades individualmente;
- marcar atividades como concluídas ou reabri-las;
- filtrar por tipo, status e matéria.

### 📚 Gerenciamento de matérias
É possível:
- cadastrar matérias;
- definir dificuldade e meta semanal de horas de estudo;
- editar matérias;
- excluir matérias individualmente.

Ao renomear uma matéria, as atividades relacionadas são atualizadas para preservar o vínculo entre os dados.

### ⚙️ Gerenciamento do semestre
A opção **Limpar semestre** permite apagar todas as matérias e atividades, mediante confirmação do usuário.

## Armazenamento dos dados

Os dados são armazenados localmente no arquivo `dados.json`.

A aplicação cria e atualiza esse arquivo automaticamente. Cada matéria e atividade possui um identificador único para permitir edição e exclusão de registros sem duplicação.

## Dados de demonstração

O projeto é disponibilizado com alguns dados fictícios para facilitar a visualização das funcionalidades. Caso deseje testar a plataforma do zero, utilize a opção **"Limpar semestre"** ao final da página.

## Tecnologias utilizadas

- Python
- Streamlit
- streamlit-calendar
- JSON
- Git e GitHub
- Google Antigravity como ferramenta de apoio ao desenvolvimento

O projeto também possui uma **Skill específica para o Antigravity**, localizada em `.agents/skills/polistudy/SKILL.md`, com instruções para manter consistência nas alterações realizadas pelo agente.

## Como executar

### 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
cd polistudy
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
```

No Windows, pelo Prompt de Comando:

```bash
.venv\Scripts\activate.bat
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
python -m streamlit run app.py
```

O Streamlit abrirá a aplicação no navegador, normalmente em `http://localhost:8501`.

## Estrutura principal

```text
polistudy/
├── .agents/
│   └── skills/
│       └── polistudy/
│           └── SKILL.md
├── app.py
├── dados.json
├── requirements.txt
├── README.md
└── .gitignore
```

## Observação

A plataforma funciona localmente e não precisa estar publicada na internet. O arquivo `dados.json` é utilizado como persistência simples e adequada ao escopo atual do projeto.
