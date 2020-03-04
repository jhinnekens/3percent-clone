class Node(object) :
    def __init__(self,id,**kwargs):
        self.id = id
        self.attr = kwargs
        self.type = 'node'

    def __getitem__(self,item):
         return self.attr[item]


class Entite(Node) :
    def __init__(self,id,**kwargs):
        super().__init__(id,**kwargs)
        self.type = 'entite'

class Propertie(Node) :
    def __init__(self,id,**kwargs):
        super().__init__(id,**kwargs)
        self.type = 'propertie'

class Trust(Node) : 
    def __init__(self,id,**kwargs):
        super().__init__(id,**kwargs)
        self.type = 'trust'