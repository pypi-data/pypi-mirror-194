from typing import Optional

Direction = {"TD": "TD", "LR": "LR", "RL": "RL", "BT": "BT"}
ChartType = {"graph": "graph", "flowchart": "flowchart"}


class MermaidFlowchart:
    def __init__(self):
        self.nodes = []
        self.edges = []

    @property
    def header(self):
        return "```mermaid\n"

    @property
    def footer(self):
        return "```\n"

    def graphtype(self, type: str, direction: str):
        t = ChartType.get(type)
        if t is None:
            t = "graph"
        d = Direction.get(direction)
        if d is None:
            d = "TD"
        return f"{t} {d};\n"

    def add_node(self, node: str):
        """Function to add a file or folder as a node when there is only one.

        Args:
            node (str): File name or folder name to be added as a node.
        """
        self.nodes.append(node)

    def add_edge(
        self,
        *,
        from_i_node: Optional[str] = None,
        from_node: Optional[str] = None,
        to_i_node: Optional[str] = None,
        to_node: Optional[str] = None,
        parent_i_node: Optional[str] = None,
        parent_node: Optional[str] = None,
    ):
        """
        Registers a directory containing multiple files and folders as nodes.

        Args:
            from_i_node (Optional[str], optional): Node number of the current directory or file. Defaults to None.
            from_node (Optional[str], optional): Name of the current directory or file. Defaults to None.
            to_i_node (Optional[str], optional): Node number of the child file or directory. Defaults to None.
            to_node (Optional[str], optional): Name of the child file or directory. Defaults to None.
            parent_i_node (Optional[str], optional): Node number of the parent file or directory. Defaults to None.
            parent_node (Optional[str], optional): Name of the parent file or directory. Defaults to None.
        """
        self.edges.append(
            (parent_i_node, parent_node, from_i_node, from_node, to_i_node, to_node)
        )

    def concat_node_str(self) -> str:
        node_str = ""
        for node in self.nodes:
            node_str += f"  {node};\n"
        return node_str

    def concat_edge_str(self) -> str:
        """Function to create the display of the node's edge.
        The edge information is stored in a tuple, displaying the index number and contents.
        * index: 0 Inode of the parent directory.
        * index: 1 Name of the parent directory.
        * index: 2 Inode of the current directory/file.
        * index: 3 Name of the current directory/file.
        * index: 4 Inode of the child directory/file or symbolic link.
        * index: 5 Name of the child directory/file or symbolic link.

        Returns:
            str: Output of the arrow display of the node.
        """
        edge_str = ""
        __tmp_str = ""
        edge_store = []
        for edge in self.edges:
            __tmp_str = f"  {edge[0]}[{edge[1]}]-->{edge[2]}[{edge[3]}];\n"
            if __tmp_str in edge_store:
                continue
            edge_store.append(__tmp_str)

            if (edge[4] is None) and (edge[5] is None):
                continue
            __tmp_str = f"  {edge[2]}[{edge[3]}]-->{edge[4]}[{edge[5]}];\n"
            if __tmp_str in edge_store:
                continue
            edge_store.append(__tmp_str)

        edge_str = "".join(edge_store)
        return edge_str

    def to_markdown(self, *, type: str = "graph", direction: str = "TD") -> str:
        """Generate markdown-formatted Mermaid syntax.
        Takes the type of the chart and the directionality of the graph as arguments to enable display customization.

        Args:
            type (str, optional): The type of chart. Defaults to "graph".
            direction (str, optional): The direction of the graph. Defaults to "TD".

        Returns:
            str: Markdown-formatted Mermaid syntax.
        """
        mermaid_str = ""
        mermaid_str += self.header
        mermaid_str += self.graphtype(type, direction)
        mermaid_str += self.concat_node_str()
        mermaid_str += self.concat_edge_str()
        mermaid_str += self.footer
        return mermaid_str
