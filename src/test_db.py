
from app.posgresclient import pgDB
import psycopg2 as ps2
import pandas as pd
import numpy as np


path = "/home/etienne/Documents/Work/Fichier de collecte d'information.xlsx"

db = pgDB()

a = db.select_where('Fichier_collecte',{'ID_Creator' : str(1)} ,'ID','Date_creation','ID_Creator')



print({key:value for key,value })

#db.drop_all_table()

#table = 'Cerfa'
#print([e for e in db.select(table)])
#print([e for e in db.show()])



#iterator = db.select(table,'Pdf')

#row = next(iterator)
#row = next(iterator)


#pdf = row['Pdf']

#pdf = bytes(pdf)

#with open("/home/etienne/Documents/Work/test.pdf" ,'wb') as f :
#    f.write(pdf)


#print([e for e in db.select(table)])


#db.create_table(table)

#with open(path, "rb") as f:
#    binaryData = f.read() 


#db.insert(table,Active = True ,Date_creation = 'NOW()' , ID_Client = 122, ID_Associe = 3, ID_Creator = 1, Fichier_Excel = ps2.Binary(binaryData))

#print([e for e in db.select(table)])

#binaryData = open(path, 'rb').read()


#print(str(ps2.Binary(binaryData)))

#prepareByteaString(binaryData)
#db.drop_table(table)
#db.create_table(table)


#db.insert(table,ID_Client = '123')


#db.create_table('Fichier_collecte')

#db.drop_table('Fichier_collecte')


#db.insert(table,ID_Client = 564 , Fichier_Excel = ps2.Binary(binaryData))
#db.select(table)


#a = db.select_where(table,{'ID' : '7'})

#db.select(table)
#df = pd.read_excel(bytes(next(a)[6]) ,  sheet_name = 'Entities information')


#print(df['Entity Name'])


