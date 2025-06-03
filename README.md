# Entrega DYNAMIC PROGRAMMING Global Solution
---

## Grupo:
- Gustavo – 559098  
- Matheus A. – 555177  
- Matheus Q. – 558801  

---

## Introdução

Este projeto consiste em um simulador de resposta a ocorrências de queimadas escrito em Python, chamado **IGNIRA**, destinado a coordenar equipes de combate a incêndios florestais. O programa utiliza diversas estruturas de dados (fila de prioridade, pilha, lista ligada, árvore e dicionário) para gerenciar inserção, atendimento, histórico e relatórios. A interface é um menu interativo via terminal, com saída formatada para facilitar o uso.

---

### Estrutura do Projeto

- **main.py**: contém todas as classes e funções:
 - **Stack**: pilha LIFO para armazenar ações de cada ocorrência.
  - **LinkedList**: lista ligada para manter o histórico de atendimentos.
  - **RegionTree**: árvore binária para organizar nomes de regiões em ordem alfabética.
  - **Occurrence**: representa cada ocorrência de queimada (ID, região, grau, status, timestamp e ações).
  - **MHeap**: implementação de max-heap (sem usar `heapq`) para priorizar ocorrências por `Grau` e `timestamp`.
  - **FireResponseSimulatorComMapeamento**: gerencia fila de ocorrências, histórico, relatórios e permite atualizar status pelo ID.
  - Funções de UI:
    - `clear_screen()`, `print_header(title)`, `pause()`
    - `main_menu()`: exibe opções e lê escolha do usuário.
    - `run_interactive()`: loop principal que processa cada opção de menu.

---

## Ao rodar o código, surgirá o menu:

    ============================================================
                Simulador de Resposta a Queimadas               
    ============================================================
    1. Inserir nova ocorrência
    2. Listar ocorrências pendentes
    3. Atender próxima ocorrência
    4. Atualizar status de ocorrência
    5. Listar histórico de atendimentos
    6. Gerar relatório por região
    7. Simular chamadas aleatórias
    0. Sair
    Escolha uma opção:

Digite o número correspondente e pressione Enter para navegar.

---
## Funcionalidades do MENU
- **1**Inserir nova ocorrência 
  --Solicita nome da região e grau (1–10). Se o grau não for inteiro, retorna ao menu.
  --Cria uma instância `Occurrence` (ID gerado automaticamente, status “pendente”, timestamp atual).
  --Insere no ` MHeap ` (por prioridade de grau e timestamp) e registra a região na RegionTree.
  Exibe:
