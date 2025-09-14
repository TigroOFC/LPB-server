import sys
import time

variaveis = {}
funcoes = {}

def avaliar_expressao(expr):
    expr = expr.strip()
    # Substituir variáveis conhecidas
    for var in variaveis:
        expr = expr.replace(var, str(variaveis[var]))
    try:
        return eval(expr)
    except:
        return expr.strip('"')

def mostrar(*args):
    resultado = ""
    for arg in args:
        if arg in variaveis:
            resultado += str(variaveis[arg])
        else:
            resultado += str(arg).strip('"')
        resultado += " "
    print(resultado.strip())

def executar_bloco(linhas):
    i = 0
    while i < len(linhas):
        linha = linhas[i].strip()
        if linha == "" or linha.startswith("--"):
            i += 1
            continue

        # Declarar variável
        if linha.startswith("variavel "):
            _, resto = linha.split("variavel ", 1)
            nome, valor = resto.split("=", 1)
            variaveis[nome.strip()] = avaliar_expressao(valor.strip())

        # Mostrar
        elif linha.startswith("mostrar("):
            conteudo = linha[len("mostrar("):-1].strip()
            partes = []
            temp = ""
            dentro_aspas = False
            for c in conteudo:
                if c == '"':
                    dentro_aspas = not dentro_aspas
                    temp += c
                elif c == " " and not dentro_aspas:
                    if temp != "":
                        partes.append(temp)
                        temp = ""
                else:
                    temp += c
            if temp != "":
                partes.append(temp)
            mostrar(*partes)

        # Incremento ou decremento sem espaço
        elif any(op in linha for op in ["+1", "-1", "+2", "-2", "*2", "/2", "%2"]):
            nome = linha.split("=")[0].strip()
            expr = linha.split("=")[1].strip()
            expr_valor = avaliar_expressao(expr)
            variaveis[nome] = expr_valor
            if "(esperar " in linha:
                try:
                    tempo = linha.split('(esperar "')[1].split('"')[0]
                    time.sleep(float(tempo))
                except:
                    pass

        # Se / Senao
        elif linha.startswith("se "):
            cond = linha[3:].split("faça")[0].strip()
            bloco = []
            i += 1
            while i < len(linhas) and linhas[i].strip() != "fim" and not linhas[i].strip().startswith("senao"):
                bloco.append(linhas[i])
                i += 1
            if avaliar_expressao(cond):
                executar_bloco(bloco)
                while i < len(linhas) and linhas[i].strip() != "fim":
                    i += 1
            elif i < len(linhas) and linhas[i].strip().startswith("senao"):
                i += 1
                bloco_senao = []
                while i < len(linhas) and linhas[i].strip() != "fim":
                    bloco_senao.append(linhas[i])
                    i += 1
                executar_bloco(bloco_senao)

        # Enquanto
        elif linha.startswith("enquanto "):
            cond = linha[len("enquanto "):].split("faça")[0].strip()
            bloco = []
            i += 1
            while i < len(linhas) and linhas[i].strip() != "fim":
                bloco.append(linhas[i])
                i += 1
            while avaliar_expressao(cond):
                executar_bloco(bloco)

        # Funções
        elif linha.startswith("função "):
            nome = linha[len("função "):].split("(")[0].strip()
            bloco = []
            i += 1
            while i < len(linhas) and linhas[i].strip() != "fim":
                bloco.append(linhas[i])
                i += 1
            funcoes[nome] = bloco

        # Chamada de função
        elif linha.endswith("()"):
            nome = linha[:-2].strip()
            if nome in funcoes:
                executar_bloco(funcoes[nome])
            else:
                raise ValueError(f"Função '{nome}' não existe")

        i += 1

def executar_lpb(codigo):
    linhas = codigo.split("\n")
    executar_bloco(linhas)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: LPB_interpretador.exe arquivo.lpb")
        sys.exit()
    nome_arquivo = sys.argv[1]
    with open(nome_arquivo, "r", encoding="utf-8") as f:
        codigo = f.read()
    executar_lpb(codigo)
