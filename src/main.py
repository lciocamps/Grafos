import random
import time


def gerar_grafo(n, p):
    """
    Gera aleatoriamente um grafo simples não direcionado com n vértices,
    incluindo cada aresta com probabilidade p.
    """
    V = list(range(1, n + 1))
    E = []

    for i in range(len(V)):
        for j in range(i + 1, len(V)):
            if random.random() < p:
                E.append((V[i], V[j]))

    return V, E


def graus(G):
    """Calcula o grau de cada vértice."""
    V, E = G
    grau_dict = {v: 0 for v in V}

    for u, v in E:
        grau_dict[u] += 1
        grau_dict[v] += 1

    return grau_dict


def conexo(G):
    """
    Verifica se todos os vértices que possuem grau maior que zero
    pertencem à mesma componente conexa (via BFS).
    """
    V, E = G
    grau_dict = graus(G)

    vertices_ativos = [v for v in V if grau_dict[v] > 0]

    if len(vertices_ativos) == 0:
        return True

    adj = {v: [] for v in V}

    for u, v in E:
        adj[u].append(v)
        adj[v].append(u)

    visitados = set()
    inicio = vertices_ativos[0]
    fila = [inicio]
    visitados.add(inicio)

    while fila:
        atual = fila.pop(0)

        for viz in adj[atual]:
            if viz not in visitados:
                visitados.add(viz)
                fila.append(viz)

    for v in vertices_ativos:
        if v not in visitados:
            return False

    return True


def euleriano(G):
    """
    Determina se o grafo possui circuito de Euler utilizando
    os critérios matemáticos:

    1. Vértices com grau > 0 devem estar na mesma componente conexa.
    2. Todos os graus devem ser pares.
    """
    V, E = G
    grau_dict = graus(G)

    # Caso especial: grafo sem arestas. Por convenção, possui circuito
    # de Euler trivial (vazio), mas não há ruas a inspecionar.
    if len(E) == 0:
        return True

    # Critério 1: Conectividade dos vértices de grau não nulo
    if not conexo(G):
        return False

    # Critério 2: Graus pares
    for v in V:
        if grau_dict[v] % 2 != 0:
            return False

    return True


def circuito_euler(G):
    """
    Constrói um circuito de Euler utilizando o
    Algoritmo de Hierholzer.
    """
    V, E = G

    if not euleriano(G):
        return None

    grau_dict = graus(G)
    vertices_ativos = [v for v in V if grau_dict[v] > 0]

    # Grafo vazio: circuito trivial (vazio)
    if not vertices_ativos:
        return []

    # Lista de adjacência com ID único por aresta
    # para suportar remoção correta.
    adj = {v: [] for v in V}

    for idx, (u, v) in enumerate(E):
        adj[u].append((v, idx))
        adj[v].append((u, idx))

    arestas_usadas = set()
    circuito = []
    pilha = [vertices_ativos[0]]

    while pilha:
        u = pilha[-1]
        achou_aresta = False

        while adj[u]:
            v, edge_id = adj[u].pop()

            if edge_id not in arestas_usadas:
                arestas_usadas.add(edge_id)
                pilha.append(v)
                achou_aresta = True
                break

        if not achou_aresta:
            circuito.append(pilha.pop())

    circuito.reverse()

    return circuito


def valida_circuito(G, C):
    """
    Valida automaticamente se o circuito encontrado:

    - Começa e termina no mesmo vértice.
    - Utiliza todas as arestas do grafo exatamente uma vez.
    """
    V, E = G

    # Grafo vazio: o único circuito válido é o circuito trivial (vazio)
    if len(E) == 0:
        return C == []

    if not C or len(C) < 2:
        return False

    # 1. Começar e terminar no mesmo vértice
    if C[0] != C[-1]:
        return False

    # 2. Utilizar cada aresta de E exatamente uma vez
    arestas_grafo = {}

    for u, v in E:
        aresta = tuple(sorted((u, v)))
        arestas_grafo[aresta] = arestas_grafo.get(aresta, 0) + 1

    arestas_circuito = {}

    for i in range(len(C) - 1):
        aresta = tuple(sorted((C[i], C[i + 1])))
        arestas_circuito[aresta] = arestas_circuito.get(aresta, 0) + 1

    return arestas_grafo == arestas_circuito


def sim_nao(valor):
    """Converte um valor booleano em 'sim' ou 'nao'."""
    return "sim" if valor else "nao"


def relatorio_teste(nome, G, esperado):
    """
    Executa um teste obrigatório, exibindo cada critério,
    o resultado obtido e o resultado esperado.
    """
    V, E = G
    grau_dict = graus(G)
    pares = all(g % 2 == 0 for g in grau_dict.values())
    obtido = euleriano(G)

    print(f"\n{nome}")
    print("  Arestas: " + (" ".join(f"({u},{v})" for u, v in E) if E else "(nenhuma)"))
    print("  Graus: " + " ".join(f"v{v}:{grau_dict[v]}" for v in V))
    print(f"  Conexo (vertices de grau nao nulo): {sim_nao(conexo(G))}")
    print(f"  Todos os graus sao pares: {sim_nao(pares)}")
    print(f"  Euleriano: {sim_nao(obtido)} | Esperado: {sim_nao(esperado)}")

    if len(E) == 0:
        print("  Grafo vazio: nao possui arestas; circuito de Euler trivial "
              "(vazio) por convencao, nao ha ruas a inspecionar.")

    if obtido:
        C = circuito_euler(G)
        valido = valida_circuito(G, C)
        print("  Circuito de Euler: " + (" -> ".join(map(str, C)) if C else "(vazio)"))
        print(f"  Validacao do circuito: {'OK' if valido else 'FALHA'}")
        passou = (obtido == esperado) and valido
    else:
        print("  Circuito de Euler: nao existe")
        passou = (obtido == esperado)

    print(f"  Resultado do teste: {'PASSOU' if passou else 'FALHOU'}")


def main():
    n = 10
    p = 0.30
    seed_val = 816

    # ==================================================
    # EXPERIMENTO 1 - Busca do 1º Grafo Euleriano
    # ==================================================

    print("=" * 50)
    print("EXPERIMENTO 1 - Busca do 1o Grafo Euleriano")
    print("=" * 50)

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

    isolados = [v for v in V if grau_dict[v] == 0]
    print(f"Vertices isolados: {isolados if isolados else 'nenhum'}")

    print(f"Conexo (vertices de grau nao nulo): {sim_nao(conexo(G))}")

    todos_pares = all(g % 2 == 0 for g in grau_dict.values())
    print(f"Todos os graus sao pares: {sim_nao(todos_pares)}")

    print(f"Euleriano: {sim_nao(euleriano(G))}")

    print("Circuito de Euler:")
    print(" -> ".join(map(str, C)))

    print(f"Validacao do circuito: {'OK' if valido else 'FALHA'}")

    # ==================================================
    # TESTES OBRIGATORIOS
    # ==================================================

    print("\n" + "=" * 50)
    print("TESTES OBRIGATORIOS")
    print("=" * 50)

    # Teste 1: Ciclo C4 (conexo e todos os graus pares)
    c4 = ([1, 2, 3, 4], [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 1)
    ])
    relatorio_teste("1. Ciclo C4", c4, esperado=True)

    # Teste 2: Caminho P4 (conexo, mas possui vertices de grau impar)
    p4 = ([1, 2, 3, 4], [
        (1, 2),
        (2, 3),
        (3, 4)
    ])
    relatorio_teste("2. Caminho P4 (vertices impares)", p4, esperado=False)

    # Teste 3: Grafo desconexo com duas componentes ciclicas
    # (todos os graus pares, mas desconexo)
    desc = ([1, 2, 3, 4, 5, 6], [
        (1, 2),
        (2, 3),
        (3, 1),
        (4, 5),
        (5, 6),
        (6, 4)
    ])
    relatorio_teste("3. Grafo desconexo (duas componentes ciclicas)", desc, esperado=False)

    # Teste 4: Grafo vazio (tratado explicitamente)
    vazio = ([1, 2, 3, 4], [])
    relatorio_teste("4. Grafo vazio", vazio, esperado=True)

    # ==================================================
    # EXPERIMENTO 2 - Avaliação com 1000 Grafos
    # ==================================================

    print("\n" + "=" * 50)
    print("EXPERIMENTO 2 - Avaliacao com 1000 Grafos")
    print("=" * 50)

    random.seed(seed_val)

    # O tempo medido inclui a geracao e a verificacao dos grafos
    t_inicio = time.perf_counter()
    eulerianos_count = 0

    for _ in range(1000):
        G_temp = gerar_grafo(n, p)

        if euleriano(G_temp):
            eulerianos_count += 1

    t_fim = time.perf_counter()

    tempo_total = t_fim - t_inicio
    proporcao = eulerianos_count / 1000.0

    print(f"Numero de vertices: {n}")
    print(f"Probabilidade p: {p:.2f}")
    print(f"Seed: {seed_val}")
    print(f"Tempo total (geracao + verificacao): {tempo_total:.4f} s")
    print(f"Grafos Eulerianos: {eulerianos_count}")
    print(f"Proporcao: {proporcao:.3f}")


if __name__ == "__main__":
    main()
