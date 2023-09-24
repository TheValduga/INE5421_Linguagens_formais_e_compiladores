def formatarTransicoes(t, e, a):
    te = []
    for k in range(0, len(e)):
        for q in range(0, len(a)):
            if t[k][q] != "-":
                s = e[k] + "," + a[q] + "," + t[k][q]
                te.append(s)
    te = sorted(te)
    te = ";".join(te)
    return te


def check_inalcancaveis(start, e, a, t, marked):
    if start not in marked:
        marked.append(start)
        x = e.index(start)
        for k in range(0, len(a)):
            if t[x][k] not in marked:
                fk = check_inalcancaveis(t[x][k], e, a, t, marked)
                for h in range(0, len(fk)):
                    if fk[h] not in marked:
                        marked.append(fk[h])
    return marked


def check_mortos(e, a, t, f, marked):
    for k in range(0, len(f)):
        if f[k] not in marked:
            marked.append(f[k])
    size_marked = len(marked)
    for p in range(0, size_marked):
        start = marked[p]
        for y in range(0, len(e)):
            if e[y] != start:
                for q in range(0, len(a)):
                    if (t[y][q] in marked) and (e[y] not in marked):
                        marked.append(e[y])
    if len(marked) > size_marked:
        fk = check_mortos(e, a, t, f, marked)
        for r in range(0, len(fk)):
            if fk[r] not in marked:
                marked.append(fk[r])
    return marked


def check_equivalencia(G, t, e, a):
    properties = []
    for k in range(0, len(e)):
        state = e[k]
        line = []
        for p in range(0, len(G)):
            if state in G[p]:
                line.append(p)
        for y in range(0, len(a)):
            for q in range(0, len(G)):
                if t[k][y] in G[q]:
                    line.append(q)
        properties.append(line)
    ngp = []
    for z in range(0, len(properties)):
        if properties[z] not in ngp:
            ngp.append(properties[z])
    new_Grupos = []
    for h in range(0, len(ngp)):
        new_group = []
        for m in range(0, len(e)):
            if ngp[h] == properties[m]:
                new_group.append(e[m])
        new_Grupos.append(new_group)
    retorna = new_Grupos
    if new_Grupos != G:
        retorna = check_equivalencia(new_Grupos, t, e, a)
    return retorna

def criarTabela(e, a, t):
    tabela = []
    for z in range(0, len(e)):
        temp1 = e[z]
        linha = []
        for p in range(0, len(a)):
            temp2 = a[p]
            track = 0
            for y in range(0, len(t)):
                if t[y][0] == temp1:
                    if t[y][1] == temp2:
                        linha.insert(p, t[y][2])
                        track = 1
            if track == 0:
                linha.insert(p, "-")
        tabela.append(linha)
    return tabela





def Retirar_Redundancias(e, n_e, a, t, f, s):
    c_t = t
    for k in range(0, len(n_e)):
        replace = []
        is_final = False
        is_start = False
        if len(n_e[k]) > 1:
            leader = n_e[k][0]
            if leader not in f:
                is_final = False
            if leader not in s:
                is_start = False
            for y in range(1, len(n_e[k])):
                replace.append(n_e[k][y])
                if n_e[k][y] in f:
                    is_final = True
                if n_e[k][y] in s:
                    is_start = True
            if is_final and (leader not in f):
                f.append(leader)
            if is_start and (leader != s):
                s = leader
            for q in range(0, len(e)):
                if e[q] in replace:
                    e[q] = leader
                for c in range(0, len(a)):
                    if c_t[q][c] in replace:
                        c_t[q][c] = leader
            for h in range(0, len(f)):
                if f[h] in replace:
                    f[h] = leader
    final_t = []
    for m in range(0, len(e)):
        if c_t[m] not in final_t:
            final_t.append(c_t[m])
    return final_t


if __name__ == '__main__':
    entrada = input().split(";")
    inicial = entrada[1]
    final = entrada[2]
    final = sorted(final[1:-1].split(","))
    alfabeto = entrada[3]
    origin_alfabeto = entrada[3]
    alfabeto = alfabeto[1:-1].split(",")
    estados = [inicial]
    for o in range(0, len(final)):
        if final[o] not in estados:
            estados.append(final[o])
    transicao = []
    for i in range(4, len(entrada)):
        temp = entrada[i].split(",")
        origin = temp[0]
        destination = temp[2]
        if origin not in estados:
            estados.append(origin)
        if destination not in estados:
            estados.append(destination)
        if temp not in transicao:
            transicao.append(temp)
    estados = sorted(estados)
    tabela_de_transicao = criarTabela(estados, alfabeto, transicao)
    temp_alcancaveis = check_inalcancaveis(inicial, estados, alfabeto, tabela_de_transicao, [])
    alcancaveis = []
    for w in range(0, len(estados)):
        if estados[w] in temp_alcancaveis:
            alcancaveis.append(estados[w])
        else:
            tabela_de_transicao[w] = ["null"]
    temp_tt1 = []
    for g in range(0, len(tabela_de_transicao)):
        if tabela_de_transicao[g] != ["null"]:
            temp_tt1.append(tabela_de_transicao[g])
    tabela_de_transicao = temp_tt1
    temp_vivos = check_mortos(alcancaveis, alfabeto, tabela_de_transicao, final, [])
    vivos = []
    mortos = []
    for n in range(0, len(alcancaveis)):
        if alcancaveis[n] in temp_vivos:
            vivos.append(alcancaveis[n])
        else:
            mortos.append(alcancaveis[n])
            tabela_de_transicao[n] = ["null"]
    for x1 in range(0, len(tabela_de_transicao)):
        if tabela_de_transicao[x1][0] != "null":
            for y1 in range(0, len(alfabeto)):
                if tabela_de_transicao[x1][y1] in mortos:
                    tabela_de_transicao[x1][y1] = "-"
    temp_tt2 = []
    for v in range(0, len(tabela_de_transicao)):
        if tabela_de_transicao[v] != ["null", "null"]:
            temp_tt2.append(tabela_de_transicao[v])
    tabela_de_transicao = temp_tt2
    KmenosF = []
    for j in range(0, len(vivos)):
        if vivos[j] not in final:
            KmenosF.append(vivos[j])
    Grupos = [final, KmenosF]
    novos_estados = check_equivalencia(Grupos, tabela_de_transicao, vivos, alfabeto)
    tt_final = Retirar_Redundancias(vivos, novos_estados, alfabeto, tabela_de_transicao, final, inicial)
    print(vivos)
    print(alfabeto)
    print(tt_final)
    e_final = []
    for px in range(0, len(vivos)):
        if vivos[px] not in e_final:
            e_final.append(vivos[px])
    f_final = []
    for py in range(0, len(final)):
        if final[py] not in f_final:
            f_final.append(final[py])
    f_final = sorted(f_final)
    numero_e = len(e_final)
    trans_format = formatarTransicoes(tt_final, e_final, alfabeto)
    final_format = "{" + ",".join(f_final) + "}"
    resultado = str(numero_e) + ";" + inicial + ";" + final_format + ";" + origin_alfabeto + ";" + trans_format
    print(resultado)
