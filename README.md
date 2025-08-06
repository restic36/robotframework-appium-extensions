# Repositório de Experimentos - Implementação de Keywords

Este repositório contém o desenvolvimento dos experimentos para implementação das seguintes keywords no projeto:

- Keyword: Long Press
- Keyword: Pinch
- Keyword: Zoom

## 📄 Organização do Repositório

O fluxo de trabalho neste repositório segue uma estratégia simples e eficiente de branches, garantindo organização, colaboração e integridade do código.

### 🚀 Branches

- **main** → Contém a versão estável do projeto. Nenhum desenvolvimento direto deve ser feito nesta branch.
- **develop** → Branch de integração. Todas as tarefas concluídas serão integradas aqui antes de serem movidas para `main`.
- **feature/** → Branches individuais para cada tarefa/keyword. Cada desenvolvedor trabalhará exclusivamente em sua branch.

Exemplo de nomenclatura das branches:
- `feature/keyword-long-press`
- `feature/keyword-pinch`
- `feature/keyword-zoom`

## ✅ Fluxo de Trabalho

1. **Criar a branch da sua tarefa**
    ```bash
    git checkout develop
    git pull
    git checkout -b feature/keyword-nome-da-keyword
    ```

2. **Desenvolver sua tarefa**
    - Realize commits pequenos e frequentes.
    - Sempre adicione mensagens claras nos commits.

3. **Enviar sua branch para o repositório**
    ```bash
    git push -u origin feature/keyword-nome-da-keyword
    ```

4. **Abrir um Pull Request**
    - Ao concluir a tarefa, abra um **Pull Request (PR)** para a branch `develop`.
    - O PR será revisado antes do merge.

5. **Merge para develop**
    - Após aprovação, o PR será integrado na branch `develop`.

6. **Merge para main**
    - Quando todas as tarefas forem concluídas e testadas na branch `develop`, será feito o merge para `main` com uma nova release.
**Pegar o local exato do app pra abrir:** adb shell dumpsys window | findstr "mCurrentFocus mFocusedApp

> **Importante:** Antes de iniciar ou continuar uma tarefa, sempre atualize sua branch local para evitar conflitos:
```bash
git checkout develop
git pull
git checkout feature/keyword-nome-da-keyword
git merge develop
