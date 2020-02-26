
from app.posgresclient import pgDB
import psycopg2 as ps2
import pandas as pd
import numpy as np

path = "/home/etienne/Documents/Work/Fichier de collecte d'information.xlsx"

db = pgDB()
table = 'Fichier_collecte'


#with open(path, "rb") as f:
#    binaryData = f.read() 

binaryData = open(path, 'rb').read()

#prepareByteaString(binaryData)
#db.drop_table(table)
#db.create_table(table)


#db.insert(table,ID_Client = '123')


#db.create_table('Fichier_collecte')

#db.drop_table('Fichier_collecte')


#db.insert(table,ID_Client = '564' , Fichier_Excel = str(ps2.Binary(binaryData)))
#db.select(table)



a = db.select_where(table,{'ID' : '7'})

df = pd.read_excel(bytes(next(a)[6]) ,  sheet_name = 'Entities information')


print(df['Entity Name'])


