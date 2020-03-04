from config import *
from .pdfWR import PDF
import pandas as pd
import math

class InputFile :

    def __init__(self,path) :
        """[summary]
        
        Arguments:
            path {[type]} -- [description]
        """
        self.path = path

    def read_sheet(self,sheet_name , usecols , names) :
        """[summary]
        
        Arguments:
            sheet_name {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
 
        return pd.read_excel(self.path,sheet_name = sheet_name , usecols = usecols , names = names)
  
    def read_entities(self) :
        return self.read_sheet(SHEET_MAP['Entities'], usecols = list(ENTITIES_MAP.values()), names = list(ENTITIES_MAP.keys()))

    def read_properties(self) :
        return self.read_sheet(SHEET_MAP['Properties'], usecols = list(PROPERTIES_MAP.values()), names = list(PROPERTIES_MAP.keys()))

    def read_shareolders(self) :
        return self.read_sheet(SHEET_MAP['Shareolders'], usecols = list(SHAREOLDERS_MAP.values()), names = list(SHAREOLDERS_MAP.keys()))

    def read_all(self) :
        self.entities = self.read_entities()
        self.properties = self.read_properties()
        self.shareolders = self.read_shareolders()

    def clean_cols(self,df) :
        for col in df :
            if df[col].dtype == 'object' :
                df[col] = self.clean_strcol(df[col])

            if 'float' in str(df[col].dtype) :
                df[col] = self.clean_floatcol(df[col])

    def clean_strcol(self,col) :
        return(col.apply(lambda x : x.strip() if type(x) == 'str' else x))

    def clean_floatcol(self,col) : 
        return(col.apply(lambda x : 0 if math.isnan(x) else x))

    def clean_all(self) : 
        self.clean_cols(self.entities)
        self.clean_cols(self.properties)
        self.clean_cols(self.shareolders)

    def check_properties(self) :
        check = ~self.properties[ENTITIES_NODE_INDEX].isin(self.entities[ENTITIES_NODE_INDEX])
        return [entitie for entitie in self.properties.loc[check,ENTITIES_NODE_INDEX]]

    def check_shareolders(self) :
        check = ~self.shareolders[ENTITIES_NODE_INDEX].isin(self.entities[ENTITIES_NODE_INDEX])
        return [entitie for entitie in self.shareolders.loc[check,ENTITIES_NODE_INDEX]]

    def check_all(self) :
        check1 = self.check_properties()
        check2 = self.check_shareolders()

        if len(check1) :
            p = len(check1) > 1
            value = 'Entitie{} {} {} declared in "{}" sheet but {} not in "{}" sheet'
            value = value.format('s' if p else '',', '.join(check1),'are' if p else 'is',
             SHEET_MAP['Properties'],'are' if p else 'is',SHEET_MAP['Entities'])
            raise Exception(value)

        if len(check2) :
            p = len(check2) > 1
            value = 'Entitie{} {} {} declared in "{}" sheet but {} not in "{}" sheet'
            value = value.format('s' if p else '',', '.join(check2),'are' if p else 'is',
             SHEET_MAP['Shareolders'],'are' if p else 'is',SHEET_MAP['Entities'])
            raise Exception(value)

    def process(self) :
        self.read_all()
        self.clean_all()
        self.check_all()