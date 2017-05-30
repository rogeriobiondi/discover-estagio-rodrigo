#Teste feito com Python - 'Triângulo de Pascal'
import time
import sys
import os


def converter_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "{0:3.3f} {1}s".format(num, x)
        num /= 1024.0


def tamanho_arq(caminho):

    if os.path.isfile(caminho):
        info = os.stat(caminho)
        return converter_bytes(info.st_size)


start_time = 0.0
arq = open('./resultado.txt', 'w+')
tam = 0

def trianguloPascal(n):
    start_time = time.clock()
    lista = [[1], [1, 1]]
    for i in range(1, n):
        linha = [1]
        for j in range(0, (len(lista[i]))-1):
            linha += [lista[i][j] + lista[i][j+1]]
        linha += [1]
        lista += [linha]
    return lista

n = input("Digite o numero de linhas para o triângulo de Pascal (2000 linhas gerou um arquivo de 500MB!):")
resultado = trianguloPascal(int(n))

for i in range(len(resultado)):
    print(resultado[i], file=arq)

print("\n >>Tempo de execução do programa: " + str(time.clock() - start_time))
print("\n >>Tempo de execução do programa: " + str(time.clock() - start_time) , file=arq)
print("\n >>Tamanho do arquivo gerado: " +  tamanho_arq('./resultado.txt'))

arq.close()