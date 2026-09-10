name: polistudy
description: Orienta o desenvolvimento do PoliStudy, uma plataforma de organização de estudos em Python e Streamlit. Use esta skill ao criar, revisar ou modificar funcionalidades do projeto.
---

# PoliStudy Skill

## Objetivo

Auxiliar no desenvolvimento do PoliStudy mantendo o projeto simples,
funcional e fácil de entender.

## Tecnologias

- Usar Python como linguagem principal.
- Usar Streamlit para a interface.
- Usar JSON para persistência local dos dados.
- Evitar bibliotecas externas quando não forem necessárias.

## Regras de desenvolvimento

- Manter o código simples e legível.
- Explicar brevemente mudanças importantes antes de implementá-las.
- Não remover funcionalidades existentes sem necessidade.
- Preservar os dados já armazenados.
- Evitar complexidade desnecessária.
- Preferir soluções adequadas para um projeto de pequeno porte.

## Funcionalidades do PoliStudy

A plataforma deve permitir:

- cadastrar matérias;
- armazenar matérias em JSON;
- cadastrar provas, trabalhos e tarefas;
- armazenar atividades em JSON;
- excluir matérias individualmente;
- excluir atividades individualmente;
- limpar todos os dados ao final do semestre;
- priorizar automaticamente as atividades de estudo;
- visualizar atividades em um calendário acadêmico mensal e semanal.

## Dados

O arquivo dados.json deve armazenar as informações persistentes
da plataforma.

Ao modificar sua estrutura, preserve compatibilidade com os dados
existentes sempre que possível.

## Exclusão de dados

- A exclusão de uma atividade deve remover apenas aquela atividade.
- Ao excluir uma matéria com atividades associadas, evitar atividades
órfãs e avisar o usuário antes da exclusão.
- A função "Limpar semestre" deve pedir confirmação antes de apagar
todas as matérias e atividades.

### Priorização automática

A prioridade das atividades deve ser calculada de forma determinística
e explicável.

O cálculo deve considerar:

- urgência da atividade;
- importância definida pelo usuário;
- dificuldade da matéria associada.

A fórmula utilizada deve ser:

Prioridade = 0,45 × urgência + 0,35 × importância + 0,20 × dificuldade.

Os pesos e critérios não devem ser alterados sem uma justificativa
ou explicação prévia.

As atividades devem ser exibidas da maior para a menor prioridade,
com uma explicação simples dos fatores que influenciaram o resultado.

### Calendário acadêmico

O calendário deve utilizar as atividades já armazenadas no `dados.json`.

Ele deve permitir:

- visualizar as atividades por mês;
- visualizar as atividades por semana;
- identificar o nome da atividade;
- identificar a matéria associada;
- visualizar provas, trabalhos e tarefas em suas respectivas datas.

O calendário deve apenas representar visualmente os dados já existentes.

A visualização do calendário não deve:

- criar atividades duplicadas;
- alterar datas automaticamente;
- modificar informações sem uma ação explícita do usuário.

## Verificação

Após modificar o projeto:

1. verificar se o Streamlit inicia sem erros;
2. testar a funcionalidade alterada;
3. confirmar que os dados continuam sendo salvos corretamente;
4. verificar se funcionalidades anteriores continuam funcionando.