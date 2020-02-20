from config import *
import pandas as pd

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
        return pd.read_excel(self.path,sheet_name = sheet_name , usecols = usecols, names = names)

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
            print(col)
            print(df[col].dtype)

    def strip(self,df) :
        df = df.transform(lambda x : x.strip() if type(x) == 'str' else x)
    
