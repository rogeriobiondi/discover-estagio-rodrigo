CREATE EXTERNAL TABLE IF NOT EXISTS temp_dados_municipios_csv (
	uf  string,
	coduf  int,
	codmundv  int,
	codmun  int,
	nomemunic  string,
	var01  int,
	var02  string,
	var03  string,
	var04  int,
	var05  int,
	var06  int,
	var07  int,
	var08  int,
	var09  int,
	var10  int,
	var11  int,
	var12  int,
	var13  double,
	var14  double,
	var15  int,
	var16  int,
	var17  int,
	var18  int,
	var19  int,
	var20  int,
	var21  int,
	var22  int,
	var23  int,
	var24  int,
	var25  int,
	var26  int,
	var27  int,
	var28  int,
	var29  int,
	var30  int,
	var31  int,
	var32  int,
	var33  int,
	var34  int,
	var35  int,
	var36  int,
	var37  int,
	var38  int,
	var39  int,
	var40  int,
	var41  int,
	var42  int,
	var43  int,
	var44  int,
	var45  int,
	var46  int,
	var47  int
  )
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
STORED AS TEXTFILE LOCATION '/user/rodrigo/Dados-IBGE/';
--Cria a tabela inicial;

LOAD DATA INPATH '/user/rodrigo/dados_municipios.csv' into table temp_dados_municipios_csv;
--carrega os dados

--Tabela de população por municipio
create table rodrigo.temp_pop_mun
comment 'Parquet Snappy data loaded from temp_dados_municipios_csv'
row format delimited
fields terminated by ';'
lines terminated by '\n'
stored as parquet as
select nomemunic as city, var01 as pop, uf as state from dados_municipios_orc;

--Tabela com Join das tabelas de população e área;
create table pop_area
comment 'Join de duas tabelas, area e pop'
row format delimited
fields terminated by ';'
lines terminated by '\n'
stored as parquet
tblproperties('parquet.compress'='snappy') as
select b.*, a.var01 as pop, (b.area/a.var01) as pessoa_por_km from dados_municipios_orc a inner join area_mun_comp b ON (a.nomemunic = b.nomemun)
