
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

ENTITIES_MAP = {
    'Name' : 0,
    'SIRET' : 2,
    'Number_shares' : 5
}

PROPERTIES_MAP = {
    'City' : 2,
    'Value' : 5,
    'Direct_owner' : 6
}

SHAREOLDERS_MAP = {
    'Name' : 0,
    'Direct_shareolder' : 1,
    'Holding_percentage' : 3
}

ENTITIES_NODE_INDEX = 'Name'
PROPERTIES_NODE_INDEX = 'City'

#### CERFA CONFIG :

FIELDS_PDF = {
    'year' : {'length' : 4 , 'type' : 'str', 'index' : 0},
    'siret' : {'length' : 14 , 'type' : 'seq', 'index' : 1}
}