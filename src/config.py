
from app import app

#### FLASK CONFIG

UPLOAD_FOLDER = app.root_path + '/static/temp'

#### INPUT FILE CONFIG

# MAPING SHEET NAME
SHEET_MAP = {
    'Entities' : 'Entities information',
    'Properties' : 'Property information',
    'Shareolders' : 'shareholders information'
}

# MAPING COLUMNS INDEX AND GIVES THE COLUMN WHICH WILL BE USE AS NODE INDEX IN ORGANIGRAMME

ENTITIES_NODE_INDEX = 'Entitie_name'
PROPERTIES_NODE_INDEX = 'Propertie_name'
PROPERTIE_VALUE = 'Value'
HOLDING_PERCENTAGE = 'Holding_percentage'
DIRECT_SHAREOLDER = 'Direct_shareolder'
NUMBER_SHARES = 'Number_shares'

ENTITIES_MAP = {
    ENTITIES_NODE_INDEX : 0,
    'Siret' : 2,
    'Adress' : 3,
    'Country' : 4,
    NUMBER_SHARES : 5
}

PROPERTIES_MAP = {
    'Adress' : 0,
    'Post_Code' : 1,
    PROPERTIES_NODE_INDEX : 2,
    'Nature' : 3,
    'Surface' : 4,
    PROPERTIE_VALUE : 5,
    ENTITIES_NODE_INDEX : 6
}

SHAREOLDERS_MAP = {
    ENTITIES_NODE_INDEX : 0,
    DIRECT_SHAREOLDER : 1,
    HOLDING_PERCENTAGE : 3,
    NUMBER_SHARES : 4
}

#### CERFA CONFIG :



FIELDS_PDF = {
    'Year' : {'length' : 4 , 'type' : 'seq', 'index' : '(PAGE1_ANNEE)'},
    'Siret' : {'length' : 14 , 'type' : 'seq', 'index' : '(PAGE1_SIRET)'},
    'Report1' : {'length' : 14 , 'type' : 'seq', 'index' : '(PAGE1_VALEUR_VENALE_A_REPORTER)'},
    'IdRepresentant' : {'length' : 100 , 'type' : 'seq', 'index' : '(PAGE1_IDENTITE_REPRESENTANT)'},
    'AdresseLigne' : {'length' : 100 , 'type' : 'seq', 'index' : '(PAGE1_ADRESSE_LIGNE1)'},
    'Denomination_entite' : {'length' : 100 , 'type' : 'seq', 'index' : '(PAGE1_DENOMINATION_ENTITEE)'}
}

