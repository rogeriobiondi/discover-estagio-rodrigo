#Fazer a abertura de um arquivo e contar as palavras repetidas desse arquivo (que está no HDFS do ambiente Hadoop):
dados = sc.textFile("hdfs://hdp9.discover.com.br:8020/user/rodrigo/Dados-IBGE/*") # Carrega arquivo do HDFS
dados.count() #Conta o número de linhas

contador = dados.flatMap(lambda line: line.split(';'))\
            .map(lambda palavra: (palavra,1))\
            .reduceByKey(lambda a,b: a+b)

contador.takeOrdered(100, key=lambda x: -x[1])

#------------------------------------------------------
#Filtragem
dados = sc.textFile("hdfs://hdp9.discover.com.br:8020/user/rodrigo/Dados-IBGE/*")
  #Uso um map que devolve um array com os campos através do .map()
linhas = dados.map(lambda linha: linha.split(";"))
  #aqui eu crio um objeto para poder usar o filtro mais facilmente

'''teste de como montar um obj sem sqlContext
def cria_obj(obj, quant):#função que seleciona o objeto de enttrada e transfoma num dicionário
    obj_saida = [[]]
    lines = obj.take(quant)
    for i in range(quant):
        k = 0
        for j in ['num_linha','cod-uf','estado','uf','cod','municipio','area']:
            obj_saida.append({j:lines[i][k]})
            k = k+1
    return obj_saida
'''
#Crio uma 'ROW' do sqlContext
objeto = linhas.map(lambda campo: Row(num_linha=int(campo[0]), cod_regiao=int(campo[1]), estado=str(campo[2].encode('utf-8').strip()), uf=str(campo[3].encode('utf-8').strip()), cod=int(campo[4]), cidade=str(campo[5].encode('utf-8').strip()), area=float(campo[6])))

)
