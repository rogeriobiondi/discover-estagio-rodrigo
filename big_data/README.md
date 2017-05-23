# Big Data

### Sobre o Hadoop e comandos comuns.

1. **Hadoop: Componentes e práticas**
-------
1.1. _Comandos do Hadoop_:

 Os comandos usados no ambiente Hadoop, via CLI, para a manipulação dos arquivos no HDSF são similares aos que temos no Linux:

  ```bash
  hadoop fs -ls #lista os arquivos dentro do HDFS
  hadoop fs -put /local_maquina/arquivo.ext /user/seu_usuario/sua_pasta #copia o arquivo local para o HDFS
  hadoop fs -get /user/seu_usuario/seu_arquivo.ext /local_maquina/pasta_local #copia o arquivo do HDFS para a máquina onde está o Hadoop  
  hadoop fs -mkdir /user/pasta_criada #cria a pasta.
  ```
Mais comandos disponíveis no [Guide da Apache](https://hadoop.apache.org/docs/r2.7.1/hadoop-project-dist/hadoop-common/CommandsManual.html)

___

1.2. __O Apache Hive__:

É um framework primeiramente desenvolvido pelo grupo do Facebook para análise de grandes quantidades de dados, executado no ambiente Hadoop, visando aproveitar a o conhecimento de SQL dos desenvolvedores, transformando Querys convencionais  em Jobs MapReduce executadas no cluster do Hadoop. Possibilita a portabilidade de aplicações baseadas em SQL para o Hadoop. Designado para _OLAP (Online Analytical Processing)_, cria uma camada entre o arquivo disponível no HDFS e a Interface do Usuário, através do uso de um Meta Store.
Apesar de aceitar SQL, não se trata de um banco de dados efetivamente. Serve para traduzir o SQL em tarefas MapReduce sobre um arquivo, compactado ou não, a fim de minimizar o tempo de desenvolvimento, visto que você pode obter os mesmos resultados de uma query através de um algoritmo em Java.  

  - *Tabelas*:  
	As tabelas são armazenadas em um arquivo de texto ou em formato binário, caso esteja compactada e dependendo do formato de arquivo que você selecionar e o tipo de tabela. O comando para se criar uma tabela é idêntico ao SQL.
  Exemplo:

  ```SQL
  --Lembre-se que ao criar a tabela, a 'location' definida é onde ficarão armazenados os dados depois de populada a tabela
--O arquivo usado como base é consumido pelo Hive, então será retirado do diretório origem
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

  - *Compactações*:  
	Há dois tipos de compressão para os formatos de arquivos do Hive, o *Snappy*, *GZip* e *LZO*, sendo a primeira mais rápida e co menor taxa de compressão, e a segunda com maior taxa de compressão, mas torna-se mais lenta ao recuperar dados com uma query.
	Os formatos suportados pelo Hive são __Parquet, ORC (Optmized Row Columnar) e AVRO__, e o uso de cada um depende do caso a ser analisado .
	Também existem os formatos textfile, sequentialFile e JSON.
  Presente nos exemplos abaixo e também na apresentação [File Format Benchmarks.ppt](../big_data/Arquivos/File Format Benchmarks.pptx).
  Vale lembrar que os arquivos "split" não suporta compressão, __a não ser a compressão LZO__.
  >O formato ORC não suporta arquivos "split", então não é possível o `STORE AS ORC` quando você tiver feito um import com a tag `--split-by` através do Sqoop.

  [Link interessante sobre File Formats e compressão.](https://acadgild.com/blog/apache-hive-file-formats/)


  - *Particionamento*:  
	A partição é um campo da tabela, usualmente os últimos campos da tabela, que servirá para a separação da tabela e fragmentação dos arquivos. A criação de partições no Hive gera um diretório em que há a separação do arquivo com os dados. Exemplo: se há uma coluna na tabela chamada “setor”, onde há os setores de uma empresa e você faz consultas constantes a ela, a criação de uma partição pode otimizar a busca dos dados; definindo uma partição onde “setor = RH”, ele gerará um diretório “setor=RH” e terá um arquivo separado com as linhas onde o setor é igual ao definido.
  Há dois tipos de particionamento, o *estático* e o *dinâmico*.
	O estático cria partições definidas pelo usuário, e deve ter um comando para cada criação de partição.
  Exemplo:
  ```sql
  CREATE TABLE IF NOT EXISTS partdados_csv (
    uf  string,
    codmundv  int,
    codmun  int,
    nomemunic  string,
    --similar ao exemplo 1
  )
  PARTITIONED BY (coduf int) --pode ser mais de um campo
  ROW FORMAT DELIMITED
  FIELDS TERMINATED BY ';'
  LINES TERMINATED BY '\n'
  STORED AS PARQUET -- Parquet File Format
  TBLPROPERTIES('PARQUET.COMPRESS'='SNAPPY'); --Compressão Snappy para o Parquet.

  --CRIAÇÃO DE UMA PARTIÇÃO ESTÁTICA:
  set hive.mapred.mode = strict; --comando para uso de criação estática apenas;

  insert into table partdados_csv partition(coduf = ' 12') select uf, codmundv, codmun, nomemunic from temp_dados_municipios_csv where coduf = 12;
  --também é possível usar o  LOAD DATA INPATH, e nesse caso deverá ser apenas os dados que casam com a partição
  ```
  Para a partição dinânica é feito outro método, onde você pode usar uma condição de SQL para criar as partições:

  ```sql
  --CRIAÇÃO DE UMA PARTIÇÂO DINAMICA:
  SET hive.exec.dynamic.partition = true;
  SET hive.exec.dynamic.partition.mode = nonstrict;

  insert into table partdados_csv partition (coduf) select * from temp_dados_municipios_csv;
  ```

  >Vale lembrar que não é possível criar uma tabela no formato `CREATE TABLE AS SELECT` não pode ter como alvo uma tabela __particionada__ ou __externa__. Esse comando copia tanto a estrutura da tabela quanto os dados. O comando `CREATE TABLE LIKE` copia apenas a estrutura da tabela.
  ___
  1.3. __Apache Sqoop__

  Trata-se de uma ferramenta para a transferência de dados de alguma base de dados relacional para o HDFS ou diretamente para o Hive __E__ vice-versa. Permite o uso de drivers definidos pelo usuário para criar instâncias do BD e também manipular os Jobs MapReduce. Para ter um bom aproveitamento computacional do Sqoop, atente-se de dividir razoavelmente o trabalho de acordo com a disponibilidade de HardWare que você possui, pois isso está diretamente ligado ao tempo que você levará para transferir o conteúdo. O caso executado, com o cluster da Discover e uma tabela com 54 milhões de linhas será explicado em outro arquivo, bem como os resultados.
  Para acessar, [clique aqui](./sqoop.md).  

  Resumidamente, uma forma prática que você pode usar para visualizar um DB, visualizar tabelas e importar uma tabela (ou todas) é:

  ```bash
  sqoop list-databases --connect jdbc:oracle:thin:<USER>@<host_ip:porta:instancia> --username <user> -P
  #Mostra as DBs presentes no Oracle CASO você tenha a permissão. Senão dará erro: ERROR manager.OracleManager: The catalog view DBA_USERS was not found. This may happen if the user does not have DBA privileges. Please check privileges and try again.

  sqoop list-tables --connect jdbc:oracle:thin:<USER>@<host_ip:porta:instancia> --username <USER> -P

  sqoop import --connect jdbc:oracle:thin:<USER>@<host_ip:porta:instancia> --username <USER> -P --table <'DB'.'TABLE'> --m 8 --split-by 'NOME_COLUNA' --where 'CONDICAO' --target-dir <diretorio_HDFS>
  ```
  A opção `-P` serve para obrigar o usuário a digitar a senha do DB no console, evitando que ela seja passada via texto ou fique salva no console. `--table` faz com que você escolha uma tabela e não será usada no caso do `--import-all-tables`, que importará todas as tabelas. `--target-dir` seleciona um local para inserir os arquivos, dentro do HDFS. `--m` seleciona o número de mappers que irão atuar em paralelo na transferência dos dados (O default é 4). `--split-by <NOME_COLUNA>` uma coluna que servirá de base para o MapReduce, sendo proporcional ao número de mappers. O comando `--where <condição>` fará parte do SQL que será usado para que o Sqoop selecione os dados da tabela. Possível de ver [neste log](./Arquivos/sqoop/log_exemplo1.txt).

  [Relação completa de comandos e sintaxe do Sqoop 1.4.6.](https://sqoop.apache.org/docs/1.4.6/SqoopUserGuide.html)

#####  POR QUESTAO DE SEGURANÇA: SALVE PASSWORDS DE DBs NO HDFS COM A DEVIDA PERMISSÃO

Primeiro abra o terminal e digite `echo -n "A SENHA AQUI" > sqoop.password`, depois mande o arquivo para o diretório com as permissões corretas:

```bash
hadoop fs -put ./sqoop.password /user/rodrigo/pasta_segura
hadoop fs -chmod 400 /user/rodrigo/pasta_segura
```
No Sqoop você deve inserir a opção:
```bash
--password-file ./user/rodrigo/pasta_segura/sqoop.password
```


[Aqui](https://community.hortonworks.com/questions/13781/sqoop-import-with-secure-password.html) há uma explicação de como ciar um password encriptado e usá-lo com o sqoop.


----

  ### Evite erros de forma simples

  * No Sqoop:
    * Caso seu usuário não seja _camel case_, digite tudo em maiúsculo;
    * O mesmo serve para DATABASES e TABLES ou VIEWS;
    * Verifique se você os privilégios necessários para executar as operações;

  * Em geral:
    * Utilize, ao final de um comando em _CLI_ (linha de comando) sempre o desvio de saída `2>&1|tee <arq.log>`. Ele salva o que o programa exibe na tela em um arquivo "<arq.log>". O que pode ser util em situações de erro (o _statement_ padrão é `2> <arq.log>`) e em situações em que tudo ocorre normal ( `1> <arq.log>`). Neste caso o `|tee ` faz com que o CLI também exiba a saída do programa.
  ___
