---
name: polistudy
description: Orienta o desenvolvimento do PoliStudy, uma plataforma de organização, acompanhamento e priorização de estudos em Python e Streamlit. Use esta skill ao criar, revisar ou modificar funcionalidades do projeto.
---

# PoliStudy Skill

## Objetivo

Auxiliar no desenvolvimento do PoliStudy mantendo o projeto simples, funcional, legível e fácil de entender.

A plataforma deve apoiar o estudante na organização de matérias, atividades, prazos, prioridades e planejamento de estudos ao longo do semestre.

## Tecnologias

- Usar Python como linguagem principal.
- Usar Streamlit para a interface.
- Usar JSON para persistência local dos dados.
- Usar `streamlit-calendar` para o calendário acadêmico.
- Evitar bibliotecas externas quando não forem necessárias.

## Regras de desenvolvimento

- Manter o código simples, organizado e legível.
- Explicar brevemente mudanças importantes antes de implementá-las.
- Não remover funcionalidades existentes sem necessidade.
- Preservar os dados já armazenados.
- Evitar complexidade desnecessária.
- Preferir soluções adequadas para um projeto de pequeno porte.
- Preservar identificadores únicos (`id`) de matérias e atividades durante edições.
- Evitar registros duplicados.
- Sempre que possível, manter compatibilidade com versões anteriores do `dados.json`.

## Funcionalidades do PoliStudy

A plataforma deve permitir:

- cadastrar matérias;
- armazenar matérias em JSON;
- editar matérias já cadastradas;
- excluir matérias individualmente;
- cadastrar provas, trabalhos e tarefas;
- armazenar atividades em JSON;
- editar atividades já cadastradas;
- excluir atividades individualmente;
- marcar atividades como pendentes ou concluídas;
- filtrar atividades por tipo, status e matéria;
- visualizar atividades pendentes dos próximos 7 dias;
- priorizar automaticamente as atividades de estudo;
- visualizar atividades em um calendário acadêmico mensal e semanal;
- visualizar métricas rápidas sobre o semestre;
- simular notas com diferentes pesos de avaliações;
- sugerir uma distribuição de tempo de estudo com base nas prioridades;
- limpar todos os dados ao final do semestre.

## Dados

O arquivo `dados.json` deve armazenar as informações persistentes da plataforma.

A estrutura deve conter, no mínimo:

- `materias`;
- `atividades`.

Cada matéria e atividade deve possuir um identificador único (`id`).

As atividades devem possuir um campo booleano `concluida`, utilizando `False` como padrão para registros antigos ou novas atividades ainda não concluídas.

Ao modificar a estrutura do arquivo, preserve compatibilidade com os dados existentes sempre que possível.

## Edição e consistência dos dados

- A edição deve atualizar o registro existente em vez de criar um novo.
- O `id` do registro deve ser preservado durante a edição.
- Ao renomear uma matéria, atualizar também as atividades associadas para evitar vínculos inconsistentes.
- Alterações devem ser persistidas imediatamente no `dados.json`.
- O cancelamento de uma edição não deve alterar os dados salvos.

## Exclusão de dados

- A exclusão de uma atividade deve remover apenas aquela atividade.
- Ao excluir uma matéria com atividades associadas, avisar o usuário antes da exclusão.
- Caso a exclusão da matéria seja confirmada, remover também suas atividades associadas para evitar atividades órfãs.
- A função "Limpar semestre" deve pedir confirmação antes de apagar todas as matérias e atividades.

## Status das atividades

Cada atividade deve poder ser marcada como:

- pendente;
- concluída.

Atividades concluídas:

- devem permanecer armazenadas como histórico;
- não devem aparecer no ranking de prioridades;
- não devem aparecer na seção "Esta semana";
- devem continuar visíveis no calendário com diferenciação visual;
- devem poder ser reabertas como pendentes.

## Filtros de atividades

A lista de atividades deve permitir filtros independentes por:

- tipo: todas, provas, trabalhos ou tarefas;
- status: todas, pendentes ou concluídas;
- matéria.

Os filtros devem afetar apenas a visualização e nunca alterar ou excluir dados.

## Priorização automática

A prioridade das atividades deve ser calculada de forma determinística e explicável.

O cálculo deve considerar:

- urgência da atividade;
- importância definida pelo usuário;
- dificuldade da matéria associada.

A fórmula utilizada deve ser:

`Prioridade = 0,45 × urgência + 0,35 × importância + 0,20 × dificuldade`

Os pesos e critérios não devem ser alterados sem uma justificativa ou explicação prévia.

As atividades devem ser exibidas da maior para a menor prioridade, com uma explicação simples dos fatores que influenciaram o resultado.

Atividades atrasadas devem receber destaque visual e aparecer antes das atividades ainda dentro do prazo.

## Esta semana

A seção "Esta semana" deve exibir apenas atividades pendentes cujo prazo esteja entre hoje e os próximos 6 dias.

A condição utilizada deve ser:

`0 <= dias_ate_o_prazo < 7`

As atividades devem ser ordenadas cronologicamente e exibir:

- dia da semana;
- data;
- nome da atividade;
- matéria;
- tipo.

Atividades atrasadas e concluídas não devem aparecer nesta seção.

## Calendário acadêmico

O calendário deve utilizar as atividades já armazenadas no `dados.json`.

Ele deve permitir:

- visualizar as atividades por mês;
- visualizar as atividades por semana;
- identificar o nome da atividade;
- identificar a matéria associada;
- visualizar provas, trabalhos e tarefas em suas respectivas datas;
- diferenciar visualmente atividades concluídas.

O calendário deve apenas representar visualmente os dados já existentes.

A visualização do calendário não deve:

- criar atividades duplicadas;
- alterar datas automaticamente;
- modificar informações sem uma ação explícita do usuário.

## Métricas rápidas

A plataforma deve apresentar, de forma compacta, métricas úteis sobre o semestre, como:

- quantidade de atividades pendentes;
- quantidade de atividades concluídas;
- quantidade de atividades atrasadas;
- quantidade de provas nos próximos 7 dias.

As métricas devem ser calculadas a partir dos dados já existentes, sem criar novos registros.

## Simulador de notas

O simulador deve permitir ao usuário:

- escolher uma matéria;
- definir quantas avaliações existem no semestre;
- informar o nome ou tipo de cada avaliação;
- atribuir pesos diferentes a provas, trabalhos e outras atividades;
- informar notas já obtidas;
- definir uma nota final desejada.

O simulador deve utilizar média ponderada quando os pesos forem diferentes.

Quando os pesos forem iguais, o resultado naturalmente equivale à média aritmética.

O simulador deve informar, quando aplicável:

- média parcial;
- peso já realizado;
- peso restante;
- nota média necessária nas avaliações restantes para atingir a nota desejada.

O simulador não deve alterar os dados persistentes das matérias ou atividades, salvo se isso for solicitado explicitamente em uma futura funcionalidade.

## Plano sugerido de estudos

A plataforma pode sugerir uma distribuição do tempo disponível de estudo entre atividades pendentes.

A sugestão deve:

- utilizar as prioridades já calculadas;
- considerar apenas atividades pendentes;
- distribuir o tempo de forma proporcional às prioridades;
- deixar claro que se trata de uma sugestão, e não de uma obrigação;
- não alterar datas, notas ou dados salvos.

## Organização da interface

A interface deve priorizar as informações mais úteis ao estudante no uso diário.

A ordem recomendada é:

1. título e apresentação;
2. métricas rápidas;
3. prioridades de estudo;
4. simulador de notas e plano sugerido de estudos;
5. seção "Esta semana";
6. calendário acadêmico;
7. cadastro e gerenciamento de atividades;
8. cadastro e gerenciamento de matérias;
9. gerenciamento do semestre.

Sempre que fizer sentido:

- usar `st.expander()` para formulários de cadastro;
- usar colunas para aproveitar melhor o espaço horizontal;
- usar `st.divider()` para separar seções;
- manter a página organizada em `layout="wide"`;
- evitar excesso de elementos visuais ou informações repetidas.

## Verificação

Após modificar o projeto:

1. verificar se o Streamlit inicia sem erros;
2. testar a funcionalidade alterada;
3. confirmar que os dados continuam sendo salvos corretamente;
4. verificar se funcionalidades anteriores continuam funcionando;
5. testar fechamento e reabertura da aplicação;
6. confirmar que o `dados.json` continua válido;
7. verificar se calendário, prioridades e filtros refletem corretamente as alterações;
8. evitar alterações desnecessárias no `README.md`, `requirements.txt` ou na estrutura de dados.
