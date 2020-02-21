
#### FLASK CONFIG

UPLOAD_FOLDER = 'app/temp/'


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

ENTITIES_MAP = {
    ENTITIES_NODE_INDEX : 0,
    'SIRET' : 2,
    'Number_shares' : 5
}

PROPERTIES_MAP = {
    PROPERTIES_NODE_INDEX : 2,
    PROPERTIE_VALUE : 5,
    ENTITIES_NODE_INDEX : 6
}

SHAREOLDERS_MAP = {
    ENTITIES_NODE_INDEX : 0,
    DIRECT_SHAREOLDER : 1,
    HOLDING_PERCENTAGE : 3
}

#### CERFA CONFIG :



FIELDS_PDF = {
    'Year' : {'length' : 4 , 'type' : 'str', 'index' : 0 , 'value' : None},
    'Siret' : {'length' : 14 , 'type' : 'seq', 'index' : 1 , 'value' : None},
    'Adresse' : {'length' : 100 , 'type' : 'seq', 'index' : 2 , 'value' : None},
    
}

