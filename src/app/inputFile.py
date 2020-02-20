from config import *
import pandas as pd

class InputFile :

    def __init__(self,path) :
        """[summary]
        
        Arguments:
            path {[type]} -- [description]
        """
        self.path = path

    def read_sheet(self,sheet_name) :
        """[summary]
        
        Arguments:
            sheet_name {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        return pd.read_excel(self.path,sheet_name = sheet_name)

    def get_entities(self) :
        return self.read_sheet(SHEET_MAP['Entities'])

    def get_properties(self) :
        return self.read_sheet(SHEET_MAP['Properties'])

    def get_shareolders(self) :
        return self.read_sheet(SHEET_MAP['Shareolders'])
