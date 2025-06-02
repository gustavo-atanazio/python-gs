# (EM PRODUÇÃO) ignore por agora.
Grupo:
 
Introdução
Este projeto consiste em um simulador de resposta a ocorrências de queimadas escrito em Python,  CHAMADO IGNIRA,  destinado a coordenar equipes de combate a incêndios florestais. O programa utiliza diversas estruturas de dados (fila de prioridade, pilha, lista ligada, árvore e dicionário) para gerenciar inserção, atendimento, histórico e relatórios. A interface é um menu interativo via terminal, com saída formatada para facilitar o uso.

Estrutura do Projeto


│
├── .editorconfig           # Configurações de formatação para editores compatíveis
├── README.md               # Este arquivo de instruções e explicações
└── main.py                 # Código-fonte do Simulador de Resposta a Queimadas
.editorconfig
Padroniza indentação (2 espaços), fim de linha (LF), codificação (UTF-8), e evita remoção automática de espaços finais ou inserção de nova linha no final do arquivo. Isso não afeta a execução do Python, mas faz com que editores compatíveis apliquem essas regras ao salvar.

main.py
Contém todas as classes e funções necessárias:

Stack (pilha)

LinkedList (lista ligada)

RegionTree (árvore binária de busca)

Occurrence (representa cada ocorrência de queimada)

FireResponseSimulator (controla fila, histórico, relatório)

Funções de UI (limpar tela, cabeçalho, menu, pausa)

Função run_interactive() que exibe o menu e trata as interações.

Instalação e Execução
Clonar ou  o repositório para uma pasta local (por exemplo, projeto-queimadas).

Abrir o terminal e navegar até essa pasta:


Executar o script com:


python main.py
ou
python3 main.py
Verificar se aparece o menu:



            Simulador de Resposta a Queimadas               

1. Inserir nova ocorrência
2. Listar ocorrências pendentes
3. Atender próxima ocorrência
4. Atualizar status de ocorrência
5. Listar histórico de atendimentos
6. Gerar relatório por região
7. Simular chamadas aleatórias
0. Sair
Escolha uma opção:
A partir daí, digite o número da opção e pressione Enter para navegar.

Como Funciona o Menu Interativo
Cada opção do menu chama uma rotina distinta. Estes são os detalhes de cada item:

Opção 1: Inserir nova ocorrência
Exibe cabeçalho “Inserir Nova Ocorrência”.

Pergunta ao usuário:

Digite o nome da região:

Digite a severidade (1 a 10):

Se a severidade não for um inteiro válido, mostra “Severidade inválida. Operação cancelada.” e retorna ao menu principal.

Caso seja válida, executa internamente:

python


occ = sim.add_occurrence(region, severity)
print(f"Ocorrência inserida: {occ}")
Cria Occurrence(region, severity) com ID único e status “pendente”.

Insere na heap (fila de prioridade) como (-severity, timestamp, occ).

Insere o nome da região em RegionTree.

Exibe, por exemplo:




Ocorrência inserida: Occurrence(id=1, region='Vale', severity=8, status='pendente')
pause() para aguardar o usuário pressionar Enter antes de voltar ao menu.

Opção 2: Listar ocorrências pendentes
Exibe cabeçalho “Ocorrências Pendentes”.

Executa:

python


pendings = sim.get_pending_list()
get_pending_list() faz sorted(self._queue, reverse=True) para retornar as instâncias Occurrence em ordem de maior severidade (e, em caso de empate, mais antiga primeiro).

Se a lista pendings estiver vazia, imprime:

mathematica


Não há ocorrências pendentes.
Caso contrário, percorre e exibe cada ocorrência:

yaml


ID: 1 | Região: Vale | Severidade: 8 | Status: pendente
ID: 2 | Região: Sul  | Severidade: 5 | Status: pendente
pause() retorna ao menu principal.

Opção 3: Atender próxima ocorrência
Exibe cabeçalho “Atender Próxima Ocorrência”.

Chama:

python


occ = sim.attend_next()
Se self._queue estiver vazia, retorna None e imprime “Não há ocorrências pendentes.”

Caso haja, faz heapq.heappop(self._queue) para remover a tupla de maior prioridade (-severity).

Altera occ.status = "em atendimento".

Empilha ações na Stack interna:

occ.add_action("Início de atendimento")

occ.add_action("Equipe alocada")

occ.add_action("Fogo contido")

occ.add_action("Atendimento finalizado")

Altera occ.status = "concluída".

Insere occ no fim de self._history.append(occ) (lista ligada).

Incrementa self._region_counts[occ.region] += 1.

Retorna a instância occ.

No terminal, se occ is None, imprime:

mathematica


Não há ocorrências pendentes.
Caso contrário, exibe:

yaml


Ocorrência atendida: Occurrence(id=1, region='Vale', severity=8, status='concluída')
Ações registradas:
  - 2025-06-01T14:30:10.123456 - Início de atendimento
  - 2025-06-01T14:30:10.234567 - Equipe alocada
  - 2025-06-01T14:30:10.345678 - Fogo contido
  - 2025-06-01T14:30:10.456789 - Atendimento finalizado
pause() aguarda Enter.

Opção 4: Atualizar status de ocorrência
Exibe cabeçalho “Atualizar Status de Ocorrência”.

Pergunta:

Digite o ID da ocorrência:

Se o valor não for inteiro, imprime “ID inválido. Operação cancelada.” e retorna ao menu.

Pergunta:

Digite o novo status (ex: cancelado):

Chama:

python


updated = sim.update_status(occ_id, new_status)
Percorre cada tupla em self._queue:

python


for (_sev, _ts, occ) in self._queue:
    if occ.id == occurrence_id:
        occ.status = new_status
        return True
Se encontrar, altera occ.status e retorna True; caso contrário, retorna False.

Se updated for True, exibe:

nginx


Status atualizado para 'cancelado'.
Caso contrário:



Ocorrência ID=7 não encontrada na fila pendente.
pause() retorna ao menu.

Opção 5: Listar histórico de atendimentos
Exibe cabeçalho “Histórico de Atendimentos”.

Executa:

python


history = sim.list_history()
Internamente, list_history() chama self._history.traverse(), que percorre todos os nós da lista ligada, retornando uma List[Occurrence] em ordem cronológica de atendimento.

Se history estiver vazio, imprime:



Histórico vazio.
Caso contrário, para cada occ em history, recupera a data da última ação (timestamp da conclusão) com:

python


concluido_em = occ.get_actions()[-1].split(" - ")[0]
e imprime:

yaml


ID: 1 | Região: Vale | Severidade: 8 | Concluída em: 2025-06-01T14:30:10.456789
ID: 2 | Região: Sul  | Severidade: 5 | Concluída em: 2025-06-01T14:45:22.123456
pause() retorna ao menu.

Importante: caso apareça o erro AttributeError: 'Stack' object has no attribute 'get_actions', significa que, no código, estava-se chamando occ.actions.get_actions() em vez de occ.get_actions(). A correção é usar occ.get_actions() ao invés de occ.actions.get_actions().

Opção 6: Gerar relatório por região
Exibe cabeçalho “Relatório por Região”.

Executa:

python


report = sim.generate_report()
generate_report() devolve dict(self._region_counts), ou seja, o dicionário que mapeia cada região para o número de ocorrências já atendidas nela.

Se report estiver vazio ({}), imprime:

nginx


Nenhuma ocorrência atendida ainda.
Caso contrário, imprime cada par (region, count):

css


Região: Vale      -> 2 ocorrência(s) atendida(s)
Região: Montanhas -> 1 ocorrência(s) atendida(s)
pause() retorna ao menu.

Por que, ao criar ou simular ocorrências, elas não aparecem imediatamente no relatório?
Porque o dicionário self._region_counts só é atualizado dentro do método attend_next(). Ou seja, para entrar no relatório, a ocorrência precisa ter sido atendida de fato. Até lá, ela fica apenas na fila (self._queue), visível em “Listar ocorrências pendentes” (Opção 2).

Opção 7: Simular chamadas aleatórias
Exibe cabeçalho “Simular Chamadas Aleatórias”.

Pergunta:

Quantas chamadas deseja simular?

Se o valor não for inteiro, imprime “Número inválido. Operação cancelada.” e retorna ao menu.

Chama:

python


sim.simulate_random_calls(n_calls)
Internamente, escolhe, em cada iteração i de 1 a n_calls:

region = random.choice(sample_regions) (lista fixa: ["Norte","Sul","Leste","Oeste","Centro","Montanhas","Planicie"])

severity = min(i, max_severity) (por padrão, max_severity = 10)

self.add_occurrence(region, severity) — insere na heap como (–severity, timestamp, occ) e em RegionTree.

Exibe:



5 chamadas simuladas inseridas.
(caso n_calls = 5)

pause() retorna ao menu.

Opção 0: Sair
Exibe cabeçalho “Saindo do Simulador...”.

Sai do loop while True em run_interactive() e encerra o programa.

Detalhamento das Estruturas de Dados
Heap (Fila de Prioridade)
Implementação: self._queue: List[Tuple[int, datetime, Occurrence]]

Uso:

Em add_occurrence(region, severity), faz:

python


heapq.heappush(self._queue, (-severity, occ.timestamp, occ))
Em attend_next(), faz:

python


_, _, occ = heapq.heappop(self._queue)
Motivo: a tupla (–severity, timestamp) garante que aprendemos:

O valor mínimo de –severity corresponde à maior severidade (por isso a negação).

Em caso de empate na severidade, o timestamp resolve, atendendo primeiro quem foi criado mais cedo.

Complexidade: inserção e remoção em O(log n), com n = número de ocorrências pendentes.

Pilha (Stack)
Classe:

python


class Stack:
    def __init__(self): ...
    def push(self, item): ...
    def pop(self): ...
    def is_empty(self): ...
    def __len__(self): ...
    def __repr__(self): ...
Uso:

Cada Occurrence tem atributo self.actions = Stack().

Em attend_next(), regista-se cada etapa do atendimento:

python


occ.add_action("Início de atendimento")
occ.add_action("Equipe alocada")
occ.add_action("Fogo contido")
occ.add_action("Atendimento finalizado")
add_action() faz self.actions.push(f"{timestamp} - {ação}").

Para mostrar as ações em LIFO (mais recente primeiro), usa-se occ.get_actions(), que percorre a pilha temporariamente para extrair todos os itens, depois reconstrói.

Complexidade: push e pop em O(1).

Lista Ligada (LinkedList)
Classes:

python


class Node:
    def __init__(self, data: Any): ...
    self.data = data
    self.next = None

class LinkedList:
    def __init__(self): self.head = None
    def append(self, data: Any): ...         # adiciona ao final
    def traverse(self) -> List[Any]: ...     # retorna lista de dados
    def __repr__(self): ...
Uso:

Em fireResponseSimulator.__init__, criamos self._history = LinkedList().

Ao concluir cada atendimento em attend_next(), fazemos:

python


self._history.append(occ)
Para listar o histórico (opção 5), chamamos self._history.traverse(), que retorna uma lista Python com todas as instâncias Occurrence atendidas, em ordem cronológica.

Complexidade:

append: O(m), onde m = tamanho atual da lista (percorre até o final).

traverse: O(k), onde k = número de elementos (para exibir todo o histórico).

Árvore Binária (RegionTree)
Classes:

python


class RegionTreeNode:
    def __init__(self, region_name: str):
        self.region_name = region_name
        self.left = None
        self.right = None

class RegionTree:
    def __init__(self): self.root = None
    def insert(self, region_name: str): ...
    def in_order_traversal(self) -> List[str]: ...
    def __repr__(self): ...
Uso:

Sempre que uma nova ocorrência é criada (em add_occurrence), chama-se:

python


self._region_tree.insert(region)
Isso insere, em ordem lexicográfica, o region_name na árvore. Se já existir, ignora.

Embora não haja uma opção de menu específica, é possível extrair a lista de regiões em ordem alfabética usando self._region_tree.in_order_traversal().

Objetivo: Demonstrar uso de árvore para organização (Modelagem com grafos/árvores, do Conjunto 1).

Dicionário para Relatório
Atributo: self._region_counts: Dict[str,int] = {}

Uso:

Ao atender uma ocorrência (em attend_next()), após mudar status e registrar ações:

python


self._region_counts[occ.region] = self._region_counts.get(occ.region, 0) + 1
Isso garante que, ao chamar generate_report(), temos:

python


return dict(self._region_counts)
mapeando cada região para quantas ocorrências já foram atendidas.

Complexidade: acesso e atualização em O(1).

Exemplos Práticos de Uso
Imagine a seguinte sequência de comandos no terminal:

text


$ python main.py
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
Escolha uma opção:  1

============================================================
               Inserir Nova Ocorrência                      
============================================================
Digite o nome da região: Vale
Digite a severidade (1 a 10): 8
Ocorrência inserida: Occurrence(id=1, region='Vale', severity=8, status='pendente')

Pressione Enter para continuar...

============================================================
            Simulador de Resposta a Queimadas               
============================================================
Escolha uma opção:  2

============================================================
             Ocorrências Pendentes                         
============================================================
ID: 1 | Região: Vale | Severidade: 8 | Status: pendente

Pressione Enter para continuar...

============================================================
            Simulador de Resposta a Queimadas               
============================================================
Escolha uma opção:  3

============================================================
           Atender Próxima Ocorrência                      
============================================================
Ocorrência atendida: Occurrence(id=1, region='Vale', severity=8, status='concluída')
Ações registradas:
  - 2025-06-01T14:30:10.123456 - Início de atendimento
  - 2025-06-01T14:30:10.234567 - Equipe alocada
  - 2025-06-01T14:30:10.345678 - Fogo contido
  - 2025-06-01T14:30:10.456789 - Atendimento finalizado

Pressione Enter para continuar...

============================================================
            Simulador de Resposta a Queimadas               
============================================================
Escolha uma opção:  6

============================================================
               Relatório por Região                        
============================================================
Região: Vale -> 1 ocorrência(s) atendida(s)

Pressione Enter para continuar...

============================================================
            Simulador de Resposta a Queimadas               
============================================================
Escolha uma opção:  0

============================================================
            Saindo do Simulador...                         
============================================================
Outro exemplo com simulação aleatória:

text


$ python main.py
============================================================
            Simulador de Resposta a Queimadas               
============================================================
Escolha uma opção:  7

============================================================
         Simular Chamadas Aleatórias                       
============================================================
Quantas chamadas deseja simular? 5
5 chamadas simuladas inseridas.

Pressione Enter para continuar...

============================================================
            Simulador de Resposta a Queimadas               
============================================================
Escolha uma opção:  2

============================================================
             Ocorrências Pendentes                         
============================================================
ID: 5 | Região: Planicie    | Severidade: 5 | Status: pendente
ID: 4 | Região: Montanhas   | Severidade: 4 | Status: pendente
ID: 3 | Região: Oeste       | Severidade: 3 | Status: pendente
ID: 2 | Região: Sul         | Severidade: 2 | Status: pendente
ID: 1 | Região: Norte       | Severidade: 1 | Status: pendente

Pressione Enter para continuar...

============================================================
            Simulador de Resposta a Queimadas               
============================================================
Escolha uma opção:  3

============================================================
           Atender Próxima Ocorrência                      
============================================================
Ocorrência atendida: Occurrence(id=5, region='Planicie', severity=5, status='concluída')
Ações registradas:
  - 2025-06-01T14:40:00.123456 - Início de atendimento
  - 2025-06-01T14:40:00.234567 - Equipe alocada
  - 2025-06-01T14:40:00.345678 - Fogo contido
  - 2025-06-01T14:40:00.456789 - Atendimento finalizado

Pressione Enter para continuar...

============================================================
            Simulador de Resposta a Queimadas               
============================================================
Escolha uma opção:  6

============================================================
               Relatório por Região                        
============================================================
Região: Planicie -> 1 ocorrência(s) atendida(s)

Pressione Enter para continuar...
Como o Projeto Atende aos Requisitos e à Pontuação
A seguir, detalhamos como cada critério de avaliação (totalizando 100 pontos) é satisfeito pelo main.py.

Qualidade de código (30 pontos)
Modularização e Reutilização

Tudo está organizado em classes com responsabilidades bem definidas (Stack, LinkedList, RegionTree, Occurrence, FireResponseSimulator).

Funções de UI (clear_screen, print_header, pause, main_menu) estão separadas da lógica de negócio.

Nomes e PEP 8

Nomes de classes em CamelCase e de métodos/variáveis em snake_case.

Indentação de 2 espaços (conforme .editorconfig).

Docstrings explicando atributos e métodos.

Comentários em pontos-chave (como explicações sobre o uso de heapq e a negação de severity).

Tratamento de erros e validações

Em entradas do usuário (ex.: int(input())), há try/except ValueError para não deixar o programa quebrar.

Mensagens claras em caso de erro (“Severidade inválida. Operação cancelada.”, “ID inválido. Operação cancelada.”).

Uso de todos os conceitos do conjunto escolhido (30 pontos)
Conjunto 1 — todos estão presentes:

Heap (fila de prioridade)

self._queue e uso de heapq.heappush/heappop.

Pilha (Stack)

Classe Stack e métodos push, pop, is_empty.

Occurrence.actions armazena etapas do atendimento em LIFO.

Lista ligada (LinkedList)

Classes Node e LinkedList.

self._history.append(occ) registra cada atendimento concluído.

list_history() retorna ordem cronológica.

Árvore binária (RegionTree)

RegionTree organiza nomes de regiões em ordem alfabética.

Método in_order_traversal() pode trazer a lista de regiões ordenadas (não há menu específico, mas a estrutura existe).

Dicionários para relatório

self._region_counts: Dict[str,int] conta quantas ocorrências foram atendidas por região.

Otimização e eficiência (10 pontos)
Heap: inserções e remoções em O(log n).

Stack: operações em O(1).

Lista ligada: append em O(m), onde m = tamanho do histórico; traverse em O(k). Considera-se aceitável, pois o histórico só cresce à medida que atendemos ocorrências.

Dicionário: acesso/atualização em O(1).

Nenhuma ordenação desnecessária:

A fila principal permanece como heap; a ordenação via sorted(...) só ocorre quando o usuário pede para listar pendentes.

Adequação à tarefa (30 pontos)
Inserir nova ocorrência

Opção 1 chama add_occurrence(region, severity) → instancia Occurrence, insere na heap e em RegionTree.

Atender próxima ocorrência com maior prioridade

Opção 3 chama attend_next(), que retira da heap a tupla (-severity, timestamp, occ).

Registrar ações realizadas

Em attend_next(), chama-se occ.add_action(...) quatro vezes e, posteriormente, exibe-se via occ.get_actions().

Listar histórico da equipe

Opção 5 chama list_history(), que devolve self._history.traverse(). Exibe-se ID, região, severidade e data de conclusão de cada ocorrência.

Atualizar status

Opção 4 chama update_status(occ_id, new_status), que percorre a fila (self._queue) procurando occ.id == occ_id e faz occ.status = new_status.

Gerar relatório de atendimento por região

Opção 6 chama generate_report(), que devolve dict(self._region_counts). Exibe quantas ocorrências foram concluídas por região.

Simular chamadas aleatórias com severidade crescente

Opção 7 chama simulate_random_calls(n_calls). Em cada loop, escolhe region aleatoriamente e severidade = min(i, max_severity).

Interface interativa e legível

clear_screen() + print_header(title) mantém a tela limpa e títulos centralizados.

Mensagens objetivas e formatadas facilitam a leitura.
