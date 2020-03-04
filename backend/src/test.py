
#from app import app

from app.inputFile import InputFile
from app.cerfawriter import CerfaWriter
from config import *
from app.organigramme import Organigramme
import networkx as nx


inputF = InputFile("/home/etienne/Documents/Work/Fichier de collecte d'information.xlsx")
entitie = 'LAVA SUD 14 Holdco B.V.'

inputF.process()

orga = Organigramme()
orga.build(inputF)


orga.draw()

#print([e for e in paths[0]])
#print([e for e in paths[1]])

#output = CerfaWriter(entitie = 'LAVA SUD 14 Holdco B.V.',orga = orga)

#print(orga.compute_share('LAVA SUD 14 Holdco B.V.'))

#print(orga.G.get_edge_data(entitie,'Lava Dutch Holdco BV'))
#print(orga.children(entitie))

#output.write_cerfa()

#### Test PDF ####


#input.write_cerfa()