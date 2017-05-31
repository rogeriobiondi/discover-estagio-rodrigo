from pyspark.sql import Row, Column, DataFrame, DataFrameNaFunctions
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import IntegerType
from pyspark.sql.types import StringType
from pyspark.sql.types import FloatType

dados = sc.textFile("hdfs://hdp9.discover.com.br:8020/user/rodrigo/Dados-IBGE/*") # Carrega arquivo do HDFS
dados.first() # Traz a primeira linha
dados.take(10) # Traz as primeiras 10 linhas
linhas = dados.map(lambda linha: linha.split(";")) # Quebra a linha do CSV em um array
objetos_linhas = linhas.map(lambda s: Row(cod=int(s[0]), cod_regiao=int(s[1]), nome=str(s[2].encode('utf-8').strip()), uf=str(s[3].encode('utf-8').strip()), pop=int(s[4]), cidade=str(s[5].encode('utf-8').strip()), populacao=float(s[6])))


## Exemplo de filtro
def filtrar(a):
  return (a["cidade"] == "ALTA FLORESTA D'OESTE")

dados_filtrados = objetos_linhas.filter(filtrar)
linhasCSV = dados_filtrados.map(lambda l: str(l[0]) + ";" + str(l[1]) + ";" + str(l[2])+ ";" + str(l[3])+ ";" + str(l[4])+ ";" + str(l[5])+ ";" + str(l[6]) + "\n" )
linhasCSV.saveAsTextFile("hdfs://hdp9.discover.com.br:8020/user/discover/teste")

# SQL
fields = [StructField("cod", IntegerType(), True), \
          StructField("cod_regiao", IntegerType(), True), \
          StructField("nome", StringType(), True), \
          StructField("uf", StringType(), True),
          StructField("pop", IntegerType(), True),
          StructField("cidade", StringType(), True),
          StructField("populacao", FloatType(), True) ]

schemaIBGE = StructType(fields)

df = sqlContext.createDataFrame(objetos_linhas, schemaIBGE)

sqlContext.registerDataFrameAsTable(df, "dados_ibge")

query = sqlContext.sql("select * from dados_ibge")

query.collect()


# SparkSQL

tabela = sqlContext.sql("SELECT * FROM rodrigo.pop_area")
tabela.collect()
tabela.count()
