import plotly.plotly as py
import plotly.tools as tools
from plotly.graph_objs import *
from sklearn.cluster import KMeans
import networkx as nx
import plotly
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib
from scipy import spatial
import random
from plotly import *

tools.set_credentials_file(username='username', api_key='key')

# edges trace for plot
def get_edge_trace(G):
    edge_trace = Scatter(
        x=[],
        y=[],
        line=Line(width=0.5,color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    return edge_trace

# nodes trace for plot
def get_node_trace(G):
    node_trace = Scatter(
        ids = [],
        x=[],
        y=[],
        customdata = [],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=Marker(
            showscale=True,
            colorscale='YIGnBu',
            reversescale=True,
            color=[],
            size=10,
            line=dict(width=2)))


    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'].append(x)
        node_trace['y'].append(y)
        node_trace['ids'].append(node)
        node_trace['customdata'].append(G.adjacency_list()[node])

    # color node by node degrees
    for node, adjacencies in enumerate(G.adjacency_list()):
        node_trace['marker']['color'].append(len(adjacencies))
        node_info = '# of connections: '+str(len(adjacencies))
        node_trace['text'].append(node_info)

    return node_trace

# find all cycle containing n-1 edges in graph G
def findPaths(G,u,n):
    if n==0:
        return [[u]]
    paths = [[u]+path for neighbor in G.neighbors(u) for path in findPaths(G,neighbor,n-1) if u not in path]
    return paths

def draw_Graph(G, graphName, graphTitle):
    edge_trace = get_edge_trace(G)
    node_trace = get_node_trace(G)

    # creat network graph
    fig = Figure(data=Data([edge_trace, node_trace]),
                 layout=Layout(
                    title=graphTitle,
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text = "",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

    py.image.save_as(fig, filename=graphName)

def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath: return newpath
    return None

if __name__ == "__main__":

    # get node positions
    nnodes = 100
    print ("Generating graph with 100 nodes....")
    # generate Graph
    G = nx.random_geometric_graph(nnodes,0.05)
    pos = nx.get_node_attributes(G,'pos')
    G_temp = nx.random_regular_graph(26,nnodes)

    # add edge from G_temp to G
    # so that degree of nodes in G is <= 25% of nodes
    for edge in G_temp.edges():
        if edge not in G.edges():
            G.add_edge(edge[0], edge[1])

    # get node positions from G_temp
    positions = []
    for node in G_temp.nodes():
        x, y = G.node[node]['pos']
        positions.append([x, y])
        

    # r is radius
    r = 1.0/(nnodes-5)
    kdtree = spatial.KDTree(positions)
    pairs = kdtree.query_pairs(r)

    # if nodes are close (inside r) but they don't have edges, add an edge between them
    for edge in pairs:
        if edge not in G.edges():
            G.add_edge(edge[0], edge[1])

    # draw real network    
    title = '<br>Network graph'
    draw_Graph(G, "networkx.png", title)
    print ("\nNetwork is saves in ", 'networkx.png')
    
    # get real network info for clustering 
    edge_trace = get_edge_trace(G)
    node_trace = get_node_trace(G)
    nodes = {'x': node_trace['x'], 'y': node_trace['y']}
    df_nodes = pd.DataFrame(data=nodes)
 

    G_overlay = None
    while True:    
        print("\n\n")
        print("Enter q to quit,")
        print("or Enter p to find shortest path, ")
        n_superpeers = input("or Enter number of super peers : ")

        if n_superpeers == 'q':
            print ("Exit!")
            exit()
        elif n_superpeers == 'p':
            source = input(" Enter source node: ")
            dest = input(" Enter destination node:")
            if source.isdigit() and dest.isdigit():
                if int(source) > 0 and int(source) < nnodes and int(dest) > 0 and int(dest) < nnodes:
                    print ("\n Shortest path from "+source+" to "+ dest+" in real network: ", nx.shortest_path(G,source=int(source),target=int(dest)))
                    if (G_overlay):
                        print ("\n List of Super peers: ", superpeers)
                        print ("\n Shortest path from "+source+" to "+ dest+" in overlay network: ", nx.shortest_path(G_overlay,source=int(source),target=int(dest)))
                    else:
                        print ("\n No overlay network exists.")
                else:
                    print ("\n ID must be in range from 0 to ", (nnodes-1))
            else:
                print("\n ID must be a digit.")

        elif n_superpeers.isdigit():

            # clustering nodes into n_superpeers groups by coordinates
            kmeans = KMeans(n_clusters=int(n_superpeers)).fit(df_nodes)

            # get list of color from matplotlib.colors
            # colormap = np.array([name for name, hex in colors.cnames.items()])
            colormap = np.array(['green', 'greenyellow', 'purple', 
                   'lime', 'orange', 'maroon', 'skyblue', 
                   'seashell', 'darksalmon', 'dimgrey', 'dodgerblue', 'lightyellow',
                   'black', 'sandybrown', 'salmon', 'limegreen',
                   'lavender', 'antiquewhite', 'steelblue',
                   'darkslateblue', 'lightgoldenrodyellow', 'thistle',
                   'cornflowerblue', 'aliceblue', 'lightsteelblue', 'blueviolet',
                   'orangered', 'lightseagreen', 'mediumpurple', 'goldenrod',
                   'darkmagenta', 'hotpink', 'indianred', 'pink',
                   'darkseagreen', 'navy', 'whitesmoke', 'mediumseagreen', 'gray',
                   'chartreuse', 'deepskyblue', 'cyan', 'navajowhite', 'azure',
                   'lightsage', 'burlywood', 'ghostwhite', 'darkgrey',
                   'darkcyan', 'peachpuff', 'olive', 'lightcyan', 'dimgray',
                   'lightskyblue', 'orchid', 'snow', 'darkgreen', 'midnightblue',
                   'mediumvioletred', 'tomato', 'darkolivegreen', 'saddlebrown',
                   'gold', 'olivedrab', 'bisque', 'darkviolet', 'royalblue', 'peru',
                   'sage', 'chocolate', 'beige', 'lavenderblush',
                   'oldlace', 'paleturquoise', 'gainsboro', 'springgreen',
                   'mediumslateblue', 'turquoise', 'yellow', 'teal', 'lightslategray',
                   'lightblue', 'mediumaquamarine', 'darkslategray', 'mintcream',
                   'lightgray', 'darkgoldenrod', 'mediumblue', 'tan', 'lightcoral',
                   'blue', 'mediumturquoise', 'crimson', 'coral', 'lemonchiffon',
                   'cornsilk', 'wheat', 'aqua', 'darkorchid', 'darkorange',
                   'khaki', 'darkkhaki', 'darkslategrey', 'deeppink', 'darkgray',
                   'violet', 'palegreen', 'linen', 'powderblue', 'magenta',
                   'slategrey', 'darkturquoise', 'mediumorchid', 'fuchsia',
                   'papayawhip', 'brown', 'seagreen', 'aquamarine', 'sienna',
                   'blanchedalmond', 'mistyrose', 'forestgreen', 'lightsalmon',
                   'slategray', 'palevioletred', 'white', 'floralwhite', 'lawngreen',
                   'ivory', 'honeydew', 'silver', 'lightgreen', 'darkred', 'indigo',
                   'rosybrown', 'darkblue', 'palegoldenrod', 'yellowgreen',
                   'red', 'lightgrey', 'cadetblue', 'firebrick', 'darksage',
                   'mediumspringgreen', 'plum', 'moccasin', 'grey', 'slateblue'],)

            plt.title("Clustering")
            plt.scatter(df_nodes.x, df_nodes.y, c=colormap[kmeans.labels_])
            
            plt.savefig('clusters.png')

            clusters = {} # list of nodes in same cluster
            for i in range(len(kmeans.labels_)):
                if kmeans.labels_[i] not in clusters:
                    clusters[kmeans.labels_[i]] = []
                clusters[kmeans.labels_[i]].append(i)
            
            # pick random node in each cluster
            superpeers = [random.choice( clusters[i] ) for i in clusters]
            print ("\nSelected nodes for Super peers: ", superpeers)
            # print(clusters)

            # build overlay network
            G_overlay = nx.Graph()
            pos_overlay = {}
            for i in superpeers:
                cluster_i = kmeans.labels_[i]
                for e in clusters[cluster_i]:
                    if i != e:
                        G_overlay.add_node(e)
                        G_overlay.add_edge(i, e)
                        x, y = G.node[e]['pos']
                        pos_overlay[e] = [x,y]
                    else:
                        G_overlay.add_node(i)
                        x, y = G.node[i]['pos']
                        pos_overlay[i] = [x,y]

            nx.set_node_attributes(G_overlay, 'pos', pos_overlay)

            # add edges between pairs of super peers
            for i in range(0, len(superpeers)):
                for j in range(i+1, len(superpeers)):
                    G_overlay.add_edge(superpeers[i], superpeers[j])
                
            title = '<br>Overlay network with '+n_superpeers+' super peers'
            draw_Graph(G_overlay, 'networkx_overlay.png', title)
            print ("\nOverlay network is save in " + 'networkx_overlay.png')

        else:
            print ("\nWrong input.")

