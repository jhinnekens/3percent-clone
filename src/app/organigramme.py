import networkx as nx


class Organigramme :

    def __init__(self,shareolders,buildings) :
        """ Constructor

        Arguments:
            shareolders {pandas.core.frame.DataFrame} -- [DataFrame of shareolders]
            buildings {pandas.core.frame.DataFrame} -- [DataFrame of buildings]
        """
        
        self.shareolders = shareolders
        self.buildings = buildings
        self.G = nx.DiGraph()

    def build(self) :
        """ Build organigramme Graph
        """

        self.building_nodes = []
        for e1,e2,e3 in zip(self.buildings.iloc[:,2],self.buildings.iloc[:,6],self.buildings.iloc[:,5]) :
            self.G.add_node(e1 , value = e3)
            self.G.add_edge(e1 , e2,shares = 1.)
            self.building_nodes.append(e1)

        self.shareolder_nodes = []
        for e1,e2,e3 in zip(self.shareolders.iloc[:,0],self.shareolders.iloc[:,1],self.shareolders.iloc[:,3]) : 
            self.G.add_edge(e1,e2,shares = e3 , display_shares = round(e3,3))
            self.shareolder_nodes.append(e1)
            self.shareolder_nodes.append(e2)

        self.shareolder_nodes = list(set(self.shareolder_nodes))

    def get_shareolders(self) :
        """ Getter for shareolders nodes
        
        Returns:
            list -- Return a list of shareolders
        """
        return self.shareolder_nodes

    def get_buildings(self) :
        """Getter for buildings nodes
        
        Returns:
            list -- Return a list of buildings
        """
        return self.building_nodes

    def compute_share(self,entitie) :
        """Compute the total holding that the entitie shares
        
        Arguments:
            entitie {str} -- entitie name
        
        Returns:
            float -- Total holding shared by the entitie
        """

        total = 0.

        for building in self.building_nodes :
            for path in map(nx.utils.pairwise, nx.all_simple_paths(self.G,building,entitie)):
                edges = [(e1,e2) for e1,e2 in path]
                path_amount = 1.0
                for edge in edges :
                    path_amount = path_amount*self.G.edges[edge]['shares']   
                total = path_amount*self.G.nodes[building]['value'] + total

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

        nx.draw_networkx_nodes(G,pos,nodelist = building_nodes , node_color = 'red', node_shape = '^' , node_size = 1000 )
        nx.draw_networkx_nodes(G,pos,nodelist = shareolder_nodes , node_color = 'yellow', node_shape = 's' , node_size = 1000)
        nx.draw_networkx_labels(G,pos,labels = {key:value for key,value in zip(building_nodes,building_nodes)})
        nx.draw_networkx_labels(G,pos,labels = {key:value for key,value in zip(shareolder_nodes,shareolder_nodes)}, font_size = 8)
        nx.draw_networkx_edge_labels(G,pos,edge_labels= nx.get_edge_attributes(G,'display_shares'))
        nx.draw_networkx_edges(G,pos)

        plt.savefig("Graph.png", format="PNG")


            



