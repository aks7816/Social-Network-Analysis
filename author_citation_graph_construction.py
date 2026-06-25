import pandas as pd
import numpy as np
import torch
#from torch_geometric.nn import GCNConv, GNNExplainer
import pandas as pd
import itertools
import ast
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import font_manager
import torch
import igraph as ig
import leidenalg as la
import seaborn as sns
import cairo
import numpy as np
np.float = float
import burst_detection as bd
import numpy as np
from scipy.signal import find_peaks
from hmmlearn.hmm import GaussianHMM
import numpy as np
from luminol.anomaly_detector import AnomalyDetector
from torch_geometric.data import Data
from sklearn.preprocessing import StandardScaler
# from torch_geometric.nn import GCNConv, GNNExplainer
# import torch.nn.functional as F


device = torch.device("mps")
if device:
    print("-----------------Connected to MPS---------------------")

###START##############################################################

# class GCN(torch.nn.Module):
#     def __init__(self, in_channels, hidden_channels, out_channels):
#         super(GCN, self).__init__()
#         self.conv1 = GCNConv(in_channels, hidden_channels)
#         self.conv2 = GCNConv(hidden_channels, out_channels)

#     def forward(self, data):
#         x = F.relu(self.conv1(data.x, data.edge_index))
#         return F.log_softmax(self.conv2(x, data.edge_index), dim = 1)
    


def netCreationAI(csv):

    df = pd.read_csv(csv)
    df["Authors"] = df["Authors"].apply(ast.literal_eval)
    # df = df.head(200000)

    years = sorted(df["Year"].unique())

    allconnectionsyear = []
    nodes = set()
    decay = []
    labels = []
    nodename = []
    relids = []
    

    for year in years:
        if year >= 2016:
        
            

            yearigraph = ig.Graph(directed = True)

            parents = df[df["ParentID"].isna()]
            parentList = (parents["AlexID"].tolist())
            
            
            

            for a in range(0, len(parentList)):
                for b in range(0, len(df["AlexID"])):
                    if df["ParentID"][b] == parentList[a]:
                    
                        childAuthors = []
                        parentAuthors = []

                        for child in df["Authors"][b]:
                        
                            if child is not None:
                                childAuthors.append(child)
                        
                        for parent in df[df["AlexID"] == parentList[a]]["Authors"].values[0]:
                        
                            if parent is not None:
                                parentAuthors.append(parent)

                        # print(parentAuthors)
                        # print(childAuthors)
                        if childAuthors == []:
                            continue
                        elif parentAuthors == []:
                            continue
                        
                        connections = list(itertools.product(parentAuthors, childAuthors))
                        
                        allconnectionsyear.extend(connections)

        
    for edge in allconnectionsyear:
        for node in edge:
            nodes.add(node)
    nodes = list(nodes)

    yearigraph.add_vertices(nodes)
    
    yearigraph.vs["name"] = nodes

    ids = {}
    for id, name in enumerate(yearigraph.vs["name"]):
        ids[name] = id

    
    for src, dest in allconnectionsyear:
        if src in ids and dest in ids:
            parentind = ids[src]
            childind = ids[dest]
            relids.append((parentind, childind))

    yearigraph.add_edges(relids)

    partition = la.find_partition(yearigraph, la.ModularityVertexPartition)

    bt = yearigraph.betweeness(directed = True)
    std = np.std(bt)
    recentyear = df.explode("Authors").groupby("Authors")["Year"].max().to_dict()


    for i, name in enumerate(nodes):
        recent = recentyear.get(name)
        if recent != 2025:
            timedecay = 1/ (2025 - recent)
        else:
            timedecay = 0
        value = bt[i] * timedecay
        decay.append([bt[i], value])
        labels.append(partition.membership[i])
        nodename.append(name)

    features = StandardScaler().fit_transform(np.array(decay))
    x = torch.tensor(features, dtype= torch.float)
    y = torch.tensor(labels, dtype= torch.long)
    edge_index = torch.tensor(relids, dtype = torch.long).t().contiguous()

    data = Data(x = x, edge_index = edge_index, y=y)
    return data, nodename

                




# def netCreationWEB(csv):

#     df = pd.read_csv(csv)
#     df["Authors"] = df["Authors"].apply(ast.literal_eval)
#     # df = df.head(200000)

#     chinesefont = font_manager.FontProperties()
#     chinesefont.set_family("Heiti TC")
#     chinesefont.set_size(14)

#     years = sorted(df["Year"].unique())
    
    

#     for year in years:
#         if year >= 1994 and year <= 2001:
        
#             focusYear = df[df["Year"] == year].reset_index(drop = True)

#             yearigraph = ig.Graph(directed = True)

#             parents = focusYear[focusYear["ParentID"].isna()]
#             parentList = (parents["AlexID"].tolist())
            
            
#             allconnectionsyear = []

#             for a in range(0, len(parentList)):
#                 for b in range(0, len(focusYear["AlexID"])):
#                     if focusYear["ParentID"][b] == parentList[a]:
                    
#                         childAuthors = []
#                         parentAuthors = []

#                         for child in focusYear["Authors"][b]:
                        
#                             if child is not None:
#                                 childAuthors.append(child)
                        
#                         for parent in focusYear[focusYear["AlexID"] == parentList[a]]["Authors"].values[0]:
                        
#                             if parent is not None:
#                                 parentAuthors.append(parent)

#                         # print(parentAuthors)
#                         # print(childAuthors)
#                         if childAuthors == []:
#                             continue
#                         elif parentAuthors == []:
#                             continue
                        
#                         connections = list(itertools.product(parentAuthors, childAuthors))
                        
#                         allconnectionsyear.extend(connections)

#             nodes = set()
#             for edge in allconnectionsyear:
#                 for node in edge:
#                     nodes.add(node)
#             nodes = list(nodes)

#             yearigraph.add_vertices(nodes)
            
#             yearigraph.vs["name"] = nodes

#             ids = {}
#             for id, name in enumerate(yearigraph.vs["name"]):
#                 ids[name] = id

#             relids = []
#             for src, dest in allconnectionsyear:
#                 if src in ids and dest in ids:
#                     parentind = ids[src]
#                     childind = ids[dest]
#                     relids.append((parentind, childind))

#             yearigraph.add_edges(relids)

#             partition = la.find_partition(yearigraph, la.ModularityVertexPartition)

#             communitycolors = sns.color_palette("hsv", n_colors = len(set(partition.membership)))
#             listcolors = []
#             for cluster in partition.membership:
#                 listcolors.append(communitycolors[cluster])

#             f, axs = plt.subplots(figsize = (10, 8))

#             ig.plot(partition, target = axs, layout = yearigraph.layout("fr"), vertex_colors = listcolors, edge_color = "gray")
#             plt.title(f"Temporal Leiden Community Clusters for {year}")
#             plt.savefig(f"Temporal Leiden Community Clusters for {year}.jpeg")



print(netCreationAI("GlobalAIData copy edit2strow.csv"))
# # netCreationWEB("GlobalWebNetworking copy.csv")




