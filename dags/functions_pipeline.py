from operator import itemgetter
import networkx as nx
import wikipedia
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def getting_data():
    ## Seed choosed is "ChatGPT" - https://pt.wikipedia.org/wiki/ChatGPT
    SEED = "Data engineering"
    STOPS = ("International Standard Serial Number",
        "International Standard Book Number",
        "National Diet Library",
        "International Standard Name Identifier",
        "International Standard Book Number (Identifier)",
        "Pubmed Identifier",
        "Pubmed Central",
        "Digital Object Identifier",
        "Arxiv",
        "Proc Natl Acad Sci Usa",
        "Bibcode",
        "Library Of Congress Control Number",
        "Jstor",
        "Doi (Identifier)",
        "Isbn (Identifier)",
        "Pmid (Identifier)",
        "Arxiv (Identifier)",
        "Bibcode (Identifier)",
        'S2Cid (Identifier)',
        'Issn (Identifier)',
        'Oclc (Identifier)',
        'Open Library (Identifier)',
        )

    wikipedia.set_lang("en")

    todo_1st = [(0, SEED)] # List of the next links to be searched. (0, SEED) means that the link SEED is at distance 0 from the SEED.
    todo_set = set(SEED) # Set of the next links to be searched. 
    done_set = set() # Set of the links already searched.

    g = nx.DiGraph()
    layer, page = todo_1st[0]
    
    while layer < 2:
        # Remove the name page of the current page from the todo_1st,
        # and add it to the set of processed pages.
        # If the script encounters this page again, it will skip over it.
        del todo_1st[0]
        done_set.add(page)

        #Show progress
        print(layer, page)

        # Attempt to download the selected page.
        try:
            wiki = wikipedia.page(page, auto_suggest=False)
        except:
            layer, page = todo_1st[0]
            print("Could not load", page)
            continue

        for link in wiki.links:
            link = link.title()
            if not link.startswith("List Of") and link not in STOPS:
                if link not in todo_set and link not in done_set:
                    todo_1st.append((layer + 1, link))
                    todo_set.add(link)
                g.add_edge(page, link)
        layer, page = todo_1st[0]

    print("{} nodes, {} edges".format(len(g), nx.number_of_edges(g)))
    ## Saving the graph
    nx.write_graphml(g, "/opt/airflow/results/wikipedia_network_raw.graphml")
    #return g

def cleaning_data():
    g = nx.read_graphml("/opt/airflow/results/wikipedia_network_raw.graphml")
    # remove self loops
    g.remove_edges_from(nx.selfloop_edges(g))

    # identify duplicates like that: 'network' and 'networks'
    duplicates = [(node, node + "s")
                for node in g if node + "s" in g
                ]

    for dup in duplicates:
        # *dup is a technique named 'unpacking'
        g = nx.contracted_nodes(g, *dup, self_loops=False)

    duplicates = [(x, y) for x, y in
                [(node, node.replace("-", " ")) for node in g]
                    if x != y and y in g]
    
    for dup in duplicates:
        g = nx.contracted_nodes(g, *dup, self_loops=False)

    # nx.contracted creates a new node/edge attribute called contraction
    # the value of the attribute is a dictionary, but GraphML
    # does not support dictionary attributes
    nx.set_node_attributes(g, 0,"contraction")
    nx.set_edge_attributes(g, 0,"contraction")

    print("{} nodes, {} edges".format(len(g), nx.number_of_edges(g)))

    # filter nodes with degree greater than or equal to 2
    core = [node for node, deg in dict(g.degree()).items() if deg >= 2]

    # select a subgraph with 'core' nodes
    gsub = nx.subgraph(g, core)

    print("{} nodes, {} edges".format(len(gsub), nx.number_of_edges(gsub)))

    nx.write_graphml(gsub, "/opt/airflow/results/wikipedia_network.graphml")

    print("Nodes removed: {:.2f}%".format(100*(1 - len(gsub.nodes)/len(g.nodes))))
    print("Edges removed: {:.2f}%".format(100*(1 - len(gsub.edges)/len(g.edges))))
    print("Final Edges per nodes ration: {:.2f}".format(len(gsub.edges)/len(gsub.nodes)))

    #return gsub

def plotting_results():
    g = nx.read_graphml("/opt/airflow/results/wikipedia_network.graphml")
    plot_cdf(g)
    plot_pdf(g)
    plot_metrics(g)
    plot_pair_grid(g)
    plot_core_shell(g)

### Ploting auxiliar functions
def plot_cdf(gsub):
    plt.style.use("default")
    # degree sequence
    degree_sequence = sorted([d for n, d in gsub.degree()], reverse=True)

    fig, ax = plt.subplots(1,2,figsize=(8,4))

    # all_data has information about degree_sequence and the width of each bin
    ax[0].hist(degree_sequence)
    ax[1].hist(degree_sequence,bins=[1,2,3,4,5,6,7,8,9,10])

    ax[0].set_title("Degree Histogram")
    ax[0].set_ylabel("Count")
    ax[0].set_xlabel("Degree")
    ax[0].set_ylim(0,5000)

    ax[1].set_title("Degree Histogram - Zoom")
    ax[1].set_ylabel("Count")
    ax[1].set_xlabel("Degree")
    ax[1].set_xlim(0,10)
    ax[1].set_ylim(0,3000)

    # Add function CDF to the plot using a secondary axis
    ax2 = ax[1].twinx()
    ax2.plot(np.cumsum(np.array([len([d for d in degree_sequence if d == i]) for i in range(1,11)]))/len(degree_sequence), color="red")
    ax2.set_ylabel("CDF", color="red")
    ax2.tick_params(axis='y', labelcolor="red")

    plt.tight_layout()
    #plt.show()
    # Save the plot
    fig.savefig("/opt/airflow/results/cdf_histograma.png")

def plot_pdf(gsub):
    plt.style.use("default")
    # degree sequence
    degree_sequence = sorted([d for n, d in gsub.degree()], reverse=True)

    fig, ax = plt.subplots(1,2,figsize=(8,4))

    # all_data has information about degree_sequence and the width of each bin
    ax[0].hist(degree_sequence)
    ax[1].hist(degree_sequence,bins=[1,2,3,4,5,6,7,8,9,10])

    ax[0].set_title("Degree Histogram")
    ax[0].set_ylabel("Count")
    ax[0].set_xlabel("Degree")
    ax[0].set_ylim(0,5000)

    ax[1].set_title("Degree Histogram - Zoom")
    ax[1].set_ylabel("Count")
    ax[1].set_xlabel("Degree")
    ax[1].set_xlim(0,10)
    ax[1].set_ylim(0,3000)

    # Add function PDF to the plot using a secondary axis
    ax2 = ax[1].twinx()
    ax2.plot(np.array([len([d for d in degree_sequence if d == i]) for i in range(1,11)])/len(degree_sequence), color="red")
    ax2.set_ylabel("PDF", color="red")
    ax2.tick_params(axis='y', labelcolor="red")


    plt.tight_layout()
    #plt.show()

    # Save the plot
    fig.savefig("/opt/airflow/results/pdf_histograma.png")

def plot_metrics(gsub):
    # Plot the degree centrality, closeness centrality, betweenness centrality, and eigenvector centrality in one single graph with four subplots

    ## Calculate centrality values for all nodes in the subgraph
    deg_cen = nx.degree_centrality(gsub)
    clo_cen = nx.closeness_centrality(gsub)
    bet_cen = nx.betweenness_centrality(gsub)
    eig_cen = nx.eigenvector_centrality(gsub)

    ## Create a list of centralities for each node
    node_and_deg_cent = [(node, round(deg_cen[node], 3)) for node in deg_cen]
    node_and_clo_cent = [(node, round(clo_cen[node], 3)) for node in clo_cen]
    node_and_bet_cent = [(node, round(bet_cen[node], 3)) for node in bet_cen]
    node_and_eig_cent = [(node, round(eig_cen[node], 3)) for node in eig_cen]

    ## Sort the list in descending order
    sorted_node_and_deg_cent = sorted(node_and_deg_cent, key=itemgetter(1), reverse=True)
    sorted_node_and_clo_cent = sorted(node_and_clo_cent, key=itemgetter(1), reverse=True)
    sorted_node_and_bet_cent = sorted(node_and_bet_cent, key=itemgetter(1), reverse=True)
    sorted_node_and_eig_cent = sorted(node_and_eig_cent, key=itemgetter(1), reverse=True)

    ## Getting the top 10 nodes by degree centrality
    top_10_deg = sorted_node_and_deg_cent[:10]
    top_10_clo = sorted_node_and_clo_cent[:10]
    top_10_bet = sorted_node_and_bet_cent[:10]
    top_10_eig = sorted_node_and_eig_cent[:10]

    ## Create a subgraph of gsub consisting only of the top 10 nodes
    top_10_nodes_deg = [node[0] for node in top_10_deg]
    top_10_nodes_clo = [node[0] for node in top_10_clo]
    top_10_nodes_bet = [node[0] for node in top_10_bet]
    top_10_nodes_eig = [node[0] for node in top_10_eig]

    gsub_deg = gsub.subgraph(top_10_nodes_deg)
    gsub_clo = gsub.subgraph(top_10_nodes_clo)
    gsub_bet = gsub.subgraph(top_10_nodes_bet)
    gsub_eig = gsub.subgraph(top_10_nodes_eig)

    ## Draw the subgraph
    plt.figure(figsize=(25, 25))
    plt.suptitle("Top 10 nodes by degree centrality, closeness centrality, betweenness centrality, and eigenvector centrality")

    ### Color the nodes in the subgraph in scale of their degree centrality
    plt.subplot(2, 2, 1)
    plt.title("Top 10 nodes by degree centrality")
    node_color_deg = [deg_cen[node] for node in gsub_deg]
    nx.draw_networkx(gsub_deg, pos=nx.kamada_kawai_layout(gsub_deg, scale=2), node_color=node_color_deg, with_labels=True, cmap=plt.cm.jet)

    ### Color the nodes in the subgraph in scale of their closeness centrality
    plt.subplot(2, 2, 2)
    plt.title("Top 10 nodes by closeness centrality")
    node_color_clo = [clo_cen[node] for node in gsub_clo]
    nx.draw_networkx(gsub_clo, pos=nx.kamada_kawai_layout(gsub_clo, scale=2), node_color=node_color_clo, with_labels=True, cmap=plt.cm.jet)


    ### Color the nodes in the subgraph in scale of their betweenness centrality
    plt.subplot(2, 2, 3)
    plt.title("Top 10 nodes by betweenness centrality")
    node_color_bet = [bet_cen[node] for node in gsub_bet]
    nx.draw_networkx(gsub_bet, pos=nx.kamada_kawai_layout(gsub_bet, scale=2), node_color=node_color_bet, with_labels=True, cmap=plt.cm.jet)


    ## Color the nodes in the subgraph in scale of their eigenvector centrality
    plt.subplot(2, 2, 4)
    plt.title("Top 10 nodes by eigenvector centrality")
    node_color_eig = [eig_cen[node] for node in gsub_eig]
    nx.draw_networkx(gsub_eig, pos=nx.kamada_kawai_layout(gsub_eig, scale=2), node_color=node_color_eig, with_labels=True, cmap=plt.cm.jet)

    ### Add a color bar in the top right corner of the graph
    sm = plt.cm.ScalarMappable(cmap=plt.cm.jet, norm=plt.Normalize(vmin=0, vmax=1))
    sm._A = []
    cbar_ax = plt.axes([0.95, 0.15, 0.05, 0.7])
    plt.colorbar(sm, cax=cbar_ax)

    ## Save the plot
    plt.savefig("/opt/airflow/results/metrics.png")

def plot_pair_grid(g):
    df = pd.DataFrame.from_dict({
        "Betweenness": pd.Series(nx.betweenness_centrality(g)),
        "Degree": pd.Series(nx.degree_centrality(g)),
        "EigenVector": pd.Series(nx.eigenvector_centrality(g)),
        "Closeness": pd.Series(nx.closeness_centrality(g))
    })
    df = df.sort_values(by=list(df.columns))
    df.reset_index(inplace=True, drop=True)
    fig = sns.PairGrid(df)
    fig.map_upper(sns.scatterplot, color="red", s=25)
    fig.map_lower(sns.kdeplot, color="red")
    fig.map_diag(sns.kdeplot, legend=False, color="red")
    #plt.show()
    ## Save the plot
    plt.savefig("/opt/airflow/results/pair_grid.png")

def plot_core_shell(gsub):
    # How many k-cores does this network have?
    print(set([v for k, v in nx.core_number(gsub).items()]))

    # Who are in the innermost core?
    print(list(nx.k_shell(gsub, k=8)))

    # Plot core and shell
    core = nx.k_core(gsub, k=8)
    shell = nx.k_shell(gsub, k=7)

    print("Core nodes: ", core.nodes())
    print("Shell nodes: ", shell.nodes())

    plt.figure(figsize=(10, 10))
    plt.title("Core and shell of the subgraph")

    pos = nx.spring_layout(gsub, seed=707)

    nx.draw_networkx_edges(gsub, pos, alpha=0.4)

    nx.draw_networkx_nodes(gsub, pos, node_size=100, node_color="grey")
    nx.draw_networkx_nodes(core, pos, node_size=100, node_color="red")
    nx.draw_networkx_nodes(shell, pos, node_size=100, node_color="blue")
    #plt.show()
    ## Save the plot
    plt.savefig("/opt/airflow/results/core_shell.png")
