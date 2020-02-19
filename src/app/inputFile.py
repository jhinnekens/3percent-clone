
import pandas as pd

class InputFile :

    def __init__(self,path) :
        self.path = path

    def read(self,sheet_name) :
        return pd.read_excel(self.path,sheet_name = sheet_name)

    