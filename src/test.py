
#from app import app

from app.inputFile import InputFile
from config import *
#from organigramme import Organigramme


input = InputFile("/home/etienne/Documents/Work/Fichier de collecte d'information.xlsx")

import networkx as nx
G = nx.DiGraph()

input.read_all()

print(input.clean_cols(input.entities))

#properties = input.get_properties()
#shareolders = input.get_shareolders()

#for index,row in entities.iterrows():
#    node_attr = {key:value for key,value in zip(ENTITIES_MAP.keys(),row.iloc[list(ENTITIES_MAP.values())]) if key != ENTITIES_NODE_INDEX}
#    G.add_node(row.iloc[ENTITIES_MAP[ENTITIES_NODE_INDEX]],**node_attr)


#print(G.nodes)

#shareolders = input.read("shareholders information")
#buildings = input.read("Property information")


#organigramme = Organigramme(shareolders,buildings)
#organigramme.build()

#print(organigramme.children('LaSalleValue Add. L.P'))
#print(organigramme.parents('LaSalleValue Add. L.P'))