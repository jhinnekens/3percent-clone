
from config import *
from .pdfWR import PDF
import pandas as pd
from weasyprint import HTML

class CerfaWriter : 

    def __init__(self,entitie,orga):
        self.pdf = PDF()
        self.entitie = entitie
        self.orga = orga

    def get_node_attr(self,attr,entitie = None,) :
        if entitie is None :
            return self.orga.entitie_attr(self.entitie,attr)
        else :
            return self.orga.entitie_attr(entitie,attr)

    def get_edge_attr(self,entitie,attr):
        return self.orga.G.get_edge_data(self.entitie,entitie)[attr]

    def write_cerfa(self) :
        self.fill_form()
        self.fill_annexe()
        self.pdf.write_pdf()


    def fill_form(self) :

        tab_a = self.orga.compute_share(self.entitie)

        self.pdf.update(
            {'PAGE1_ANNEE' : '2019',
             'PAGE1_DENOMINATION_ENTITEE' : self.entitie + '\n' + self.get_node_attr('Adress'),
             'PAGE1_SIRET' : round(self.get_node_attr('Siret')),
             'PAGE1_VALEUR_VENALE_A_REPORTER' : tab_a,
             'PAGE1_IDENTITE_REPRESENTANT' : "PwC Société d'Avocats (à l'attention de PRENOM NOM)",
             'PAGE1_ADRESSE_LIGNE1' : "Crystal Park 61 Rue de Villiers 92208 Neuilly-sur-Seine Cedex France"
            })

        

        tab_b = round(self.get_node_attr('Number_shares'))
        tab_c = tab_b + 0

        tab_d = 0
        tab_e = tab_c + tab_d

        tab_f = (tab_e*100)/tab_b
        tab_g = tab_f*tab_a
        tab_h = tab_a-tab_g
        tab_i = tab_h*3

    def fill_annexe(self):

        self.fill_annexe_shareolders()


    def fill_annexe_shareolders(self) :

        df = pd.DataFrame(columns=['Raison sociale', 'Adresse','Pays','% de détention'])

        for shareolder in self.orga.children(self.entitie) :

            df = df.append(
                {
                    'Raison sociale' : shareolder + '\n' + str(round(self.get_node_attr('Siret',shareolder))),
                    'Adresse' : self.get_node_attr('Adress',shareolder),
                    'Pays' : self.get_node_attr('Country',shareolder),
                    '% de détention' : str(self.get_edge_attr(shareolder,HOLDING_PERCENTAGE)*100)
                },
                ignore_index=True
            )
        HTML(string=df.to_html()).write_pdf(UPLOAD_FOLDER + '/annexe_shareolders.pdf')
        self.pdf.add_page('annexe_shareolders')


