import networkx as nx


class Organigramme :

    def __init__(self,shareolders,buildings) :
        self.shareolders = shareolders
        self.buildings = buildings
        self.G = nx.DiGraph()

    def build(self) :

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
        return self.shareolder_nodes

    def get_buildings(self) :
        return self.building_nodes

    def compute_share(self,entitie) :
        total = 0

        for building in self.building_nodes :
            for path in map(nx.utils.pairwise, nx.all_simple_paths(self.G,building,entitie)):
                edges = [(e1,e2) for e1,e2 in path]
                path_amount = 1.0
                for edge in edges :
                    path_amount = path_amount*self.G.edges[edge]['shares']   
                total = path_amount*self.G.nodes[building]['value'] + total

        return round(total)

    def info(self) :
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


            



