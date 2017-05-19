# Hive: SQL
----
#### _Nesta seção irei adicionar os comandos de SQL que usei no Hive para tratar com as tabelas_.

Depois de importar a tabela com os dados do mês de novembro, criei mais uma tabela, adicionando os campos _dia, mes e km rodado_.

```sql
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
```

Depois criei mais tabelas com contagens para dados relevantes:

>Seleciondo o dia com as viagens.

```sql
create table sim_nov_viagens as
select dia_viagem , count(*) as viagens from sim_nov group by dia_viagem order by dia_viagem desc
```

>Os ônibus com mais viagens   

```sql
create table sim_nov_sonibus as
select nr_onibus as numero_onibus , count(*) as viagens from sim_nov group by nr_onibus order by viagens desc
```
>Motoristas com mais viagens  

```sql
create table sim_nov_moto as
select no_motorista as nome_motorista , count(*) as viagens from sim_nov group by no_motorista order by viagens desc

```
