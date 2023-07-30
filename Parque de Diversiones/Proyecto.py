#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:18:37 2023

@author: gerardo guerrero, mauricio díaz, santiago villaseñor
"""

import bibBD as lector
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psycopg2 as obg


host = 'localhost'
database = 'Parque Diversiones 1.0'
user = 'postgres'
password = 'basesdatos_cd'

conex = lector.conexión(host, database, user, password)

#Consulta: visitas a atracciones en 2022 y 2023

df = lector.consult(conex, '''
select nombre,count(*) as "visitas"
from visitante
join boleto
on boleto.idvisit = visitante.idvisit
where idboleto in(
	select idboleto
	from visita
	where idarea in (
		select idarea
		from atracción) and extract(year from fechadeingreso) = 2022)
group by nombre''')
atrac_22 = df['visitas']

df = lector.consult(conex, '''
select nombre,count(*) as "visitas"
from visitante
join boleto
on boleto.idvisit = visitante.idvisit
where idboleto in(
	select idboleto
	from visita
	where idarea in (
		select idarea
		from atracción) and extract(year from fechadeingreso) = 2023)
group by nombre''')
atrac_23 = df['visitas']

# Datos de ejemplo para las barras
valores = [atrac_22.mean(), atrac_23.mean()]

# Valor de referencia
valor_referencia = np.mean(valores)

indices = np.arange(len(valores))
fig, ax = plt.subplots()

# Crea las barras
ax.bar(indices, valores, align='center', alpha=0.5)

# Crea la barra de referencia
ax.axhline(y=valor_referencia, color='r', linestyle='--', label='Promedio')

# Etiquetas en el eje x
ax.set_xticks(indices)
ax.set_xticklabels(['2022', '2023'])

# Etiquetas y título

ax.set_ylabel('Visitas')
ax.set_title('Visitas a atracciones por año')

# Leyendas
ax.legend()

plt.show()

#Visitas históricas de cada área:
df = lector.consult(conex, '''select nombre, count(*)
from visita b
join Área
on Área.idarea=b.idarea
group by nombre''')
df = df.set_index('nombre')
df = df['count']
print(df)
serie = df
ax = serie.plot.bar()
# Cambiar el nombre de la gráfica
ax.set_title('Visitas históricas')
# Mostrar el gráfico
plt.show()

#Evolución de las ventas anuales
df = lector.consult(conex, '''select sum(monto)
from venta
where extract(year from fecha) = 2023''')
sum23 = df['sum']
sum23 = sum23[0]
print(sum23)
df = lector.consult(conex, '''select sum(monto)
from venta
where extract(year from fecha) = 2022''')
sum22 = df['sum']
sum22 = sum22[0]
print(sum22)
df = lector.consult(conex, '''select sum(monto)
from venta
where extract(year from fecha) = 2021''')
sum21 = df['sum']
sum21 = sum21[0]
print(sum21)

ventas = pd.Series({'2021':sum21,'2022':sum22,'2023':sum23})
ax = ventas.plot()
ax.set_ylabel('Monto')
ax.set_title('Ventas por año')


df = lector.consult(conex, '''
select count(*)
from boleto
where tipo = 'Básico' ''')
bas=df['count']
bas = bas[0]

df = lector.consult(conex, '''
select  count(*)
from boleto
where tipo = 'Premium' ''')
premium=df['count']
premium = premium[0]

serie = pd.Series({'Básico':bas,'Premium':premium})
ax = serie.plot.pie(autopct='%.1f%%')
ax.set_title('Marketshare de cada tipo de boleto')

plt.show()

