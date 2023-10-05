import streamlit as st
import numpy as np
import pandas as pd
import os
from networkx.generators.random_graphs import fast_gnp_random_graph, gnp_random_graph
from streamlit_agraph import agraph, Node, Edge, Config
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Graph Coloring Problem")

# A global variable to store the adjacency matrix of the generated graph
global M
global G_hat

error_code = 0

# Node color Map
node_color_map = {
    0 : "#F2134F",
    1 : "#0554F2",
    2 : "#49A646",
    3 : "#D3D925",
    4 : "#F29F05",
    5 : "#F2F2F2",
    6 : "#F20530",
    7 : "#0477BF",
    8 : "#51A65E",
    9 : "#F2B705",
    10 : "#BF3F61",
    11 : "#467362",
    12 : "#A66329",
    13 : "#F29544",
    14 : "#F2D6BD"
}

st.header("Graph Inputs : ")

# Number of nodes you need in the graph
n_nodes = st.text_input("Home many nodes you want in the graph? (Please enter a number)", value = 6)

# Do you want a dense or sparse graph
prob = st.text_input("Enter a value between 0 and 1 to control the denseness of the graph", value = 0.6)

# Number of colors you want to color the graph with
n_colors = st.text_input("Enter the number of colors you wanto paint your nodes with:", value = 10)

# data type conversion
n_nodes = int(n_nodes)
prob = float(prob)
n_colors = int(n_colors)

def generate_graph(n, p):
    global M
    global G_hat
    # Generate a graph based on above parameters
    G = fast_gnp_random_graph(n_nodes, prob)
    G_hat = G
    # Adjacency matrix of graph G
    M = nx.to_numpy_array(G, dtype = "uint16")
    
    # plot the initial state of the graph G
    fig, ax = plt.subplots(figsize = (10, 7))
    nx.draw(G, with_labels = True)
    st.pyplot(fig)


# button to generate the graph
generate_graph_button = st.button("Generate New Graph", on_click= generate_graph(n_nodes, prob))

# printing Adjacency matrix of above graph
st.header("Adjacency Matrix of the above created graph: ")
st.table(M)

# dimensions of the current graph
n_rows, n_cols = M.shape

# Matrix to keep track of nodes and assigned colors
Node_Color_Matrix = np.zeros((n_rows, n_colors), dtype = "uint")



def color_neighbors(neighbor_array, current_node, current_node_color):
    Node_Color_Matrix[current_node][current_node_color] = 1
    for neighbor in neighbor_array[0]:
        Node_Color_Matrix[neighbor][current_node_color] = 2
    return Node_Color_Matrix

start_node = 0
start_color = 0
# Only for start node we do this explicitely
node_neighbors = np.where(M[start_node] == 1)
temp_matrix = color_neighbors(node_neighbors, start_node, start_color)

remaining_nodes = list(range(n_rows))
remaining_nodes.remove(start_node)

for node in remaining_nodes:
    try:
        # look for all the adjacent nodes available
        node_neighbors = np.where(M[node] == 1)
        # Assign the first color available to the node
        node_color = np.where(Node_Color_Matrix[node] == 0)[0][0]
        # Call the color neighbor function to color the current node as well as other nodes
        temp_matrix = color_neighbors(node_neighbors, node, node_color)
    
    except Exception as e:
        error_code = -1
        #print("{} colors are not sufficient to fulfill the coloring constraints".format(n_colors))
        break
    

# checking how many colors are used for this graphs
print("Total colors given : ", n_colors)
not_used_colors = len(np.where(Node_Color_Matrix.sum(axis = 0) == 0)[0])
print("Colors not used after graph processing : ", not_used_colors)

# Assigned colors to nodes:
node_color_dict = {}
for node in range(n_rows):
    try:
        node_color = np.where(Node_Color_Matrix[node] == 1)[0][0]
        node_color_dict[node] = node_color
    except Exception as e:
        st.error("{} colors are not sufficient to color the graph with given constraint".format(n_colors))
        error_code = -1
        break

node_color_dict = {k : node_color_map[v] for k,v in node_color_dict.items()}

if error_code == 0:
    # plotting final network
    fig, ax = plt.subplots(figsize = (10, 7))
    nx.draw(G_hat, node_color = node_color_dict.values(), with_labels = True)
    st.pyplot(fig)

    st.write("Total number of Colors Provided : {}".format(n_colors))
    st.write("Total Colors used in the graph : {}".format(n_colors - not_used_colors))

    st.header("Node Color Matrix")
    st.table(Node_Color_Matrix)
    st.write("- Rows are the nodes in the graph")
    st.write("- Columns are colors in the graph")
    st.write("- 1 in the cell means that color is assigned to that node")
    st.write("- 2 in the cell means that that color is blocked for that node")

st.subheader("Created by: Akash Ponduru")
st.subheader("Guided by: Professor Gary Dargush")
