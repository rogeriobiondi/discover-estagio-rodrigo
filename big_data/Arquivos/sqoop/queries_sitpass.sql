CREATE external TABLE SIM_TESTE (
    NUM_LINHA int,
   	CD_OPERADORA int ,
	NO_OPERADORA string ,
	NR_GARAGEM int ,
	NR_ONIBUS int ,
	NR_CATRACA int ,
	NR_VALIDADOR string ,
	NR_ARQUIVO int ,
	DT_OPERACAO DATE ,
	NR_SERVICO int ,
	NR_SEQ_SERVICO int ,
	NR_MOTORISTA_RTP int ,
	NO_MOTORISTA string,
	CD_CLIENTE_MOTORISTA int,
	DG_CLIENTE_MOTORISTA int,
	DT_INICIO_SERVICO DATE ,
	DT_FIM_SERVICO DATE,
	KM_INICIO_SERVICO int ,
	KM_FIM_SERVICO int ,
	NR_CURSO int ,
	NR_SEQ_CURSO int ,
	CD_GRUPO_TARIFARIO int ,
	DS_GRUPO_TARIFARIO string,
	NR_LINHA int ,
	NO_LINHA string ,
	NR_SUBLINHA int ,
	IN_SENTIDO string ,
	DT_INICIO_CURSO DATE ,
	DT_FIM_CURSO DATE ,
	KM_INICIO_CURSO int ,
	KM_FIM_CURSO int ,
	DT_SAIDA_TERMINAL DATE,
	NR_SEQ_ARQUIVO int,
	DT_VALIDACAO DATE ,
	TP_TECNOLOGIA int ,
	NR_PRODUTO int ,
	NO_PRODUTO string ,
	TP_PRODUTO string ,
	NR_SERIE string,
	NR_INTERNO int,
	NR_FISICO_MICRON string,
	NR_VIA int,
	NO_CLIENTE string,
	CD_CLIENTE int,
	DG_CLIENTE int,
	NO_CLIENTE_TITULAR string,
	CD_CLIENTE_TITULAR int,
	DG_CLIENTE_TITULAR int,
	NR_LOTE int,
	NR_SEQ_TRANSACAO int,
	NR_ITA1 int,
	NR_ITA2 int,
	NR_JETONS_ITA1 int,
	NR_JETONS_ITA2 int,
	TP_VALIDACAO int,
	DT_INICIO_VIAGEM DATE,
	NR_LINHA_PRECEDENTE int,
	DT_EXTREMA_VALIDADE DATE,
	VL_TARIFA int
   )
   ROW FORMAT DELIMITED
   fields terminated BY ","
   LINES TERMINATED BY "\n"
   STORED AS textfile
   LOCATION '/user/rodrigo/SITPASS/'

   --Importando o mês de novembro que está completo
   --mudando o campo DATE para String para evitar o erro ORA-01843
   --do qual ainda não tive solução.

--A query abaixo foi executada para criar a View no Oracle.

   CREATE OR REPLACE VIEW "SITPASS"."SIT_NOV" ("NUM_LINHA", "DIA_VIAGEM", "CD_OPERADORA", "NR_GARAGEM", "NR_ONIBUS", "NR_CATRACA", "NO_MOTORISTA", "KM_INICIO_SERVICO", "KM_FIM_SERVICO", "NR_SEQ_CURSO", "NR_LINHA", "NO_LINHA", "NO_PRODUTO", "TP_PRODUTO", "NR_INTERNO", "NR_FISICO_MICRON", "NO_CLIENTE") AS
   select ROWNUM as NUM_LINHA,
 to_number(to_char(di.DT_OPERACAO, 'yyyymmdd')) as DIA_VIAGEM ,
 -- to_number(to_char(di.DT_OPERACAO, 'dd')) as DIA_VIAGEM ,
 -- to_number(to_char(di.DT_OPERACAO, 'mm')) as MES_VIAGEM ,
 -- to_number(to_char(di.DT_OPERACAO, 'yyyy')) as ANO_VIAGEM ,
 -- to_char(di.DT_OPERACAO, 'YYYY-MM-DD hh24:mm:ss') as DIA_VIAGEM ,
 di.CD_OPERADORA,
 di.NR_GARAGEM,
 di.NR_ONIBUS,
 di.NR_CATRACA,
 di.NO_MOTORISTA,
 di.KM_INICIO_SERVICO,
 di.KM_FIM_SERVICO,
 di.NR_SEQ_CURSO,
 di.NR_LINHA,
 di.NO_LINHA,
 di.NO_PRODUTO,
 di.TP_PRODUTO,
 di.NR_INTERNO,
 di.NR_FISICO_MICRON,
 di.NO_CLIENTE from SIM_DETALHE_INFORMACAO di
 --where DT_OPERACAO>date'2016-10-30' AND DT_OPERACAO<'01/12/16'
 where  to_number(to_char(di.DT_OPERACAO, 'yyyymmdd')) between 20161101 AND 20161131;


--Criei uma tabela mais resumida no hive:

CREATE EXTERNAL TABLE SIM_NOV_TESTE(
NUM_LINHA int,
DIA_VIAGEM timestamp,
CD_OPERADORA int,
NR_GARAGEM int,
NR_ONIBUS INT,
NR_CATRACA int,
NO_MOTORISTA string,
KM_INICIO_SERVICO int,
KM_FIM_SERVICO int,
NR_SEQ_CURSO int,
NR_LINHA int,
NO_LINHA string,
NO_PRODUTO string,
TP_PRODUTO string,
NR_INTERNO int,
NR_FISICO_MICRON string,
NO_CLIENTE string
)
ROW FORMAT delimited
fields terminated by ","
lines terminated by "\n"
STORED AS TEXTFILE
LOCATION '/user/rodrigo/SIT_NOV/'

--Uma tabela interna com dados calculados, comprimida, que será
--base para uma tabela particionada por dia

create table sim_nov
comment 'Tabela com dados calculados da tabela sit_nove_teste'
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as orc
tblproperties ("orc.compress"="SNAPPY") as
select a.*,
a.km_inicio_servico - a.km_fim_servico  as km_rodado,
month(a.dia_viagem) as mes,
day(a.dia_viagem) as dia
from rodrigo_sitpass.sim_nov_teste a
