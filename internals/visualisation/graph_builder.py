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
    size: int
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
                    shape='diamond',
                    size=50
                )
                continue

            color = 'purple' if '404' in str(parsed_pages[page].title) else 'blue'
            nodes[page] = NodeInfo(
                node=page,
                title=f'{parsed_pages[page].title} | {page}',
                color=color,
                shape='diamond',
                size=50
            )

            # add node for links
            if len(parsed_pages[page].links) > 1:
                name = link_node(page)
                graph.add_node(name)
                nodes[name] = NodeInfo(
                    node=name,
                    title=name,
                    color='yellow',
                    shape='star',
                    size=10
                )
                graph.add_edge(page, name)

            # add node for objects
            if len(parsed_pages[page].objects) > 1:
                name = obj_node(page)
                graph.add_node(name)
                nodes[name] = NodeInfo(
                    node=name,
                    title=name,
                    color='orange',
                    shape='triangle',
                    size=10
                )
                graph.add_edge(page, name)

            # add node for unreachable hosts
            if len(parsed_pages[page].unreachable) > 1:
                name = f'Unreachable | {page}'
                graph.add_node(name)
                nodes[name] = NodeInfo(
                    node=name,
                    title=name,
                    color='violet',
                    shape='triangleDown',
                    size=10
                )
                graph.add_edge(page, name)

            # add node for cookies
            if len(parsed_pages[page].cookies) > 1:
                name = f'Cookies | {page}'
                graph.add_node(name)
                nodes[name] = NodeInfo(
                    node=name,
                    title=name,
                    color='pink',
                    shape='star',
                    size=10
                )
                graph.add_edge(page, name)

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
                            shape='triangle',
                            size=30
                        )
                    graph.add_edge(link_node(page) if len(parsed_pages[page].links) > 1 else page, link)

            # add links to objects
            for obj in parsed_pages[page].objects:
                name = obj.link
                if name not in nodes.keys():
                    graph.add_node(name)
                    color = 'orange'
                    tp = obj.object_type
                    if 'pdf' in tp:
                        color = 'gray'
                    elif 'image' in tp:
                        color = 'white'
                    elif 'css' in tp:
                        color = 'blue'
                    elif '.js' in tp:
                        color = 'yellow'

                    nodes[name] = NodeInfo(
                        node=name,
                        title=f'{tp} | {name}',
                        color=color,
                        shape='dot',
                        size=20
                    )
                graph.add_edge(obj_node(page) if len(parsed_pages[page].objects) > 1 else page, name)

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
                        shape='square',
                        size=20
                    )
                graph.add_edge(f"Unreachable | {page}" if len(parsed_pages[page].unreachable) > 1 else page, name)

            # add links to cookies
            for i_cookie_source in range(len(parsed_pages[page].cookies)):
                source_name = f'{i_cookie_source} | Cookies | {page}'
                if source_name not in nodes.keys():
                    graph.add_node(source_name)
                    nodes[source_name] = NodeInfo(
                        node=source_name,
                        title=source_name,
                        color='brown',
                        shape='triangle',
                        size=20
                    )
                    graph.add_edge(f'Cookies | {page}' if len(parsed_pages[page].cookies) > 1 else page, source_name)
                    for cookie in parsed_pages[page].cookies[i_cookie_source].cookies:
                        name = f'{cookie.name} | {cookie.value}'
                        graph.add_node(name)
                        nodes[name] = NodeInfo(
                            node=name,
                            title=name,
                            color='orange',
                            shape='dot',
                            size=20
                        )
                        graph.add_edge(source_name if len(parsed_pages[page].cookies[i_cookie_source].cookies) > 1 else page, name)

        return graph, nodes

    @staticmethod
    def export_graph(graph: nx.Graph, nodes: dict[NodeInfo], file_name: str = "graph.html"):
        net = pyvis.network.Network(notebook=True, font_color='#10000000', bgcolor="#222222", height=1000)
        net.barnes_hut(gravity=-15000, central_gravity=0.3, spring_length=100, spring_strength=0.05, damping=0.1, overlap=0)

        # Construct nodes
        for link, node in nodes.items():
            net.add_node(node.node, color=node.color, shape=node.shape, title=node.title, size=node.size)

        # link them
        for edge in graph.edges:
            net.add_edge(edge[0], edge[1])

        net.show_buttons(filter_=['physics'])
        net.show(file_name)
