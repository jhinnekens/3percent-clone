
from config import *
from .pdfWR import PDF
import pandas as pd
from weasyprint import HTML

class CerfaWriter : 

    def __init__(self,entitie,orga,nom,prenom,email):
        self.pdf = PDF()
        self.entitie = entitie
        self.orga = orga
        self.nom = nom.strip()
        self.prenom = prenom.strip()
        self.email = email.strip()
        self.properties_holding = {}
        total = 0.0

        for propertie in self.orga.properties_shared(self.entitie) :
            holding = self.orga.compute_share_prop(entitie,propertie)
            total = total + holding
            self.properties_holding[propertie] = {
                'Holding' : holding,
                HOLDING_PERCENTAGE : holding/self.orga.G.nodes[propertie][PROPERTIE_VALUE]
            }
        self.total_holding = total
        

    def get_node_attr(self,attr,entitie = None,) :
        if entitie is None :
            return self.orga.entitie_attr(self.entitie,attr)
        else :
            return self.orga.entitie_attr(entitie,attr)

    def get_edge_attr(self,entitie,attr):
        return self.orga.G.get_edge_data(self.entitie,entitie)[attr]

    def fill_pdf(self) : 
        self.fill_form()
        self.fill_annexe()
        return self.pdf.pdf_writer

    def fill_form(self) :

       

        tab_a = self.total_holding
        tab_b = round(self.get_node_attr('Number_shares'))
        tab_c = sum([self.orga.G.edges[(self.entitie,p)][NUMBER_SHARES] for p in self.orga.children(self.entitie)])

        tab_d = tab_b - tab_c
        tab_e = tab_c + tab_d

        try :
            tab_f = (tab_e*100)/tab_b
        except :
            tab_f = 0

        tab_g = (tab_f*tab_a)/100
        tab_h = tab_a-tab_g
        tab_i = tab_h*3

        
        updated_fields =    {

            'PAGE1_ANNEE' : '2020',
            'PAGE1_DENOMINATION_ENTITEE' : self.entitie + '\n' + self.get_node_attr('Adress'),
            'PAGE1_SIRET' : round(self.get_node_attr('Siret')),
            'PAGE1_IDENTITE_REPRESENTANT' : "PwC Société d'Avocats (à l'attention de {} {})".format(self.prenom,self.nom),
            'PAGE1_ADRESSE_LIGNE1' : "Crystal Park 61 Rue de Villiers 92208 Neuilly-sur-Seine Cedex France",
            'PAGE1_EMAIL' : self.email,
            'PAGE1_TEL' : '01 56 57 82 79',
            'PAGE1_ENTITE_INTERPOSEE' : 'Voir Annexe 1 ci-joint',
            'PAGE1_TOTAL_PARTS' : tab_b,
            'PAGE1_VALEUR_VENALE_A_REPORTER' : tab_a,
            'PAGE2_VALEUR_VENALE_A_REPORTER' : tab_a,
            'PAGE2_TOTAL_a' : tab_a,
            'PAGE2_TOTAL_c' : tab_c,
            'PAGE2_TOTAL_d' : tab_d,
            'PAGE2_TOTAL_e' : tab_e,
            'PAGE2_TOTAL_f' : tab_f,
            'PAGE2_TOTAL_g' : tab_g,
            'PAGE2_TOTAL_h' : tab_h,
            'PAGE2_TOTAL_i' : tab_i
            
            }

        self.pdf.update(updated_fields)

    def fill_annexe(self):

        self.fill_annexe_interpose()
        self.fill_annexe_properties()
        self.fill_annexe_shareolders()

    def fill_annexe_interpose(self):
        df = pd.DataFrame(columns=['Raison sociale', 'Adresse','Participation'])

        for entitie in self.orga.get_all_parents(self.entitie) :
            Participation = []
            for child in self.orga.children(entitie) :
                Participation.append("Détenue à {}% par {}".format(self.orga.G.get_edge_data(entitie,child)[HOLDING_PERCENTAGE],child))
            df = df.append(
                {
                    'Raison sociale' : entitie,
                    'Adresse' : self.get_node_attr('Adress',entitie),
                    'Participation' : Participation
                },
                ignore_index=True
            )
        self.pdf.add_page(HTML(string=df.to_html()))

    def fill_annexe_properties(self) :
        DATE = '01/01/2017'
        df = pd.DataFrame(columns=['Adresse', 'CP','Commune','Nature','Surface en m2',
         'Valeur vénale(€) au {}'.format(DATE),'Pourcentage de détention',
         'Valeur vénale(€) au {} rapportée au pourcentage de détention du déclarant'.format(DATE)])

        for propertie in self.orga.properties_shared(self.entitie) :
            node = self.orga.G.nodes[propertie]
            df = df.append(
                {
                    'Adresse' : node['Adress'],
                    'CP' : node['Post_Code'],
                    'Commune' : propertie,
                    'Nature' : node['Nature'],
                    'Surface en m2' : node['Surface'],
                    'Valeur vénale(€) au {}'.format(DATE) : node[PROPERTIE_VALUE],
                    'Pourcentage de détention' : self.properties_holding[propertie][HOLDING_PERCENTAGE],
                    'Valeur vénale(€) au {} rapportée au pourcentage de détention du déclarant'.format(DATE) : self.properties_holding[propertie]['Holding']

                },
                ignore_index=True
            )
        self.pdf.add_page(HTML(string=df.to_html()))

    def fill_annexe_shareolders(self):

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

        #HTML(string=df.to_html()).write_pdf(UPLOAD_FOLDER + '/annexe_shareolders.pdf')
        #self.pdf.add_page('annexe_shareolders')

        self.pdf.add_page(HTML(string=df.to_html()))


