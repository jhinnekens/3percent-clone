import networkx as nx
from config import *
import matplotlib.pyplot as plt


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
            self.G.nodes[row[ENTITIES_NODE_INDEX]]['shape'] = 'rect'
            self.entities_nodes.append(row[ENTITIES_NODE_INDEX])

        self.properties_nodes = []
        for index,row in inputFile.properties.iterrows():
            node_attr = {key:value for key,value in zip(PROPERTIES_MAP.keys(),row[list(PROPERTIES_MAP.keys())]) if key != PROPERTIES_NODE_INDEX}
            edge_attr = {HOLDING_PERCENTAGE : 1.0 , NUMBER_SHARES : self.G.nodes[row[ENTITIES_NODE_INDEX]][NUMBER_SHARES] }
            self.G.add_node(row[PROPERTIES_NODE_INDEX],**node_attr)
            self.G.nodes[row[PROPERTIES_NODE_INDEX]]['shape'] = 'triangle'
            self.G.add_edge(row[PROPERTIES_NODE_INDEX],row[ENTITIES_NODE_INDEX],**edge_attr)
            self.properties_nodes.append(row[PROPERTIES_NODE_INDEX])

        for index,row in inputFile.shareolders.iterrows():
            edge_attr = {HOLDING_PERCENTAGE : row[HOLDING_PERCENTAGE], NUMBER_SHARES : row[NUMBER_SHARES]}
            self.G.add_edge(row[ENTITIES_NODE_INDEX],row[DIRECT_SHAREOLDER],**edge_attr)

        pos = nx.nx_agraph.graphviz_layout(self.G, prog='dot')

        y = list()
        x = list()
        for node_pos in pos.values() :
            y.append(node_pos[1])
            x.append(node_pos[0])

        x = list(set(x))
        x.sort()

        if max(x) != min(x) :
            x_norm = [(e-min(x))/(max(x)-min(x)) for e in x]
        else : 
            x_norm = [0.5 for i in range(le(x))]
        
        x = {key:value for key,value in zip(x,x_norm)}

        y = list(set(y))
        y.sort()
        y = {key:value for key,value in zip(y,range(len(y)))}

        
        for node in self.G.nodes :
            self.G.nodes[node]['coord'] = {'x' : x[pos[node][0]] , 'y' : pos[node][1]}
            self.G.nodes[node]['layer'] = y[pos[node][1]]
            self.G.nodes[node]['total_layer'] = len(y)


    def compute_layer(self) : 

        for propertie in self.properties_nodes :
            lvl = 1
            bfs = nx.bfs_successors(self.G,propertie)
            for neighbors in bfs : 
                nodes = neighbors[1]
                for node in nodes :
                    self.G.nodes[node]['layer'].append(lvl)
                lvl+=1

        for node in self.entities_nodes :
            self.G.nodes[node]['layer'] = max(self.G.nodes[node]['layer'])
    
    def get_entities(self) :
        """ Getter for entities nodes
        
        Returns:
            list -- Return a list of entities
        """
        return self.entities_nodes

    def get_properties(self) :
        """Getter for properties nodes
        
        Returns:
            list -- Return a list of buildings
        """
        return self.properties_nodes

    def entitie(self,entitie) :
        return self.G.nodes[entitie]

    def entitie_attr(self,entitie,attr) :
        return self.entitie(entitie)[attr]

    def get_paths(self,entitie,propertie) :
        paths = []
        for path in map(nx.utils.pairwise, nx.all_simple_paths(self.G,propertie,entitie)):
            paths.append([e for e in path])
        return paths

    def get_all_paths(self,entitie) :
        """ Return all edges between properties and the given entitie
        
        Arguments:
            entitie {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        paths = []
        for propertie in self.properties_nodes :
            for path in self.get_paths(entitie,propertie) :
                paths.append(path)
        return paths

    def get_all_parents(self,entitie) :
        """ Return all entities between the given entitie and properties
        
        Arguments:
            entitie {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        paths = self.get_all_paths(entitie)
        parents = []
        for path in paths :
            for e1,e2 in path :
                if e1 != entitie and e1 not in self.properties_nodes:
                    parents.append(e1)
                if e2 != entitie and e2 not in self.properties_nodes:
                    parents.append(e2)
        parents = list(set(parents))
        return parents

    def properties_shared(self,entitie) : 
        shared_properties = []
        for propertie in self.get_properties():
            if nx.has_path(self.G,propertie,entitie):
                shared_properties.append(propertie)
        return shared_properties

    def compute_share_prop(self,entitie,propertie) :
        paths = self.get_paths(entitie,propertie)
        total = 0.0
        for path in paths :
            edges = [(e1,e2) for e1,e2 in path]
            path_amount = 1.0
            for edge in edges :

                path_amount = path_amount*self.G.edges[edge][HOLDING_PERCENTAGE]
            total = path_amount*self.G.nodes[propertie][PROPERTIE_VALUE] + total
        return round(total)

    def compute_share(self,entitie) :
        total = 0
        for propertie in self.properties_nodes :
            total = total + self.compute_share_prop(entitie,propertie)

        return total

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

    def jsonify(self):
        return nx.node_link_data(self.G)

    def draw(self) :
        pos = nx.nx_agraph.graphviz_layout(self.G, prog='dot', args='-Gordering=out -Nwidth=".2" -Nheight=".2" -Nmargin=0 -Gfontsize=8')

        nx.draw_networkx_nodes(self.G,pos,nodelist = self.properties_nodes , node_color = 'red', node_shape = '^' , node_size = 500 )
        nx.draw_networkx_nodes(self.G,pos,nodelist = self.entities_nodes , node_color = 'yellow', node_shape = 's' , node_size = 500)
        nx.draw_networkx_labels(self.G,pos,labels = {key:value for key,value in zip(self.properties_nodes,self.properties_nodes)})
        nx.draw_networkx_labels(self.G,pos,labels = {key:value for key,value in zip(self.entities_nodes,self.entities_nodes)}, font_size = 4)
        #nx.draw_networkx_edge_labels(self.G,pos)
        nx.draw_networkx_edges(self.G,pos,connectionstyle=None)

        plt.savefig("/home/etienne/Documents/Graph.png", format="PNG")



