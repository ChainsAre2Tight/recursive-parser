import networkx as nx
import pyvis.network
from dataclasses import dataclass

from internals.objects import Page, ReferencedObject


def link_node(name):
    return f'Links | {name}'


def obj_node(name):
    return f'Objects | {name}'


def same_website(link1: str, link2: str) -> bool:
    return link1[link1.find('/') + 2:].split('/')[0] == link2[link2.find('/') + 2:].split('/')[0]


@dataclass
class NodeInfo:
    node: str
    title: str
    color: str
    shape: str


class GraphBuilder:

    @staticmethod
    def graph_from_parsed_pages(parsed_pages: dict[str]) -> tuple[nx.Graph, dict[NodeInfo]]:
        graph = nx.Graph()
        nodes = dict()

        # Construct nodes
        for page in parsed_pages.keys():
            # add node itself
            graph.add_node(page)
            if type(parsed_pages[page]) == str:
                nodes[page] = NodeInfo(
                    node=page,
                    title=f'Unreachable | {page}',
                    color='red',
                    shape='diamond'
                )
                continue

            nodes[page] = NodeInfo(
                node=page,
                title=f'{parsed_pages[page].title} | {page}',
                color='blue',
                shape='diamond'
            )

            # add node for links
            if len(parsed_pages[page].links) > 0:
                name = link_node(page)
                graph.add_node(name)
                nodes[name] = NodeInfo(
                    node=name,
                    title=name,
                    color='yellow',
                    shape='square'
                )
                graph.add_edge(page, name)

            # add node for objects
            if len(parsed_pages[page].objects) > 0:
                name = obj_node(page)
                graph.add_node(name)
                nodes[name] = NodeInfo(
                    node=name,
                    title=name,
                    color='orange',
                    shape='triangle'
                )
                graph.add_edge(page, name)

            # add node for unreachable hosts
            if len(parsed_pages[page].unreachable) > 0:
                name = f'Unreachable | {page}'
                graph.add_node(name)
                nodes[name] = NodeInfo(
                    node=name,
                    title=name,
                    color='red',
                    shape='triangleDown'
                )
                graph.add_edge(page, name)

            # add node for cookies
            # add node for forms
            # add node for ...

        # add links between nodes
        for page in parsed_pages.keys():
            if type(parsed_pages[page]) == str:
                continue
            # add links to other pages
            for link in parsed_pages[page].links:
                if link in parsed_pages.keys():
                    graph.add_edge(page, link)
                else:
                    if link not in nodes.keys():
                        graph.add_node(link)
                        same_site = same_website(page, link)
                        nodes[link] = NodeInfo(
                            node=link,
                            title=link,
                            color='orange' if same_site else 'green',
                            shape='triangle'
                        )
                    graph.add_edge(link_node(page), link)

            # add links to objects
            for obj in parsed_pages[page].objects:
                name = obj.link
                if name not in nodes.keys():
                    graph.add_node(name)
                    color = 'orange'
                    tp = obj.object_type
                    if 'pdf' in tp:
                        color = 'red'
                    elif 'image' in tp:
                        color = 'white'
                    elif 'css' in tp:
                        color = 'blue'

                    nodes[name] = NodeInfo(
                        node=name,
                        title=f'{tp} | {name}',
                        color=color,
                        shape='square'
                    )
                graph.add_edge(obj_node(page), name)

            # add links to unreachable pages
            for obj in parsed_pages[page].unreachable:
                name = obj.link
                if name not in nodes.keys():
                    graph.add_node(name)
                    tp = obj.object_type
                    color = 'orange' if tp == "Unknown/Timeout" else 'red'
                    color = 'purple' if same_website(page, name) else color

                    nodes[name] = NodeInfo(
                        node=name,
                        title=f'{tp} | {name}',
                        color=color,
                        shape='square'
                    )
                graph.add_edge(f"Unreachable | {page}", name)

            # add links to cookies

        return graph, nodes

    @staticmethod
    def export_graph(graph: nx.Graph, nodes: dict[NodeInfo], file_name: str = "graph.html"):
        net = pyvis.network.Network(notebook=True, font_color='#10000000', bgcolor="#222222")

        # Construct nodes
        for link, node in nodes.items():
            net.add_node(node.node, color=node.color, shape=node.shape, title=node.title)

        # link them
        for edge in graph.edges:
            net.add_edge(edge[0], edge[1])

        net.show_buttons(filter_=['physics'])
        net.show(file_name)
