#Big Data

###Sobre o Hadoop e comandos comuns.

1. **Hadoop: Componentes e práticas**
-------
1.1. Comandos do Hadoop:

  Os comandos usados no ambiente Hadoop, via CLI, para a manipulação dos
  arquivos no HDSF são similares aos que temos no Linux:

  ```bash
  hadoop fs -ls #lista os arquivos dentro do HDFS
  hadoop fs -put /local_maquina/arquivo.ext /user/seu_usuario/sua_pasta #copia o arquivo local para o HDFS
  hadoop fs -get /user/seu_usuario/seu_arquivo.ext /local_maquina/pasta_local #copia o arquivo do HDFS para a máquina onde está o Hadoop  
  hadoop fs -mkdir /user/pasta_criada #cria a pasta.
  ```
Mais comandos disponíveis no [Guide da Apache](https://hadoop.apache.org/docs/r2.7.1/hadoop-project-dist/hadoop-common/CommandsManual.html)

1.2. O Apache Hive:

  É um framework primeiramente desenvolvido pelo grupo do Facebook para análise de grandes quantidades de dados, executado no ambiente Hadoop, visando aproveitar a o conhecimento de SQL dos desenvolvedores, transformando Querys convencionais  em Jobs MapReduce executadas no cluster do Hadoop. Possibilita a portabilidade de aplicações baseadas em SQL para o Hadoop. Designado para OLAP (Online Analytical Processing), cria uma camada entre o arquivo disponível no HDFS e a Interface do Usuário, através do uso de um Meta Store.
  Apesar de aceitar SQL, não se trata de um banco de dados efetivamente. Serve para traduzir o SQL em tarefas MapReduce sobre um arquivo, compactado ou não, a fim de minimizar o tempo de desenvolvimento, visto que você pode obter os mesmos resultados de uma query através de um algoritmo em Java.

  - Tabelas:
	As tabelas são armazenadas em um arquivo de texto ou em formato binário, caso esteja compactada e dependendo do formato de arquivo que você selecionar e o tipo de tabela. O comando para se criar uma tabela é idêntico ao SQL.
  Exemplo:

  ```SQL
  CREATE EXTERNAL TABLE IF NOT EXISTS temp_dados_municipios_csv (
    uf  string,
    coduf  int,
    codmundv  int,
    codmun  int,
    nomemunic  string
    --Demais vars
  )
  ROW FORMAT DELIMITED
  FIELDS TERMINATED BY ';'
  LINES TERMINATED BY '\n'
  STORED AS TEXTFILE LOCATION '/user/rodrigo/Dados/';

  --Para inserir os dados nessa tabela [! o arquivo deve estar no HDFS neste caso !]
  LOAD DATA INPATH '/user/rodrigo/dados_municipios.csv' into table temp_dados_municipios_csv;
  ```

  - Compactações:
	Há dois tipos de compressão para os formatos de arquivos do Hive, o Snappy e o GZip, sendo a primeira mais rápida e co menor taxa de compressão, e a segunda com maior taxa de compressão, mas torna-se mais lenta ao recuperar dados com uma query.
	Os formatos suportados pelo Hive são Parquet, ORC (Optmized Row Columnar) e AVRO, e o uso de cada um depende do caso a ser analisado .
	Também existem os formatos textfile e JSON.
  - Particionamento:
	A partição é um campo da tabela, usualmente os últimos campos da tabela, que servirá para a separação da tabela e fragmentação dos arquivos. A criação de partições no Hive gera um diretório em que há a separação do arquivo com os dados. Exemplo: se há uma coluna na tabela chamada “setor”, onde há os setores de uma empresa e você faz consultas constantes a ela, a criação de uma partição pode otimizar a busca dos dados; definindo uma partição onde “setor = RH”, ele gerará um diretório “setor=RH” e terá um arquivo separado com as linhas onde o setor é igual ao definido.
  Há dois tipos de particionamento, o estático e o dinâmico.
	O estático cria partições definidas pelo usuário, e deve ter um comando para cada criação de partição.
