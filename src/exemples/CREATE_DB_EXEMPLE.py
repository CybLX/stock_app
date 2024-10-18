#%%
import pandas as pd
import sqlite3
from datetime import date, datetime
import os
#%%
dir = './Tabelas/'
at = os.listdir(dir)


db = sqlite3.connect('./invst.db')
cursor = db.cursor()

prefix_to_power = {'K' : 10e3, 'M' : 10e6}
def replace_multiply(value):
    if pd.notna(value):
        prefix = value[-1]
    
        if prefix in prefix_to_power.keys():
            valor_numerico = float(value[:-1])
            value = prefix_to_power[prefix] * valor_numerico
    
    return value

for i in at:
    name = i.split(sep = '.')[0]
    
    cursor.execute(f"""
                        create table {name}(
                        date    DATE    PRIMARY KEY     NOT NULL,
                        last    REAL,
                        first   REAL,
                        max     REAL,
                        min     REAL,
                        vol     INTEGER,
                        var     REAL
                        ) 
""")
    
    ativo = pd.read_csv(dir+i)
    ativo.replace({",":'.'}, regex= True, inplace = True)
    ativo.replace({"%":''}, regex= True, inplace = True)
    ativo['Vol.'] = ativo['Vol.'].apply(replace_multiply)
    ativo.fillna(0, inplace = True)
    ativo['Data'] = pd.to_datetime(ativo['Data'], format = '%d.%m.%Y').dt.date
    ativo = ativo.astype({"Último" : float, "Abertura" : float, 'Máxima' : float, 'Mínima':float,'Vol.' : int, 'Var%': float })
    tuples = list(ativo.itertuples(index = False, name = None))
    for i in tuples:
        cursor.execute(f'insert into {name} (date, last, first, max, min, vol, var) Values (?, ?, ?, ?, ?, ?, ?)', i)
db.commit()
# %%

def replace_multiply(value : str):
    prefix_to_power = {'K' : 10e3, 'M' : 10e6}
    if pd.notna(value):
        if value != "":
            prefix = value[-1]
            if prefix in prefix_to_power.keys():
                valor_numerico = float(value[:-1])
                value = prefix_to_power[prefix] * valor_numerico
        else:
            value = 0
    return value
def tratamento(download):
    download.replace({",":"."}, regex = True, inplace = True)
    download.replace({"%":""}, regex =True, inplace=True)
    download['vol'] = download['vol'].apply(replace_multiply)
    download.fillna(0, inplace = True)
    download['date'] = pd.to_datetime(download['date'], format= '%d.%m.%Y').dt.date
    download = download.astype({'date' : str, "last" : float, "first" : float, 'max' : float, 'min':float,'vol' : int, 'var': float })
    return download


dir = './Tabelas/'
at = os.listdir(dir)



for i in at:
    db = sqlite3.connect('./invst.db')
    name = i.split(sep = '.')[0]
    data = pd.read_csv(dir + i)
    data = data.rename(columns = {"Data" : 'date',
                                  "Último" : 'last',
                                  "Abertura" : 'first',
                                  "Máxima" : 'max',
                                  "Mínima" : 'min',
                                  "Vol." : 'vol',
                                  "Var%" : 'var'})
    
    data = tratamento(download = data)


    hist_collect = pd.read_sql(f"SELECT date FROM '{name}'", db)

    update_checks = []
    for my_date in list(data['date']):
        if my_date in list(hist_collect.date) or my_date == str(date.today()):
            pass
        else:
            update_checks.append(my_date)
    
    if len(update_checks) == 0 :
                print('*'*20 + '\n' + 'SEM ATUALIZACAO de {}'.format(name) + '\n' +  '*'*20)
                db.commit()
    else:
        pack_atualiza = []
        for d in update_checks:
            pack_atualiza.append(data.loc[data['date'] == d])
        atualizado = pd.concat(pack_atualiza, axis=0).sort_values(by = 'date').reset_index(drop = True)
        atualizado = atualizado.set_index('date')
        atualizado.to_sql('{}'.format(name), con = db, if_exists = 'append')
        db.commit()
        print('*'*20 + '\n' + 'ATUALIZADO: {}'.format(name) + '\n' + '*'*20)



# %%
