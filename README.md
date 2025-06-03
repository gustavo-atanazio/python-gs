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
  - **MHeap**: implementação de max-heap para priorizar ocorrências por `Grau` e `timestamp`.
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

1. **Inserir nova ocorrência**
   - Solicita nome da região e grau (1–10). Se o grau não for inteiro, retorna ao menu.
   - Cria uma instância `Occurrence` (ID gerado automaticamente, status “pendente”, timestamp atual).
   - Insere no `MHeap` (por prioridade de grau e timestamp) e registra a região na `RegionTree`.
   - Exibe:
     ```
     Ocorrência inserida: Occurrence(id=1, region='Vale', Grau=8, status='pendente')
     ```

2. **Listar ocorrências pendentes**
   - Chama `sim.get_pending_list()`, que retorna todas as ocorrências na fila, em ordem de prioridade.
   - Se não houver ocorrências, exibe “Não há ocorrências pendentes.”, caso contrário imprime:
     ```
     ID: 1 | Região: Vale | Grau: 8 | Status: pendente
     ```

3. **Atender próxima ocorrência**
   - Chama `sim.attend_next()`. Se a fila estiver vazia, imprime “Não há ocorrências pendentes.”
   - Caso haja, remove a ocorrência de maior prioridade, muda `status` para “em atendimento”, registra quatro ações (“Início de atendimento”, “Equipe alocada”, “Fogo contido”, “Atendimento finalizado”), altera `status` para “concluida”, adiciona ao histórico (`LinkedList`) e incrementa contador por região.
   - Exibe algo como:
     ```
     Ocorrência atendida: Occurrence(id=1, region='Vale', Grau=8, status='concluida')
     Ações registradas:
       - 2025-06-01T14:30:10.123456 - Início de atendimento
       - 2025-06-01T14:30:10.234567 - Equipe alocada
       - 2025-06-01T14:30:10.345678 - Fogo contido
       - 2025-06-01T14:30:10.456789 - Atendimento finalizado
     ```

4. **Atualizar status de ocorrência**
   - Solicita o ID da ocorrência e o novo status (`cancelado`, `em atendimento` ou `concluida`). Se inválido, retorna ao menu.
   - Se o ID estiver na fila (status “pendente”), remove a ocorrência do heap, atualiza `status` e remove o mapeamento interno para impedir novas atualizações. Exibe:
     ```
     Status atualizado para 'cancelado' e ocorrência removida da fila pendente.
     ```
   - Caso contrário, “Ocorrência ID=X não encontrada ou não está mais pendente.”

5. **Listar histórico de atendimentos**
   - Chama `sim.list_history()`, que retorna as ocorrências atendidas em ordem cronológica.
   - Se vazio, imprime “Histórico vazio.”. Senão, exibe para cada ocorrência:
     ```
     ID: 1 | Região: Vale | Grau: 8 | concluida em: 2025-06-01T14:30:10.456789
     ```
     (usa a ação mais recente do stack para obter o timestamp de conclusão)

6. **Gerar relatório por região**
   - Chama `sim.generate_report()`, que devolve um dicionário `{região: total_atendimentos}`.
   - Se vazio, imprime “Nenhuma ocorrência atendida ainda.”. Senão, exibe:
     ```
     Região: Vale      -> 2 ocorrência(s) atendida(s)
     Região: Montanhas -> 1 ocorrência(s) atendida(s)
     ```

7. **Simular chamadas aleatórias**
   - Solicita quantas chamadas simular; se inválido, retorna ao menu.
   - Chama `sim.simulate_random_calls(n_calls)`, que cria `n_calls` ocorrências em regiões sorteadas (`["Norte","Sul","Leste","Oeste","Centro","Montanhas","Planície","vale"]`) com grau incremental (até 10).
   - Exibe:
     ```
     5 chamadas simuladas inseridas.
     ```

0. **Sair**
   - Exibe “Saindo do Simulador...” e encerra o programa.


### Esclarecimentos/Comentários para o professor
Olá professor- Matheus Alves aqui, passando para esclarecer que utilizei llm para me auxiliar na correção do meu código e para ajustar os comentários ( Não estranhe se tiver muitos kkk). Gostaria de usar Kivy para deixar a interface mais bonita e incorpada, mas o pouco tempo que temos, para fazer tantas entregas, não me permite. 
