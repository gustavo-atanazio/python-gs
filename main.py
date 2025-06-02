import heapq
import random
import datetime
import os
from typing import Any, Optional, List, Dict, Tuple

# ------------------------------------------------------------
# Estrutura de Pilha (para armazenar ações em cada ocorrência)
# ------------------------------------------------------------
class Stack:
    """
    Implementação simples de uma pilha (LIFO) usando lista interna.
    Métodos:
        push(item): empilha um item.
        pop() -> item: desempilha e retorna o item.
        is_empty() -> bool: verifica se a pilha está vazia.
    """
    def __init__(self) -> None:
        self._items: List[Any] = []

    def push(self, item: Any) -> None:
        """Coloca um item no topo da pilha."""
        self._items.append(item)

    def pop(self) -> Any:
        """Remove e retorna o item do topo da pilha. Lança IndexError se vazia."""
        if self.is_empty():
            raise IndexError("Pop de pilha vazia")
        return self._items.pop()

    def is_empty(self) -> bool:
        """Retorna True se a pilha estiver vazia, caso contrário False."""
        return len(self._items) == 0

    def __len__(self) -> int:
        """Número de elementos na pilha."""
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items!r})"


# ------------------------------------------------------------
# Estrutura de Lista Ligada (para histórico de atendimentos)
# ------------------------------------------------------------
class Node:
    """
    Nó de lista ligada contendo referência à ocorrência atendida e ao próximo nó.
    """
    def __init__(self, data: Any) -> None:
        self.data: Any = data
        self.next: Optional['Node'] = None

class LinkedList:
    """
    Implementação de lista ligada simplesmente encadeada.
    Métodos:
        append(data): adiciona um novo nó ao final da lista.
        traverse() -> List[Any]: retorna lista de todos os dados armazenados, em ordem.
    """
    def __init__(self) -> None:
        self.head: Optional[Node] = None

    def append(self, data: Any) -> None:
        """Insere um novo nó com 'data' ao final da lista."""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            curr = self.head
            while curr.next is not None:
                curr = curr.next
            curr.next = new_node

    def traverse(self) -> List[Any]:
        """Retorna uma lista com todos os dados dos nós, em ordem."""
        result: List[Any] = []
        curr = self.head
        while curr is not None:
            result.append(curr.data)
            curr = curr.next
        return result

    def __repr__(self) -> str:
        return f"LinkedList({self.traverse()!r})"


# ------------------------------------------------------------
# Estrutura de Árvore Binária Simples (para organizar regiões)
# ------------------------------------------------------------
class RegionTreeNode:
    """
    Nó de uma árvore binária, contendo nome da região e dois filhos.
    """
    def __init__(self, region_name: str) -> None:
        self.region_name: str = region_name
        self.left: Optional['RegionTreeNode'] = None
        self.right: Optional['RegionTreeNode'] = None

class RegionTree:
    """
    Árvore binária que organiza regiões (por ordem ALFABETICA dos nomes).
    Método:
        insert(region_name): insere novo nó na árvore.
        in_order_traversal() -> List[str]: retorna lista de regiões em ordem alfabética.
    """
    def __init__(self) -> None:
        self.root: Optional[RegionTreeNode] = None

    def insert(self, region_name: str) -> None:
        """Insere 'region_name' na árvore de regiões."""
        self.root = self._insert_rec(self.root, region_name)

    def _insert_rec(self, node: Optional[RegionTreeNode], region_name: str) -> RegionTreeNode:
        if node is None:
            return RegionTreeNode(region_name)
        if region_name < node.region_name:
            node.left = self._insert_rec(node.left, region_name)
        elif region_name > node.region_name:
            node.right = self._insert_rec(node.right, region_name)
        return node

    def in_order_traversal(self) -> List[str]:
        """Retorna lista de nomes de regiões em ordem alfabética."""
        result: List[str] = []
        self._in_order(self.root, result)
        return result

    def _in_order(self, node: Optional[RegionTreeNode], result: List[str]) -> None:
        if node is not None:
            self._in_order(node.left, result)
            result.append(node.region_name)
            self._in_order(node.right, result)

    def __repr__(self) -> str:
        return f"RegionTree({self.in_order_traversal()!r})"


# ------------------------------------------------------------
# Classe que representa uma Ocorrência de Queimada
# ------------------------------------------------------------
class Occurrence:
    """
    Representa uma ocorrência de queimada.
    Atributos:
        id: identificador único da ocorrência.
        region: string com o nome da região/município.
        Grau: nível da queimada (int maior → prioridade maior).
        status: 'pendente', 'em atendimento' ou 'concluída'.
        timestamp: data/hora de criação.
        actions: pilha de ações registradas durante o atendimento.
    Métodos:
        add_action(action): registra ação no atendimento (pilha).
        get_actions() -> List[str]: retorna lista de ações, da mais recente à mais antiga.
    """
    _counter = 0  # contador de IDs automáticos

    def __init__(self, region: str, Grau: int) -> None:
        self.id: int = Occurrence._generate_id()
        self.region: str = region
        self.Grau: int = Grau
        self.status: str = "pendente"
        self.timestamp: datetime.datetime = datetime.datetime.now()
        self.actions: Stack = Stack()

    @classmethod
    def _generate_id(cls) -> int:
        cls._counter += 1
        return cls._counter

    def add_action(self, action: str) -> None:
        """Registra uma ação realizada durante o atendimento (ex.: 'Equipe enviada', 'Fogo contido')."""
        self.actions.push(f"{datetime.datetime.now().isoformat()} - {action}")

    def get_actions(self) -> List[str]:
        """
        Retorna lista de ações registradas, do topo da pilha (mais recente) até o fundo,
        sem modificar a pilha original.
        """
        temp_stack = Stack()
        actions_list: List[str] = []

        while not self.actions.is_empty():
            item = self.actions.pop()
            actions_list.append(item)
            temp_stack.push(item)

        while not temp_stack.is_empty():
            self.actions.push(temp_stack.pop())

        return actions_list

    def __repr__(self) -> str:
        return (f"Occurrence(id={self.id}, region={self.region!r}, "
                f"Grau={self.Grau}, status={self.status!r})")


# ------------------------------------------------------------
# Classe Controladora do Simulador
# ------------------------------------------------------------
class FireResponseSimulator:
    """
    Simulador que gerencia ocorrências de queimada, IGNIRA.
    Usa:
        - heap (priority queue) para gerenciar fila de ocorrências.
        - lista ligada para armazenar histórico de atendimentos.
        - dicionário para relatório por região.
        - árvore binária para estruturar regiões (demonstrativo).
    """
    def __init__(self) -> None:
        self._queue: List[Tuple[int, datetime.datetime, Occurrence]] = []
        self._history: LinkedList = LinkedList()
        self._region_counts: Dict[str, int] = {}
        self._region_tree: RegionTree = RegionTree()

    def add_occurrence(self, region: str, Grau: int) -> Occurrence:
        """
        Insere nova ocorrência na fila de atendimento.
        """
        occ = Occurrence(region, Grau)
        heapq.heappush(self._queue, (-Grau, occ.timestamp, occ))
        self._region_tree.insert(region)
        return occ

    def attend_next(self) -> Optional[Occurrence]:
        """
        Remove da fila e atende a ocorrência de maior prioridade.
        Simula ações e atualiza histórico e relatório.
        """
        if not self._queue:
            return None

        _, _, occ = heapq.heappop(self._queue)
        occ.status = "em atendimento"
        occ.add_action("Início de atendimento")
        occ.add_action("Equipe alocada")
        occ.add_action("Fogo contido")
        occ.status = "concluída"
        occ.add_action("Atendimento finalizado")
        self._history.append(occ)
        self._region_counts[occ.region] = self._region_counts.get(occ.region, 0) + 1
        return occ

    def update_status(self, occurrence_id: int, new_status: str) -> bool:
        """
        Atualiza o status de uma ocorrência específica na fila (se ainda pendente).
        """
        for idx, (_sev, _ts, occ) in enumerate(self._queue):
            if occ.id == occurrence_id:
                occ.status = new_status
                return True
        return False

    def list_history(self) -> List[Occurrence]:
        """Retorna lista de todas as ocorrências atendidas, em ordem de atendimento."""
        return self._history.traverse()

    def generate_report(self) -> Dict[str, int]:
        """Gera relatório de quantidade de ocorrências atendidas por região."""
        return dict(self._region_counts)

    def simulate_random_calls(self, n_calls: int, max_Grau: int = 10) -> None:
        """Simula chamadas aleatórias de ocorrências."""
        sample_regions = ["Norte", "Sul", "Leste", "Oeste", "Centro", "Montanhas", "Planicie"]
        for i in range(1, n_calls + 1):
            region = random.choice(sample_regions)
            Grau = min(i, max_Grau)
            self.add_occurrence(region, Grau)

    def get_pending_list(self) -> List[Occurrence]:
        """Retorna lista de ocorrências pendentes (sem remover)."""
        return [occ for (_sev, _ts, occ) in sorted(self._queue, reverse=True)]


# ------------------------------------------------------------
# Funções de UI no terminal
# ------------------------------------------------------------
def clear_screen():
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str):
    """cabeçalho formatado com o título centralizado."""
    clear_screen()
    print("=" * 60)
    print(title.center(60))
    print("=" * 60)


def pause():
    """Pausa a execução até o usuário pressionar Enter."""
    input("\nPressione Enter para continuar...")


def main_menu():
    """Exibe o menu principal e retorna a opção escolhida."""
    print("1. Inserir nova ocorrência")
    print("2. Listar ocorrências pendentes")
    print("3. Atender próxima ocorrência")
    print("4. Atualizar status de ocorrência")
    print("5. Listar histórico de atendimentos")
    print("6. Gerar relatório por região")
    print("7. Simular chamadas aleatórias")
    print("0. Sair")
    print("Escolha uma opção: ", end="")
    try:
        choice = int(input())
    except ValueError:
        choice = -1
    return choice


def run_interactive():
    sim = FireResponseSimulator()
    while True:
        print_header("Simulador de Resposta a Queimadas (IGNIRA)")
        choice = main_menu()

        if choice == 1:
            print_header("Inserir Nova Ocorrência")
            region = input("Digite o nome da região (EX.: Norte,Sul,Leste,Oeste,Centro,Montanhas,Planicie, Vale, ETC): ")
            try:
                Grau = int(input("Digite o grau do incendio, dentro da escala (1 a 10): "))
            except ValueError:
                print("Grau de incêndio inválido. Operação cancelada.")
                pause()
                continue
            occ = sim.add_occurrence(region, Grau)
            print(f"Ocorrência inserida: {occ}")
            pause()

        elif choice == 2:
            print_header("Ocorrências Pendentes")
            pendings = sim.get_pending_list()
            if not pendings:
                print("Não há ocorrências pendentes.")
            else:
                for occ in pendings:
                    print(f"ID: {occ.id} | Região: {occ.region} | Grau: {occ.Grau} | Status: {occ.status}")
            pause()

        elif choice == 3:
            print_header("Atender Próxima Ocorrência")
            occ = sim.attend_next()
            if occ is None:
                print("Não há ocorrências pendentes.")
            else:
                print(f"Ocorrência atendida: {occ}")
                print("Ações registradas:")
                for action in occ.get_actions():
                    print(f"  - {action}")
            pause()

        elif choice == 4:
            print_header("Atualizar Status de Ocorrência")
            try:
                occ_id = int(input("Digite o ID da ocorrência: "))
            except ValueError:
                print("ID inválido. Operação cancelada.")
                pause()
                continue
            new_status = input("Digite o novo status (cancelado, em atendimento ou concluida): ")
            updated = sim.update_status(occ_id, new_status)
            if updated:
                print(f"Status atualizado para '{new_status}'.")
            else:
                print(f"Ocorrência ID={occ_id} não encontrada na fila pendente.")
            pause()

        elif choice == 5:
            print_header("Histórico de Atendimentos")
            history = sim.list_history()
            if not history:
                print("Histórico vazio.")
            else:
                for occ in history:
                    # chama occ.get_actions() 
                    concluido_em = occ.get_actions()[-1].split(" - ")[0]
                    print(f"ID: {occ.id} | Região: {occ.region} | Grau: {occ.Grau} | Concluída em: {concluido_em}")
            pause()
        elif choice == 6:
            print_header("Relatório por Região")
            report = sim.generate_report()
            if not report:
                print("Nenhuma ocorrência atendida ainda.")
            else:
                for region, count in report.items():
                    print(f"Região: {region} -> {count} ocorrência(s) atendida(s)")
            pause()

        elif choice == 7:
            print_header("Simular Chamadas Aleatórias")
            try:
                n_calls = int(input("Quantas chamadas deseja simular? "))
            except ValueError:
                print("Número inválido. Operação cancelada.")
                pause()
                continue
            sim.simulate_random_calls(n_calls)
            print(f"{n_calls} chamadas simuladas inseridas.")
            pause()

        elif choice == 0:
            print_header("Saindo do Simulador...")
            break

        else:
            print("Opção inválida. Tente novamente.")
            pause()


if __name__ == "__main__":
    run_interactive()
