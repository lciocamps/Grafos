import random
import time


def gerar_grafo(n, p): # gera um grafo simples nao direcionado com n vertices, cada aresta com probabilidade p
    V = list(range(1, n + 1))
    E = []

    # cada par {u, v} e visitado uma vez (j > i): sem lacos e sem arestas repetidas
    for i in range(len(V)):
        for j in range(i + 1, len(V)):
            # a aresta entra no grafo com probabilidade p
            if random.random() < p:
                E.append((V[i], V[j]))

    return V, E


def graus(G): # calcula o grau de cada vertice
    V, E = G
    grau_dict = {v: 0 for v in V}

    for u, v in E:
        grau_dict[u] += 1
        grau_dict[v] += 1

    return grau_dict


def conexo(G): # verifica se todos os vertices com grau maior que 0 pertencem a mesma componente conexa
    V, E = G
    grau_dict = graus(G)

    # vertices isolados sao ignorados pelo criterio de euler
    vertices_ativos = [v for v in V if grau_dict[v] > 0]

    # sem vertices de grau nao nulo, nao ha o que conectar
    if len(vertices_ativos) == 0:
        return True

    # lista de adjacencia: cada aresta (u, v) aparece na lista de u e na de v
    adj = {v: [] for v in V}

    for u, v in E:
        adj[u].append(v)
        adj[v].append(u)

    # bfs a partir de um vertice ativo qualquer (o primeiro da lista)
    visitados = set()
    inicio = vertices_ativos[0]
    fila = [inicio]
    visitados.add(inicio)

    while fila:
        atual = fila.pop(0)  # retira o vertice mais antigo da fila

        # enfileira vizinhos ainda nao visitados
        for viz in adj[atual]:
            if viz not in visitados:
                visitados.add(viz)
                fila.append(viz)

    # conexo se a bfs alcancou todos os vertices ativos
    for v in vertices_ativos:
        if v not in visitados:
            return False

    return True


def euleriano(G): # determina se o grafo possui circuito de euler

    # criterios: vertices com grau > 0 na mesma componente conexa e todos os graus pares
    V, E = G
    grau_dict = graus(G)

    # grafo sem arestas: circuito trivial (vazio)
    if len(E) == 0:
        return True

    # criterio 1: conectividade dos vertices de grau nao nulo
    if not conexo(G):
        return False

    # criterio 2: graus pares
    for v in V:
        if grau_dict[v] % 2 != 0:
            return False

    return True


def circuito_euler(G): # constroi o circuito de euler utilizando o algoritmo de hierholzer
    V, E = G

    # so existe circuito se o grafo for euleriano
    if not euleriano(G):
        return None

    grau_dict = graus(G)
    vertices_ativos = [v for v in V if grau_dict[v] > 0]

    # grafo vazio: circuito trivial
    if not vertices_ativos:
        return []

    # lista de adjacencia com id unico por aresta (a mesma aresta aparece nas listas dos dois extremos)
    adj = {v: [] for v in V}

    for idx, (u, v) in enumerate(E):
        adj[u].append((v, idx))
        adj[v].append((u, idx))

    arestas_usadas = set() # ids das arestas ja percorridas
    circuito = [] # vertices finalizados (ordem reversa)
    pilha = [vertices_ativos[0]]  # caminho atual, comeca num vertice ativo

    while pilha:
        u = pilha[-1] # topo da pilha
        achou_aresta = False

        while adj[u]:
            v, edge_id = adj[u].pop()

            # ignora aresta ja usada (vista pelo outro extremo)
            if edge_id not in arestas_usadas:
                arestas_usadas.add(edge_id)
                pilha.append(v)  # avanca para o vizinho
                achou_aresta = True
                break

        # sem arestas livres em u: u vai para o circuito e volta ao vertice anterior da pilha
        if not achou_aresta:
            circuito.append(pilha.pop())

    # vertices saem na ordem inversa
    circuito.reverse()

    return circuito


def valida_circuito(G, C): # confere se o circuito comeca e termina no mesmo vertice e usa cada aresta exatamente uma vez
    V, E = G

    # grafo vazio: o unico circuito valido e o vazio
    if len(E) == 0:
        return C == []

    if not C or len(C) < 2:
        return False

    # 1. comeca e termina no mesmo vertice
    if C[0] != C[-1]:
        return False

    # 2. cada aresta usada exatamente uma vez
    # conta as arestas do grafo (sorted faz (1, 2) e (2, 1) serem a mesma)
    arestas_grafo = {}

    for u, v in E:
        aresta = tuple(sorted((u, v)))
        arestas_grafo[aresta] = arestas_grafo.get(aresta, 0) + 1

    # conta as arestas percorridas (pares consecutivos do circuito)
    arestas_circuito = {}

    for i in range(len(C) - 1):
        aresta = tuple(sorted((C[i], C[i + 1])))
        arestas_circuito[aresta] = arestas_circuito.get(aresta, 0) + 1

    # contagens iguais: nenhuma aresta faltou, repetiu ou e inexistente
    return arestas_grafo == arestas_circuito


def sim_nao(valor): # converte booleano em 'sim' ou 'nao'
    return "sim" if valor else "nao"


def relatorio_teste(nome, G, esperado): # executa um teste obrigatorio e mostra obtido x esperado
    V, E = G
    grau_dict = graus(G)
    pares = all(g % 2 == 0 for g in grau_dict.values())
    obtido = euleriano(G)

    print(nome)

    if len(E) == 0:
        print("   Sem arestas: circuito trivial (vazio) por convencao")

    print(f"   Conexo: {sim_nao(conexo(G))} | Graus pares: {sim_nao(pares)} | "
          f"Euleriano: {sim_nao(obtido)} (esperado: {sim_nao(esperado)})")

    passou = (obtido == esperado)

    if obtido:
        C = circuito_euler(G)
        valido = valida_circuito(G, C)
        circ = " -> ".join(map(str, C)) if C else "(vazio)"
        print(f"   Circuito: {circ} | Validacao: {'OK' if valido else 'FALHA'}")
        passou = passou and valido

    print(f"   {'PASSOU' if passou else 'FALHOU'}")

def main():
    n = 10
    p = 0.30
    seed_val = 816

    # experimento 1: busca do primeiro grafo euleriano

    print("\n" + "=" * 50)
    print("EXPERIMENTO 1 - Busca do 1o Grafo Euleriano")
    print("=" * 50 + "\n")

    random.seed(seed_val)
    grafos_gerados = 0

    while True:
        grafos_gerados += 1
        G = gerar_grafo(n, p)

        if euleriano(G):
            break

    V, E = G
    grau_dict = graus(G)
    C = circuito_euler(G)
    valido = valida_circuito(G, C)

    print(f"Numero de vertices: {n}")
    print(f"Probabilidade p: {p:.2f}")
    print(f"Seed: {seed_val}")
    print("Grafo Euleriano encontrado!")
    print(f"Numero de grafos gerados: {grafos_gerados}")

    print(f"Arestas ({len(E)}):")
    print(" ".join([f"({u},{v})" for u, v in E]))

    print("Graus:")
    for v in V:
        print(f"v{v}: {grau_dict[v]}")

    print(f"Conexo: {sim_nao(conexo(G))}")

    todos_pares = all(g % 2 == 0 for g in grau_dict.values())
    print(f"Todos os graus sao pares: {sim_nao(todos_pares)}")

    print(f"Euleriano: {sim_nao(euleriano(G))}")

    print("Circuito de Euler:")
    print(" -> ".join(map(str, C)))

    print(f"Validacao do circuito: {'OK' if valido else 'FALHA'}")

    
    # experimento 2: avaliacao com 1000 grafos

    print("\n" + "=" * 50)
    print("EXPERIMENTO 2 - Avaliacao com 1000 Grafos")
    print("=" * 50 + "\n")

    # seed reiniciada para o experimento ser reproduzivel por si so (a sequencia recomeca igual a do experimento 1)
    random.seed(seed_val)

    # o tempo inclui a geracao e a verificacao dos grafos
    t_inicio = time.perf_counter()
    eulerianos_count = 0

    for _ in range(1000):
        G_temp = gerar_grafo(n, p)

        if euleriano(G_temp):
            eulerianos_count += 1

    t_fim = time.perf_counter()

    tempo_total = t_fim - t_inicio
    proporcao = eulerianos_count / 1000.0

    print(f"Tempo total: {tempo_total:.4f} s")
    print(f"Grafos Eulerianos: {eulerianos_count}")
    print(f"Proporcao: {proporcao:.3f}")

    # testes obrigatorios
    
    print("\n" + "=" * 50)
    print("TESTES OBRIGATORIOS")
    print("=" * 50 + "\n")
    
    # ciclo C4 (conexo e todos os graus pares)
    c4 = ([1, 2, 3, 4], [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 1)
    ])
    relatorio_teste("1. Ciclo C4", c4, esperado=True)
    
    # caminho P4 (conexo, mas possui vertices de grau impar)
    p4 = ([1, 2, 3, 4], [
        (1, 2),
        (2, 3),
        (3, 4)
    ])
    relatorio_teste("2. Caminho P4 (vertices impares)", p4, esperado=False)
    
    # grafo desconexo com duas componentes ciclicas (todos os graus pares, mas desconexo)
    desc = ([1, 2, 3, 4, 5, 6], [
        (1, 2),
        (2, 3),
        (3, 1),
        (4, 5),
        (5, 6),
        (6, 4)
    ])
    relatorio_teste("3. Grafo desconexo (duas componentes ciclicas)", desc, esperado=False)
    
    # grafo vazio
    vazio = ([1, 2, 3, 4], [])
    relatorio_teste("4. Grafo vazio", vazio, esperado=True)


if __name__ == "__main__":
    main()
