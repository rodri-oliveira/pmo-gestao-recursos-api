# Gestão de Projetos e Recursos — API PMO

Backend desenvolvido em **Python e FastAPI** para apoiar o planejamento de projetos, a distribuição de profissionais e a análise de horas planejadas e efetivamente apontadas.

## Problema e solução

Quando projetos, equipes e horas são acompanhados em controles separados, fica difícil identificar sobrecargas e comparar planejamento com execução. A API estrutura essas informações em entidades relacionadas e fornece consultas e indicadores para uma interface gerencial.

## Funcionalidades presentes no repositório

- Cadastro e relacionamento entre **seções, equipes, recursos e projetos**.
- Gestão de **alocações** e **horas planejadas**.
- Consolidação de **apontamentos** e indicadores de **planejado × realizado**.
- Endpoints de relatórios, dashboards e filtros por período, projeto e equipe.
- Rotinas de integração e sincronização com plataforma de gestão de tarefas.
- Componentes de autenticação e registros de atividade.

## Arquitetura e tecnologias

**Python · FastAPI · Pydantic · PostgreSQL · SQLAlchemy · Alembic**

O código separa rotas HTTP (`app/api/`), serviços (`app/application/`), domínio (`app/domain/`), persistência (`app/infrastructure/`) e configuração (`app/core/`).

**Interface web:** [PMO — Frontend](https://github.com/rodri-oliveira/pmo-gestao-recursos-web).

## Como avaliar

O ponto de entrada está em `app/main.py`; as dependências estão em `requirements.txt`. Examine os modelos de alocação, as rotas de apontamentos e os serviços de relatórios.

**Pré-requisitos para demonstração:** uma instância de PostgreSQL, a configuração das integrações e uma base de dados de exemplo. A execução completa depende desses serviços; não há ambiente demonstrativo público disponível neste repositório.

## Competências demonstradas

Modelagem relacional, regras de negócio, APIs REST, integração entre sistemas, automação e construção de indicadores de gestão.

**Status:** implementação documentada; as integrações exigem configuração para execução local.
