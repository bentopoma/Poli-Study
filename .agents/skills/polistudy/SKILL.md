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
- armazenar matérias;
- cadastrar provas, trabalhos e tarefas;
- armazenar atividades;
- excluir matérias individualmente;
- excluir atividades individualmente;
- limpar os dados ao final do semestre;
- futuramente, priorizar automaticamente o que estudar.

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

## Verificação

Após modificar o projeto:

1. verificar se o Streamlit inicia sem erros;
2. testar a funcionalidade alterada;
3. confirmar que os dados continuam sendo salvos corretamente;
4. verificar se funcionalidades anteriores continuam funcionando.