# ElasticSearch

1. [Uso com o Hive](#es-hive)

2. [Consulta e criação de índices](#cons-es)

3. [Aggregations & Filters](#es-filters)

Links úteis:
* [Hive & ElasticSearch Integration](https://www.elastic.co/guide/en/elasticsearch/hadoop/current/hive.html)

  * [Configuração](https://www.elastic.co/guide/en/elasticsearch/hadoop/current/configuration.html)


* [ElasticSearch & Hadoop](https://www.elastic.co/blog/elasticsearch-and-hadoop)


______

### <a name='es-hive'></a>Uso com o Hive

1. Baixe o _elasticsearch-hadoopX.X.X.jar_ no site: <https://www.elastic.co/downloads/hadoop>  
2. Deixe disponível em um diretório tanto _"Local"_ quando no HDFS.
3. Através do HUE, vá _Query editor_ do Hive e coloque a linha, que colcoar a localização do Elastic Search para ser utilizado como _Storage Handler_ para o Hive __toda vez que for importar uma tabela__:
  ```SQL
    ADD JAR hdfs:///user/rodrigo/es-hadoop/elasticsearch-hadoop-5.4.0.jar
    ADD JAR /usr/hdp/current/hive-client/lib/commons-httpclient-3.0.1.jar;

  ```
4. Crie uma tabela externa com as configurações da tabela que você deseja exportar:
  ```SQL
  create external table pop_area_es (
coduf int,
uf string,
nomemun string,
area double,
pop int,
pessoa_por_km double
)
comment 'Join de duas tabelas, area e pop'
row format delimited
fields terminated by ','
lines terminated by '\n'
stored by 'org.elasticsearch.hadoop.hive.EsStorageHandler'
TBLPROPERTIES('es.resource' = 'dados/ibge',
            'es.nodes' = '10.100.2.32:9200,10.100.2.33:9200');
--a linha acima, TBLPROPERTIES, retém a configuração que você deseja passar para o ElasticSearch
  ```
  [/\ Configuração /\](https://www.elastic.co/guide/en/elasticsearch/hadoop/current/configuration.html)

_____   
## <a name='cons-es'></a> Consulta e criação de índices.

A linha acima já gerou um _índice_ e um _type_ na linha `'es.resource' = '<índice/type>'`, então neste caso não é necessário criar o índice. Nesse caso _index_ = dados, _type_ = ibge.

Após isso você poderá ver o índice criado na lista de índices do ElasticSearch:  

>http://hdp11.discover.com.br:9200/_cat/indices?v

![Índice](./Arquivos/es_index.png)


_____

## <a name='es-aggr'></a> Aggregations & Filters

[Consultar este link (Aggregations):](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html)

[Este aqui para filtros](https://www.elastic.co/guide/en/elasticsearch/reference/current/_executing_filters.html)
