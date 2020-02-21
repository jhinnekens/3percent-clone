import networkx as nx
from config import *


class Organigramme :

    def __init__(self) :
        """ Constructor

        Arguments:
            shareolders {pandas.core.frame.DataFrame} -- [DataFrame of shareolders]
            buildings {pandas.core.frame.DataFrame} -- [DataFrame of buildings]
        """
        
        self.G = nx.DiGraph()

    def build(self,inputFile) :
        """ Build organigramme Graph
        """

        self.entities_nodes=[]
        for index,row in inputFile.entities.iterrows():
            node_attr = {key:value for key,value in zip(ENTITIES_MAP.keys(),row[list(ENTITIES_MAP.keys())]) if key != ENTITIES_NODE_INDEX}
            self.G.add_node(row[ENTITIES_NODE_INDEX],**node_attr)
            self.entities_nodes.append(row[ENTITIES_NODE_INDEX])

        self.properties_nodes = []
        for index,row in inputFile.properties.iterrows():
            node_attr = {key:value for key,value in zip(PROPERTIES_MAP.keys(),row[list(PROPERTIES_MAP.keys())]) if key != PROPERTIES_NODE_INDEX}
            edge_attr = {HOLDING_PERCENTAGE : 1.0}
            self.G.add_node(row[PROPERTIES_NODE_INDEX],**node_attr)
            self.G.add_edge(row[PROPERTIES_NODE_INDEX],row[ENTITIES_NODE_INDEX],**edge_attr)
            self.properties_nodes.append(row[PROPERTIES_NODE_INDEX])

        for index,row in inputFile.shareolders.iterrows():
            edge_attr = {HOLDING_PERCENTAGE : row[HOLDING_PERCENTAGE]}
            self.G.add_edge(row[ENTITIES_NODE_INDEX],row[DIRECT_SHAREOLDER],**edge_attr)
    
    def get_entities(self) :
        """ Getter for entities nodes
        
        Returns:
            list -- Return a list of entities
        """
        return self.shareolder_nodes

    def get_properties(self) :
        """Getter for properties nodes
        
        Returns:
            list -- Return a list of buildings
        """
        return self.properties_nodes

    def compute_share(self,entitie) :
        """Compute the total holding that the entitie shares
        
        Arguments:
            entitie {str} -- entitie name
        
        Returns:
            float -- Total holding shared by the entitie
        """

        total = 0.

        for propertie in self.properties_nodes :
            for path in map(nx.utils.pairwise, nx.all_simple_paths(self.G,propertie,entitie)):
                edges = [(e1,e2) for e1,e2 in path]
                path_amount = 1.0
                for edge in edges :
                    path_amount = path_amount*self.G.edges[edge][HOLDING_PERCENTAGE]   
                total = path_amount*self.G.nodes[propertie][PROPERTIE_VALUE] + total

        return round(total)

    def children(self,entitie) :
        """ Return entities which shared the given entitie
        
        Arguments:
            entitie {str} -- parent entitie
        
        Returns:
            list -- A list of entities
        """
        return [child for child in self.G.successors(entitie)]
    
    def parents(self,entitie) : 
        """ Return entities which are shared by the given entitie
        
        Arguments:
            entitie {str} -- child entitie
        
        Returns:
            list -- A list of entities
        """
        return [parent for parent in self.G.predecessors(entitie)]

    def info(self) :
        """ Compute general infos about organigramme graph
        
        Returns:
            str -- return number of edges,nodes and average degrees
        """
        return str(nx.info(self.G))

    def draw(self) :
        return
        pos = graphviz_layout(G, prog='dot')

        nx.draw_networkx_nodes(G,pos,nodelist = properties_nodes , node_color = 'red', node_shape = '^' , node_size = 1000 )
        nx.draw_networkx_nodes(G,pos,nodelist = shareolder_nodes , node_color = 'yellow', node_shape = 's' , node_size = 1000)
        nx.draw_networkx_labels(G,pos,labels = {key:value for key,value in zip(properties_nodes,properties_nodes)})
        nx.draw_networkx_labels(G,pos,labels = {key:value for key,value in zip(shareolder_nodes,shareolder_nodes)}, font_size = 8)
        nx.draw_networkx_edge_labels(G,pos,edge_labels= nx.get_edge_attributes(G,'display_shares'))
        nx.draw_networkx_edges(G,pos)

        plt.savefig("Graph.png", format="PNG")


            



