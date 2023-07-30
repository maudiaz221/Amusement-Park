import psycopg2 as obg
import pandas as pd

conn = obg.connect(host="localhost",dbname="parque",user="postgres",password="cuchara02.",port=5432)

cur = conn.cursor()

#consulta 1
cur.execute(''' select distinct v.nombre
from visitante v, boleto b, atracción a, visita vi
where v.IdVisit=b.IdVisit and b.IdBoleto=vi.IdBoleto and vi.IdArea=a.IdArea
order by v.nombre
''')
resp = cur.fetchall()
df1 = pd.DataFrame(resp,columns = ['nombre'])
print(df1)

nuevo = pd.read_sql_query(''' select distinct v.nombre
from visitante v, boleto b, atracción a, visita vi
where v.IdVisit=b.IdVisit and b.IdBoleto=vi.IdBoleto and vi.IdArea=a.IdArea
order by v.nombre
''',conn)
print('Nueva \n',nuevo)

#consulta 2
cur.execute(''' 
select IdBoleto
from Boleto
''')
resp = cur.fetchall()
df2 = pd.DataFrame(resp)
print(df2)


#consulta 3

cur.execute(''' 
select v.nombre, count(*) "Número de atracciones"
from visitante v, boleto b, atracción a, visita vi
where v.IdVisit=b.IdVisit and b.IdBoleto=vi.IdBoleto and vi.IdArea=a.IdArea
group by v.nombre
order by v.nombre
''')
resp = cur.fetchall()
df3 = pd.DataFrame(resp,columns = ['nombre','atracciones'])
print(df3)


#consulta 4

cur.execute(''' 
select v.idvisit, v.nombre, sum(monto)
from visitante v, boleto b, tienda t, visita vi,venta ve
where v.IdVisit=b.IdVisit and b.IdBoleto=vi.IdBoleto and vi.IdArea=t.IdArea 
	and t.IdArea=ve.IdArea
group by v.idvisit
''')
resp = cur.fetchall()
df4 = pd.DataFrame(resp)
print(df4)


#Hacemos un data frame en base a las consultas,
df1['idBoleto'] = df2
df1['num de atracciones'] = df3['atracciones']
df1['monto'] =[None,None,None,None,None,None]

print('dataFrame final\n', df1)




#cierra la base de datos
conn.commit()
cur.close()
conn.close()

'''
Consultas
select distinct v.nombre
from visitante v, boleto b, atracción a, visita vi
where v.IdVisit=b.IdVisit and b.IdBoleto=vi.IdBoleto and vi.IdArea=a.IdArea
order by v.nombre

select IdBoleto
from Boleto



select v.nombre, count(*) "Número de atracciones"
from visitante v, boleto b, atracción a, visita vi
where v.IdVisit=b.IdVisit and b.IdBoleto=vi.IdBoleto and vi.IdArea=a.IdArea
group by v.nombre

select v.idvisit, v.nombre, sum(monto)
from visitante v, boleto b, tienda t, visita vi,venta ve
where v.IdVisit=b.IdVisit and b.IdBoleto=vi.IdBoleto and vi.IdArea=t.IdArea 
	and t.IdArea=ve.IdArea
group by v.idvisit


'''