#!/usr/bin/python3
import requests
from grape import Graph
from grape import GraphVisualizer
from matplotlib import figure
import graphviz
import sys
import re
def genWikiLinksByTitle(title): 
    with open('minecraftnodelist.tsv', 'xt', encoding='utf-8') as node_file:
        node_file.write(f'{title!r}\n')
    response = requests.Session().get( 
        url="https://en.wikipedia.org/w/api.php", 
        params={ 
            "utf8": 1, 
            "formatversion": 2, 
            "format": "json", 
            "action": "query", 
            "titles": title, 
            "prop": "links", 
            "pllimit": "max", 
        } 
    ) 
 
    wikiData = response.json() 
    pages = wikiData['query']['pages'][0]['links']
    for page in pages: 
        x = re.sub('\'','\\\'', page['title'])
        with open('minecraftnodelist.tsv', 'at', encoding='utf-8') as node_file:
            node_file.write(f'{x!r}\n') 
        with open('minecraftedgelist.tsv', 'at', encoding='utf-8') as edge_file:
            edge_file.write(f'{title!r}\t{x!r}\n')
genWikiLinksByTitle("Minecraft")
mineGraph = Graph.from_csv(
    edge_path="./minecraftedgelist.tsv",
    edge_list_separator="\t",
    edge_list_header=False,
    sources_column_number=0,
    destinations_column_number=1,
    edge_list_numeric_node_ids=False,
    node_path="./minecraftnodelist.tsv",
    node_list_header=False,
    nodes_column_number=0,
    directed=True,
    name="MineGraph",
    edge_list_is_correct=True,
    node_list_separator='\n',
)
graphViz = GraphVisualizer(mineGraph, decomposition_method="TSNE", n_components=2, edge_embedding_method="Hadamard")

dot_content = graphViz.plot_dot()

with open('graph.dot', 'w', encoding='utf-8') as sys.stdout:
    print(dot_content)
graphviz.render(engine='dot', format='png', filepath='./graph.dot', renderer='cairo', formatter='cairo', outfile='./g.png', raise_if_result_exists=True, overwrite_filepath=False)
