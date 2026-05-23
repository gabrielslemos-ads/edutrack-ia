# Proposta: API CRUD para Disciplinas (Subjects)

## Why
Atualmente, não existe uma forma padronizada via API para que os usuários gerenciem suas disciplinas (subjects). A criação de endpoints CRUD é fundamental para permitir que a aplicação frontend possa criar, listar, atualizar e deletar os registros de disciplinas de forma segura e desacoplada.

## What Changes
Esta mudança introduz um conjunto completo de endpoints RESTful para o gerenciamento de disciplinas.

1.  **Novos Endpoints de API:** Serão criados os seguintes endpoints no Xano:
    - `POST /subjects`: Para criar uma nova disciplina.
    - `GET /subjects`: Para listar as disciplinas do usuário autenticado.
    - `PATCH /subjects/{id}`: Para atualizar uma disciplina específica.
    - `DELETE /subjects/{id}`: Para deletar uma disciplina específica.

## Impact
- **Backend:** O backend Xano será estendido com novos endpoints. A lógica de cada endpoint deverá implementar uma verificação de segurança para garantir que um usuário só possa manipular suas próprias disciplinas.
- **Frontend:** Habilita o desenvolvimento de funcionalidades completas de gerenciamento de disciplinas na interface do Streamlit.
- **Segurança:** A implementação correta do filtro por `user_id` em todos os endpoints é crítica para garantir a privacidade e a segurança dos dados dos usuários.