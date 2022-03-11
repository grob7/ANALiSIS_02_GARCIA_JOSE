#%%
#PROYECTO 2 
## SYNERGY LOGISTICS 

# Reporte de estrategia operativa

# Jóse Roberto García Ramos

#Opción 1) Rutas de importación y exportación. 

#Opción 2) Medio de transporte utilizado.

#Opción 3) Valor total de importaciones y exportaciones.




import pandas as pd


#%%
#Que transa vamos a empezar
synergydb = pd.read_csv('synergy_logistics_database.csv', index_col = 0, parse_dates = [5])
#%%
#Por la naturaleza de economica de Synergy Logistics debemos filtrar si es una importacion o una exportacion
x = synergydb[synergydb['direction']== 'Exports']
m = synergydb[synergydb['direction']== 'Imports']
#%%
## 1 Rutas de importación y exportación
#Synergy logistics está considerando la posibilidad de enfocar sus esfuerzos en las 10 rutas más
#demandadas. Acorde a los flujos de importación y exportación, ¿cuáles son esas
#10 rutas? ¿le conviene implementar esa estrategia? ¿porqué? 

#Se genera un cálculo general de rutas para exportaciones e importaciones, para poder comparar el valor total
routes = synergydb.groupby(['direction','origin','destination','transport_mode'])
suma = routes.sum()['total_value']
#Se realiza .describe() para poder agregar la suma y tener el count (cuántas veces se usaron)
routes = routes['total_value'].describe()
routes['suma_total'] = suma
routes = routes.reset_index()
#%%
#Se calcula el Top 10 de las rutas más demandadas para exportaciones
#rutas de exportaciones
routes_x = routes[routes['direction']=='Exports']
top_routesx= routes_x.sort_values(by='count',ascending=False).head(10)

#%%
#rutas de importaciones
routes_m = routes[routes['direction']=='Imports']
top_routesm= routes_m.sort_values(by='count',ascending=False).head(10)

#%%
#porcentaje de ingresos por concepto importaciones y exportaciones
# rutas exportaciones o rutas importaciones
def t_i_r(database,top=10):
    #Se genera la información de el valor total
    suma_tot_database= database['suma_total'].sum()
    topusos= database.sort_values(by='suma_total', ascending=False).head(top)
    suma_tot_top= topusos['suma_total'].sum()

    #Se asocia un porcentaje del valor total al top elegido
    total_usos= topusos['count'].sum()
    porcent= (suma_tot_top/suma_tot_database)*1000
    porcent=int(porcent)/100

    print(f'Las {top} rutas más demandadas, aportan el {porcent}% de los ingresos.\nTotal de servicios prestados:{total_usos}')

t_i_r(routes_x,10)
t_i_r(routes_m,10)
#%%
## 2 Medio de transporte utilizado
#Con base en las importaciones y las exportaciones 
#¿Cuáles son los 3 medios de transporte #más importantes para Synergy logistics considerando el valor de las
#importaciones y exportaciones? 
#¿Cuál es medio de transporte que podrían reducir? 

#%%
#Con exportaciones agrupamos por el medio de transporte
transport_x = x.groupby(['transport_mode'])
#Esta variable cuenta las veces que cada transporte fue utilizado
top_transp_x = transport_x.count()['total_value']
top_transp_x=top_transp_x.reset_index()

#Usamos una variable que tenga el acumulado de ventas por cada transporte
income=transport_x['total_value'].sum()
income=income.reset_index()

#Agregamos al transporte y los ingresos generadas
top_transp_x['ingresos']=income['total_value']
top_transp_x['ingresos*10e-9']=round((top_transp_x['ingresos']*0.000000001),2)
top_transp_x = top_transp_x.sort_values('total_value',ascending=False).head()

#verificamos que porcentaje de ingresos representa cada transporte
top_income=top_transp_x['ingresos'].sum()
top_transp_x['porcentaje_gan']=round((top_transp_x['ingresos']/top_income)*100,2)
top_transp_x=top_transp_x.sort_values('porcentaje_gan',ascending=False).head()
top_transp_x['%acumulado_gan']=top_transp_x.cumsum()['porcentaje_gan']

top_transp_x=top_transp_x.sort_values('total_value',ascending=False).head()
top_transp_x


#%%
#Con importaciones agrupamos por el medio de transporte
transport_m = m.groupby(['transport_mode'])
#Esta variable cuenta las veces que cada transporte fue utilizado
top_transp_m = transport_m.count()['total_value']
top_transp_m = top_transp_m.reset_index()

#Usamos una variable que tenga el acumulado de ventas por cada transporte
income_m=transport_m['total_value'].sum()
income_m=income_m.reset_index()

#Agregamos al transporte los ingresos generadas
top_transp_m['ingresos']=income_m['total_value']
top_transp_m['ingresos*10e-9']=round((top_transp_m['ingresos']*0.000000001),2)
top_transp_m = top_transp_m.sort_values('total_value',ascending=False).head()

#verificamos que porcentaje de ingresos representa cada transporte
inc_m=top_transp_m['ingresos'].sum()
top_transp_m['porcentaje_gan']=round((top_transp_m['ingresos']/inc_m)*100,2)
top_transp_m=top_transp_m.sort_values('porcentaje_gan',ascending=False).head()
top_transp_m['%acumulado_gan']=top_transp_m.cumsum()['porcentaje_gan']

top_transp_m=top_transp_m.sort_values('total_value',ascending=False).head()
top_transp_m

#%%
## 3 Valor total de importaciones y exportaciones
#Si Synergy Logistics quisiera enfocarse en los países que generan el 
# 80% de sus ingresos por importaciones y exportaciones


#¿En qué grupo de países debería enfocar sus esfuerzos?

#EXPORTACIONES
#Generamos la suma total de ingresos para exportaciones
t_x=x['total_value'].sum()
#Asignamos un porcentaje de aportación a cada exportación a la ganancia total
incomeee_x = x.groupby(['origin'])
incomee_x= incomeee_x.sum()['total_value']
incomee_x=incomee_x.reset_index()
#Esta variable cuenta las veces que cada transporte fue utilizado 
incomee_x['porcentaje']=round((incomee_x['total_value']/t_x)*100,2)
incomee_x=incomee_x.sort_values('porcentaje',ascending=False).head(20)
incomee_x['% acumulado']=incomee_x.cumsum()['porcentaje']
#%%
#IMPORTACIONES
#Generamos la suma total de ingresos para exportaciones
t_m=m['total_value'].sum()
#Asignamos un porcentaje de aportación a cada exportación a la ganancia total
incomeee_m = m.groupby(['origin'])
incomee_m= incomeee_m.sum()['total_value']
incomee_m=incomee_m.reset_index()
#Esta variable cuenta las veces que cada transporte fue utilizado 
incomee_m['porcentaje']=round((incomee_m['total_value']/t_m)*100,2)
incomee_m=incomee_m.sort_values('porcentaje',ascending=False).head(20)
incomee_m['% acumulado']=incomee_m.cumsum()['porcentaje']
incomee_m.to_excel('Vt_mortaciones.xlsx')
incomee_m
t_m