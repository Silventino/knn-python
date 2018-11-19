import csv
import random
import math
import operator 
import pprint
#~ from sklearn.metrics import confusion_matrix

def distanciaEuclidiana(instancia1, instancia2, qntValores):
    distancia = 0
    for x in range(qntValores):

        distancia += pow(float(instancia1[x]) - float(instancia2[x]), 2)
    return math.sqrt(distancia)

def carregarDataSet(nomeDoArquivo, porcentagemTreino, instanciasTreino=[] , instanciasTeste=[], nomes=[]):
    with open(nomeDoArquivo, 'r') as csvfile:
        linhas = csv.reader(csvfile)
        dados = list(linhas)
        for x in range(len(dados)-1):
            if(dados[x][-1] not in nomes):
                nomes.append(dados[x][-1])
            for y in range(4):
                dados[x][y] = float(dados[x][y])
            if random.random() < porcentagemTreino:
                instanciasTreino.append(dados[x])
            else:
                instanciasTeste.append(dados[x])
        print(nomes)

def getKVizinhosMaisProximos(instanciasTreino, instanciaTeste, k):
    distancias = []
    tam = len(instanciaTeste)-1
    for x in range(len(instanciasTreino)):
        distEuclidiana = distanciaEuclidiana(instanciaTeste, instanciasTreino[x], tam)
        distancias.append((instanciasTreino[x], distEuclidiana))
    distancias.sort(key=operator.itemgetter(1))
    
    vizinhosMaisProximos = []
    for x in range(k):
        vizinhosMaisProximos.append(distancias[x][0])
    return vizinhosMaisProximos

def getResultado(vizinhos):
    possiveisClasses = {}
    for x in range(len(vizinhos)):
        response = vizinhos[x][-1]
        if response in possiveisClasses:        # se a classe ja foi votada, incrementa
            possiveisClasses[response] += 1
        else:                                   # senão, coloca ela no dicionario com valor 1
            possiveisClasses[response] = 1
    votosOrdenaos = sorted(iter(possiveisClasses.items()), key=operator.itemgetter(1), reverse=True)
    return votosOrdenaos[0][0]  # o resultado será a classe mais votada
    
def calculaAcuracia(instanciasTeste, predicoes, nomes):
    corretas = 0
    
    matrizConfusao = {}
    for nome in nomes:
        matrizConfusao[nome] = {}
        for n in nomes:
            matrizConfusao[nome][n] = 0



    # matrizConfusao['Iris-versicolor'] = {'Iris-versicolor': 0, 'Iris-setosa': 0, 'Iris-virginica': 0}
    # matrizConfusao['Iris-virginica'] = {'Iris-versicolor': 0, 'Iris-setosa': 0, 'Iris-virginica': 0}
    # matrizConfusao['Iris-setosa'] = {'Iris-versicolor': 0, 'Iris-setosa': 0, 'Iris-virginica': 0}

    for x in range(len(instanciasTeste)):
        matrizConfusao[instanciasTeste[x][-1]][predicoes[x]] += 1
        
        if instanciasTeste[x][-1] == predicoes[x]:
            corretas += 1
    #~ print(corretas)
    
    imprimeMatrizConfusao(matrizConfusao, nomes)
    
    #~ pprint.pprint(matrizConfusao)
    return (corretas/float(len(instanciasTeste))) * 100.0
    
def imprimeMatrizConfusao(matriz, nomes):
    print("\nTabela de Confusao")
    print("======================================================================================")
    print("{:^20}".format(''), end='')
    for nome in nomes:
        print()
        print(" {:^20s}|".format(nome),  end='')
    print()
    print("======================================================================================")
    
    for k in matriz:
        print("{:20s} ".format(k), end = '')
        
        #~ print(str(k) + ": ", end='')
        print('|{:^20d}|{:^20d}|{:^20d}|'.format(matriz[k][nomes[0]], matriz[k][nomes[1]], matriz[k][nomes[2]]))
        #~ print()
    print("======================================================================================")
    print()

def main():
    
    # prepare data
    instanciasTreino = []
    instanciasTeste = []
    nomes = []
    porcentagemTreino = 0.99
    carregarDataSet('spambase.data', porcentagemTreino, instanciasTreino, instanciasTeste, nomes)
    print('Tamanho do treino: ' + str(len(instanciasTreino)))
    print('Tamanho dos testes: ' + str(len(instanciasTeste)))

    
    #~ k = 3
    for i in range(4):
        predicoes = []
        k = (i*2)+1
        print("*****************************************************************************************")
        print("k= " + str(k))
        for x in range(len(instanciasTeste)):
            #~ print(k)
            vizinhos = getKVizinhosMaisProximos(instanciasTreino, instanciasTeste[x], k)
            #~ print(len(vizinhos))
            resultado = getResultado(vizinhos)
            predicoes.append(resultado)
            # print('predição = ' + repr(resultado) + ', resposta correta = ' + repr(instanciasTeste[x][-1]))
        acuracia = calculaAcuracia(instanciasTeste, predicoes, nomes)
        print('Acuraria: ' + str(acuracia) + '%\n')
        
main()

# i = []
# j = []
# carregarDataSet("iris.data", 0.66, i, j)
# print(len(i))
# print(len(j))
