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
  - `Stack` (pilha)  
  - `LinkedList` (lista ligada)  
  - `RegionTree` (árvore binária de busca)  
  - `Occurrence` (representa cada ocorrência)  
  - `FireResponseSimulator` (controla fila, histórico e relatórios)  
  - Funções de UI: limpar tela, cabeçalho, menu, pausa  
  - `run_interactive()`: exibe o menu e processa interações

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

