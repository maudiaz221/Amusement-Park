import psycopg2 as obg
import pandas as pd

conn = obg.connect(host="localhost",dbname="parque",user="postgres",password="cuchara02.",port=5432)

cur = conn.cursor()

#consulta 1
cur.execute(''' select * from boleto
''')
resp = cur.fetchall()
df = pd.DataFrame(resp)
print(df)

#consulta 2


#consulta 3


#consulta 4






#cierra la base de datos
conn.commit()
cur.close()
conn.close()

'''
select distinct v.nombre
from visitante v, boleto b, atracción a, visita vi
where v.IdVisit=b.IdVisit and b.IdBoleto=vi.IdBoleto and vi.IdArea=a.IdArea
order by v.nombre

select IdBoleto
from Boleto
where FechaDeC >= '2023-01-01'


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