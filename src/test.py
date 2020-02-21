
#from app import app

from app.inputFile import InputFile
from config import *
from app.organigramme import Organigramme
import matplotlib.pyplot as plt


input = InputFile("/home/etienne/Documents/Work/Fichier de collecte d'information.xlsx")


input.process()

orga = Organigramme()
orga.build(input)

print(orga.compute_share('LAVA SUD 14 Holdco B.V.'))